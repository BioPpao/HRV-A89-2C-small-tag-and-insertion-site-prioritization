#!/usr/bin/env python3
"""Shared helpers for CONSERVATION_001.

Uses only stdlib plus requests in acquisition script. Alignment is
reference-guided because no mature MSA executable is available in this runtime.
"""

from __future__ import print_function

import math
import re


AA = set("ACDEFGHIKLMNPQRSTVWY")
UNKNOWN = set("XBZUOJ")


def read_fasta(path):
    records = []
    name = None
    seq = []
    with open(path) as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if name is not None:
                    records.append((name, "".join(seq)))
                name = line[1:]
                seq = []
            else:
                seq.append(line.strip())
    if name is not None:
        records.append((name, "".join(seq)))
    return records


def write_fasta(records, path, width=80):
    with open(path, "w") as out:
        for name, seq in records:
            out.write(">%s\n" % name)
            for i in range(0, len(seq), width):
                out.write(seq[i:i + width] + "\n")


def clean_seq(seq):
    return re.sub("[^A-Za-z*]", "", seq).upper()


def parse_type_label(text, species_prefix):
    text = (text or "").replace("_", " ")
    patterns = [
        r"HRV[\s-]*([ABC])[\s-]*(\d+[A-Z]?)",
        r"RHINOVIRUS[\s-]*([ABC])[\s-]*(\d+[A-Z]?)",
        r"HUMAN RHINOVIRUS[\s-]*([ABC])?\s*SEROTYPE\s*(\d+[A-Z]?)",
        r"HUMAN RHINOVIRUS[\s-]*(\d+[A-Z]?)",
        r"RHINOVIRUS[\s-]*(\d+[A-Z]?)",
    ]
    up = text.upper()
    for pat in patterns:
        m = re.search(pat, up)
        if not m:
            continue
        groups = [g for g in m.groups() if g]
        if len(groups) == 2 and groups[0] in ("A", "B", "C"):
            return groups[0] + groups[1]
        if len(groups) >= 1:
            return species_prefix + groups[-1]
    return "ambiguous"


def shannon_entropy(counts):
    total = float(sum(counts.values()))
    if total <= 0:
        return 0.0
    ent = 0.0
    for value in counts.values():
        if value:
            p = value / total
            ent -= p * math.log(p, 2)
    return ent


def normalize_entropy(ent):
    return ent / math.log(20, 2)


def nw_align(ref, seq, match=2, mismatch=-1, gap=-3):
    """Needleman-Wunsch global alignment."""
    n = len(ref)
    m = len(seq)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    trace = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        score[i][0] = i * gap
        trace[i][0] = 1
    for j in range(1, m + 1):
        score[0][j] = j * gap
        trace[0][j] = 2
    for i in range(1, n + 1):
        ri = ref[i - 1]
        row = score[i]
        prev = score[i - 1]
        for j in range(1, m + 1):
            diag = prev[j - 1] + (match if ri == seq[j - 1] else mismatch)
            up = prev[j] + gap
            left = row[j - 1] + gap
            best = diag
            tb = 0
            if up > best:
                best = up
                tb = 1
            if left > best:
                best = left
                tb = 2
            row[j] = best
            trace[i][j] = tb
    i, j = n, m
    ar = []
    ase = []
    while i > 0 or j > 0:
        tb = trace[i][j]
        if i > 0 and j > 0 and tb == 0:
            ar.append(ref[i - 1])
            ase.append(seq[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and (j == 0 or tb == 1):
            ar.append(ref[i - 1])
            ase.append("-")
            i -= 1
        else:
            ar.append("-")
            ase.append(seq[j - 1])
            j -= 1
    return "".join(reversed(ar)), "".join(reversed(ase)), score[n][m]


def sw_extract(ref, target, match=3, mismatch=-1, gap=-4):
    """Smith-Waterman local alignment of A89 2C against target polyprotein."""
    n = len(ref)
    m = len(target)
    score = [[0] * (m + 1) for _ in range(n + 1)]
    trace = [[0] * (m + 1) for _ in range(n + 1)]
    best = 0
    best_pos = (0, 0)
    for i in range(1, n + 1):
        ri = ref[i - 1]
        row = score[i]
        prev = score[i - 1]
        for j in range(1, m + 1):
            diag = prev[j - 1] + (match if ri == target[j - 1] else mismatch)
            up = prev[j] + gap
            left = row[j - 1] + gap
            val = 0
            tb = 3
            if diag >= up and diag >= left and diag > 0:
                val = diag
                tb = 0
            elif up >= left and up > 0:
                val = up
                tb = 1
            elif left > 0:
                val = left
                tb = 2
            row[j] = val
            trace[i][j] = tb
            if val > best:
                best = val
                best_pos = (i, j)
    i, j = best_pos
    ar = []
    at = []
    target_positions = []
    while i > 0 and j > 0 and score[i][j] > 0:
        tb = trace[i][j]
        if tb == 0:
            ar.append(ref[i - 1])
            at.append(target[j - 1])
            target_positions.append(j)
            i -= 1
            j -= 1
        elif tb == 1:
            ar.append(ref[i - 1])
            at.append("-")
            i -= 1
        elif tb == 2:
            ar.append("-")
            at.append(target[j - 1])
            target_positions.append(j)
            j -= 1
        else:
            break
    ar = "".join(reversed(ar))
    at = "".join(reversed(at))
    target_positions = list(reversed(target_positions))
    aligned_ref = sum(1 for c in ar if c != "-")
    matches = sum(1 for a, b in zip(ar, at) if a != "-" and b != "-" and a == b)
    comparable = sum(1 for a, b in zip(ar, at) if a != "-" and b != "-")
    if not target_positions:
        return None
    start = min(target_positions)
    end = max(target_positions)
    return {
        "score": best,
        "ref_coverage": aligned_ref / float(n),
        "identity": matches / float(comparable or 1),
        "target_start": start,
        "target_end": end,
        "sequence": target[start - 1:end],
    }


def bool_text(value):
    return "True" if value else "False"
