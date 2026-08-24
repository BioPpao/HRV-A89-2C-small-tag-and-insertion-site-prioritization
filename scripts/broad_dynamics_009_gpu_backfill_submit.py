#!/usr/bin/env python3
"""Backfill pending BROAD_DYNAMICS_009 production replicas onto free GPUs.

This script is intentionally narrow: it only handles bd009_prod20 array rows
from results/broad_dynamics_009/production_manifest.tsv.
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path

MANIFEST = Path("results/broad_dynamics_009/production_manifest.tsv")
LOG = Path("results/broad_dynamics_009/gpu_backfill_submissions.tsv")
SBATCH_SCRIPT = "scripts/broad_dynamics_009_gmx_production.sbatch"


def run(cmd: list[str], check: bool = True) -> str:
    out = subprocess.run(cmd, check=check, text=True, capture_output=True)
    return out.stdout.strip()


def parse_tres(text: str, key: str) -> int:
    for item in text.split(","):
        if item.startswith(key + "="):
            return int(item.split("=", 1)[1].rstrip("M"))
    return 0


def node_blocks() -> list[dict[str, str]]:
    blocks = [b for b in run(["scontrol", "show", "node"]).split("\n\n") if b.strip()]
    nodes: list[dict[str, str]] = []
    for block in blocks:
        d: dict[str, str] = {}
        for key, val in re.findall(r"(\w+)=([^\s]+)", block):
            d[key] = val
        if "NodeName" in d:
            nodes.append(d)
    return nodes


def free_gpu_nodes(partitions: set[str]) -> list[tuple[str, str, int]]:
    out: list[tuple[str, str, int]] = []
    bad = ("DOWN", "DRAIN", "NOT_RESPONDING")
    for n in node_blocks():
        node_parts = set(n.get("Partitions", "").split(","))
        usable = sorted(node_parts & partitions)
        if not usable or any(x in n.get("State", "") for x in bad):
            continue
        cfg = parse_tres(n.get("CfgTRES", ""), "gres/gpu")
        alloc = parse_tres(n.get("AllocTRES", ""), "gres/gpu")
        free = max(cfg - alloc, 0)
        for _ in range(free):
            out.append((n["NodeName"], usable[0], free))
    return out


def expand_task_id(job_id: str) -> list[tuple[str, int]]:
    m = re.match(r"(\d+)_\[(.+)\]$", job_id)
    if m:
        base, spec = m.groups()
        vals: list[tuple[str, int]] = []
        for part in spec.split(","):
            if "-" in part:
                a, b = map(int, part.split("-", 1))
                vals.extend((base, i) for i in range(a, b + 1))
            else:
                vals.append((base, int(part)))
        return vals
    m = re.match(r"(\d+)_(\d+)$", job_id)
    if m:
        return [(m.group(1), int(m.group(2)))]
    return []


def active_tasks() -> tuple[set[int], dict[int, str]]:
    stdout = run(["squeue", "-h", "-u", os.environ.get("USER", ""), "-n", "bd009_prod20", "-o", "%i\t%T"], check=False)
    active: set[int] = set()
    pending: dict[int, str] = {}
    for line in stdout.splitlines():
        if not line.strip():
            continue
        jid, state = line.split("\t", 1)
        for base, idx in expand_task_id(jid):
            active.add(idx)
            if state.upper().startswith("PENDING"):
                pending[idx] = f"{base}_{idx}"
    return active, pending


def read_manifest() -> tuple[list[str], list[dict[str, str]]]:
    with MANIFEST.open(newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        return reader.fieldnames or [], list(reader)


def write_manifest(fields: list[str], rows: list[dict[str, str]]) -> None:
    with MANIFEST.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def append_log(row: dict[str, str]) -> None:
    fields = ["timestamp", "array_index", "old_job_id", "new_job_id", "node", "partition", "command", "status"]
    exists = LOG.exists()
    with LOG.open("a", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        if not exists:
            writer.writeheader()
        writer.writerow(row)


def submit_one(idx: int, old_job: str, node: str, partition: str, args: argparse.Namespace) -> str:
    if old_job and args.rescue_pending:
        run(["scancel", old_job], check=False)
    cmd = [
        "sbatch",
        "--parsable",
        f"--partition={partition}",
        "--gres=gpu:1",
        f"--cpus-per-task={args.cpus_per_task}",
        f"--mem={args.mem}",
        "--oversubscribe",
        f"--nodelist={node}",
        f"--array={idx}",
        SBATCH_SCRIPT,
    ]
    if args.dry_run:
        return "DRY_RUN:" + " ".join(cmd)
    return run(cmd)


def once(args: argparse.Namespace) -> int:
    fields, rows = read_manifest()
    active, pending = active_tasks()
    slots = free_gpu_nodes(set(args.partitions.split(",")))
    candidates = [
        int(r["slurm_array_index"])
        for r in rows
        if int(r["slurm_array_index"]) not in active
        or (args.rescue_pending and int(r["slurm_array_index"]) in pending)
    ]
    candidates = [
        i for i in sorted(set(candidates))
        if i not in active or (args.rescue_pending and i in pending)
    ]
    n = min(len(slots), len(candidates), args.max_submit)
    now = datetime.now().isoformat(timespec="seconds")
    for idx, (node, partition, _free) in zip(candidates[:n], slots[:n]):
        old = pending.get(idx, "")
        new = submit_one(idx, old, node, partition, args)
        new_id = new if new.startswith("DRY_RUN:") else f"{new}_{idx}"
        for r in rows:
            if int(r["slurm_array_index"]) == idx:
                r["job_id"] = new_id
                r["status"] = f"backfill_submitted_{partition}_{node}"
        append_log({
            "timestamp": now,
            "array_index": str(idx),
            "old_job_id": old,
            "new_job_id": new_id,
            "node": node,
            "partition": partition,
            "command": new if new.startswith("DRY_RUN:") else f"sbatch array={idx}",
            "status": "dry_run" if args.dry_run else "submitted",
        })
    if n and not args.dry_run:
        write_manifest(fields, rows)
    return n


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--partitions", default="A40,RTX3090")
    p.add_argument("--cpus-per-task", type=int, default=2)
    p.add_argument("--mem", default="8G")
    p.add_argument("--max-submit", type=int, default=8)
    p.add_argument("--interval", type=int, default=300)
    p.add_argument("--loop", action="store_true")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--rescue-pending", action=argparse.BooleanOptionalAction, default=False)
    args = p.parse_args()
    while True:
        submitted = once(args)
        print(f"{datetime.now().isoformat(timespec='seconds')}\tsubmitted={submitted}", flush=True)
        if not args.loop:
            break
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
