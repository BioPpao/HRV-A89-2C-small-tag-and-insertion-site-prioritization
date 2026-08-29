"""Render fixed-view WT overlays for Figure 5 with the local PyMOL installation.

Run from the repository root:
    D:\\Pymol\\Scripts\\pymol.exe -cq scripts/render_figure05_structure_insets.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import pymol
from pymol import cmd

pymol.finish_launching(["pymol", "-cq"])


ROOT = Path.cwd()
OUT = ROOT / "figures" / "group_meeting" / "Figure05_inserted_structure_landscape"
WT = ROOT / "results" / "open_structure_007" / "wt_smoke" / (
    "A89_2C_WT_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_007.pdb"
)

CASES = [
    {
        "construct_id": "A89_2C_289_290_MAP8",
        "junction": "289|290",
        "tag": "MAP8",
        "tag_resi": "290-297",
        "model": ROOT / "results" / "open_structure_007" / "tier1_shallow"
        / "A89_2C_289_290_MAP8_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_011.pdb",
        "color": "0x0B6E69",
        "tag_color": "0x17324D",
        "output": "inset_289_290_MAP8.png",
    },
    {
        "construct_id": "A89_2C_290_291_MAP8",
        "junction": "290|291",
        "tag": "MAP8",
        "tag_resi": "291-298",
        "model": ROOT / "results" / "open_structure_007" / "tier1_shallow"
        / "A89_2C_290_291_MAP8_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_011.pdb",
        "color": "0x2A9D8F",
        "tag_color": "0x17324D",
        "output": "inset_290_291_MAP8.png",
    },
    {
        "construct_id": "A89_2C_248_249_MAP8",
        "junction": "248|249",
        "tag": "MAP8",
        "tag_resi": "249-256",
        "model": ROOT / "results" / "open_structure_007" / "tier1_shallow"
        / "A89_2C_248_249_MAP8_unrelaxed_rank_001_alphafold2_ptm_model_1_seed_011.pdb",
        "color": "0x0B6E69",
        "tag_color": "0x17324D",
        "output": "inset_248_249_MAP8.png",
    },
]


def configure_scene() -> None:
    cmd.reinitialize()
    cmd.bg_color("white")
    cmd.set("orthoscopic", 1)
    cmd.set("ray_opaque_background", 1)
    cmd.set("ray_trace_mode", 1)
    cmd.set("ray_trace_color", "0x17324D")
    cmd.set("antialias", 2)
    cmd.set("ambient", 0.48)
    cmd.set("direct", 0.42)
    cmd.set("specular", 0.12)
    cmd.set("shininess", 8)
    cmd.set("cartoon_smooth_loops", 1)
    cmd.set("cartoon_fancy_helices", 1)
    cmd.set("cartoon_sampling", 14)
    cmd.set("cartoon_transparency", 0.0)


def render_case(case: dict[str, object], reference_view: tuple[float, ...]) -> dict[str, str]:
    configure_scene()
    cmd.load(str(WT), "wt")
    cmd.load(str(case["model"]), "inserted")

    # PyMOL's sequence-aware align retains the insertion as a gap while fitting native C-alpha atoms.
    cmd.align(
        "inserted and polymer.protein and name CA",
        "wt and polymer.protein and name CA",
        cycles=5,
        transform=1,
    )
    cmd.select("tag", f"inserted and chain A and resi {case['tag_resi']}")
    cmd.select("native_inserted", "inserted and polymer.protein and not tag")
    cmd.select("local_wt", "byres (wt within 12 of tag)")
    cmd.select("local_inserted", "byres (inserted within 12 of tag)")

    cmd.hide("everything", "all")
    cmd.show("cartoon", "local_wt")
    cmd.show("cartoon", "local_inserted")
    cmd.show("sticks", "tag")
    cmd.color("0xC7CCD1", "local_wt")
    cmd.color(str(case["color"]), "local_inserted")
    cmd.color(str(case["tag_color"]), "tag")
    cmd.set("cartoon_transparency", 0.42, "local_wt")
    cmd.set("cartoon_transparency", 0.03, "local_inserted")
    cmd.set("stick_radius", 0.18, "tag")

    # Fixed rotation and a constant zoom buffer give comparable local snapshots.
    cmd.set_view(reference_view)
    cmd.center("tag")
    cmd.zoom("tag", buffer=12.0, complete=1)
    cmd.clip("slab", 34.0)

    out_path = OUT / str(case["output"])
    cmd.ray(1400, 1000)
    cmd.png(str(out_path), dpi=300)

    return {
        "construct_id": str(case["construct_id"]),
        "source_model_path_or_identifier": str(Path(case["model"]).relative_to(ROOT)).replace("\\", "/"),
        "wt_reference_path_or_identifier": str(WT.relative_to(ROOT)).replace("\\", "/"),
        "camera_orientation_strategy": (
            "fixed WT-derived orthoscopic rotation; model sequence-aware CA alignment; "
            "tag-centered 12-A buffer; 34-A slab"
        ),
        "site_shown": str(case["junction"]),
        "tag_shown": str(case["tag"]),
        "rendering_script_used": "scripts/render_figure05_structure_insets.py",
        "output_file": str(out_path.relative_to(ROOT)).replace("\\", "/"),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    requested = sys.argv[1] if len(sys.argv) > 1 else None
    selected_cases = [
        case for case in CASES if requested is None or case["construct_id"] == requested
    ]
    if not selected_cases:
        raise SystemExit(f"Unknown construct_id: {requested}")

    configure_scene()
    cmd.load(str(WT), "wt")
    cmd.orient("wt and polymer.protein")
    reference_view = cmd.get_view()

    new_rows = [render_case(case, reference_view) for case in selected_cases]
    manifest_path = OUT / "Figure05_structure_inset_manifest.tsv"
    previous = []
    if manifest_path.exists():
        with manifest_path.open("r", newline="", encoding="utf-8") as handle:
            previous = list(csv.DictReader(handle, delimiter="\t"))
    replaced = {row["construct_id"] for row in new_rows}
    manifest = [row for row in previous if row["construct_id"] not in replaced] + new_rows
    order = {case["construct_id"]: i for i, case in enumerate(CASES)}
    manifest.sort(key=lambda row: order.get(row["construct_id"], 999))
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(manifest[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(manifest)

    print(f"Rendered {len(new_rows)} structure inset(s) to {OUT}")
    cmd.quit()


if __name__ == "__main__":
    main()
