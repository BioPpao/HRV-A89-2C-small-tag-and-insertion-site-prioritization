# Local Multimer Recovery V2

Focused local trimer modeling completed for 6 constructs using single-sequence AlphaFold2 multimer.

Context: tagged protomer plus two WT protomers. This is a tractable local accommodation cross-check, not a full A89 hexamer prediction and not biological validation.

Outputs: `results/broad_dynamics_009/local_multimer/local_multimer_model_metrics.tsv` and `data/local_multimer_tag_context_v2.tsv`.

## Result

All completed local multimer rows are marked `completed_all_models_nonfinite_coordinates`.

The generated PDB coordinate fields and AlphaFold multimer confidence values parsed from score JSON files were non-finite (`nan`). The integration script therefore did not compute clash, orientation, interface-preservation or tag-neighbor geometry metrics from these models.

Interpretation:

- supports rigid-placement interpretation: no;
- weakens a previous rigid clash: no;
- creates a new oligomer-context conflict: no;
- final status: `inconclusive_nonfinite_multimer_coordinates`.

This is a technical model-output limitation, not evidence that any candidate is biologically tolerated or intolerant.
