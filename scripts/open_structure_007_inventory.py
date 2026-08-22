#!/usr/bin/env python3
"""Write OPEN_STRUCTURE_PIPELINE_007 environment inventory."""
from __future__ import annotations

import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

import pandas as pd


def run(label: str, cmd: list[str], timeout: int = 30) -> dict[str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        text = (p.stdout + p.stderr).strip()
        return {"probe": label, "status": "completed", "exit_code": str(p.returncode), "value": text.replace("\t", " ").replace("\n", " | ")}
    except subprocess.TimeoutExpired:
        return {"probe": label, "status": "timeout", "exit_code": "timeout", "value": "command timed out"}
    except Exception as e:
        return {"probe": label, "status": "failed", "exit_code": "exception", "value": repr(e)}


def py_probe(python: str) -> list[dict[str, str]]:
    rows = [run(f"{python}:version", [python, "--version"], timeout=10)]
    code = (
        "import importlib.util,sys;"
        "mods=['colabfold','jax','openmm','MDAnalysis','mdtraj','Bio','pandas','scipy','numpy'];"
        "print('python_executable',sys.executable);"
        "[print(m,'OK' if importlib.util.find_spec(m) else 'MISSING') for m in mods]"
    )
    rows.append(run(f"{python}:python_modules", [python, "-c", code], timeout=20))
    return rows


def main() -> None:
    outdir = Path("results/open_structure_007")
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    rows.append({"probe": "cwd", "status": "completed", "exit_code": "0", "value": str(Path.cwd())})
    rows.append({"probe": "hostname_python", "status": "completed", "exit_code": "0", "value": socket.gethostname()})
    rows.append({"probe": "cuda_visible_devices", "status": "completed", "exit_code": "0", "value": os.environ.get("CUDA_VISIBLE_DEVICES", "")})
    for label, cmd, timeout in [
        ("pwd", ["pwd"], 10),
        ("hostname", ["hostname"], 10),
        ("df_h", ["df", "-h"], 20),
        ("df_i", ["df", "-i"], 20),
        ("quota_s", ["quota", "-s"], 10),
        ("du_project_tools", ["du", "-sh", ".", ".tools"], 60),
        ("du_cache", ["du", "-sh", str(Path.home() / ".cache")], 10),
        ("which_slurm", ["bash", "-lc", "which sinfo; which squeue; which sbatch; which srun"], 10),
        ("sinfo_gpu_nodes", ["bash", "-lc", "sinfo -N -o '%N %P %G %t' | grep -Ei 'gpu|3090|cuda|a40' || true"], 20),
        ("squeue_user", ["bash", "-lc", "squeue -u \"$USER\""], 20),
        ("nvidia_smi", ["bash", "-lc", "nvidia-smi 2>&1 || true"], 10),
        ("dev_nvidia", ["bash", "-lc", "ls -l /dev/nvidia* 2>&1 || true"], 10),
        ("module_relevant", ["bash", "-lc", "module avail 2>&1 | grep -Ei 'colab|alphafold|openfold|esmfold|jax|cuda|pytorch|openmm|mdanalysis|mdtraj|dssp|mkdssp|usalign|tm-align|tmalign|hh-suite|hhsuite|mmseqs|kalign|python|gromacs|amber|apbs' | head -240 || true"], 30),
        ("command_paths", ["bash", "-lc", "for x in colabfold_batch colabfold_search colabfold_download colabfold_relax nvidia-smi python3 pip3 micromamba conda mamba usalign USalign TMalign TM-align mkdssp dssp mmseqs kalign jackhmmer hhblits; do printf '%s=' \"$x\"; command -v \"$x\" || true; done"], 20),
        ("micromamba_info", [".tools/bin/micromamba", "info"], 20),
    ]:
        rows.append(run(label, cmd, timeout))
    for python in [
        ".tools/envs/open_structure_007/bin/python",
        "/public/home/yukang/.conda/envs/hrv2c_hexamer/bin/python",
        ".tools/envs/hrv2c-one-shot/bin/python3.11",
    ]:
        if Path(python).exists():
            rows.extend(py_probe(python))
    pd.DataFrame(rows).to_csv(outdir / "environment_inventory.tsv", sep="\t", index=False)


if __name__ == "__main__":
    main()
