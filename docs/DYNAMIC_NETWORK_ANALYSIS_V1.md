# Dynamic Network Analysis V1

Generated: 2026-08-24

Task: `BROAD_DYNAMICS_AND_RECOVERY_009`

## Summary

Dynamic network analysis was completed for all 39 included trajectories.

Output:

- `data/dynamic_network_perturbation_v1.tsv`

Method:

- align native A89 `112-321` CA coordinates to each replica's first frame;
- calculate native-residue CA dynamic cross-correlation;
- define persistent CA contact networks from reference contacts retained in >= 50% of frames;
- estimate coupling from the insertion-local window to broad functional neighborhoods:
  - Walker-A-like `153-166`;
  - Walker-B/sensor-like `214-224` and `248-260`;
  - C-terminal oligomer/RNA-like `286-310`.

## Main Result

Network metrics are now available as a screening layer, but they should be interpreted cautiously because this is a 20 ns apo/protein-only segment model.

Raw local-to-functional DCCM values in the dynamics panel ranged approximately from `0.2267` to `0.3549` among candidate constructs. The strongest raw values were observed for `289|290 x G196_minimal` and the hard-negative `155|156 x MAP8`; these are perturbation signals for review, not functional proof.

Persistent contact-network edge counts and path metrics are retained in the TSV. No network result overrides direct homolog InDel conflict or exact nucleotide/RNA uncertainty.

## Limits

- WT has no insertion-local window, so some effect-vs-WT fields are `NA` by definition rather than failed calculations.
- The network uses CA contacts and correlations, not explicit RNA, ATP/Mg, membrane or hexamer dynamics.
- Community analysis was not promoted to a primary claim because the 20 ns screen is too short for stable community-level biological interpretation.
