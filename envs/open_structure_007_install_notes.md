# OPEN_STRUCTURE_PIPELINE_007 environment notes

Primary prefix:

`/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization/.tools/envs/open_structure_007`

Base install:

```bash
.tools/bin/micromamba create -y -p .tools/envs/open_structure_007 -f envs/open_structure_007.yml
```

Compatibility repairs applied on 2026-08-22:

```bash
.tools/envs/open_structure_007/bin/pip install --no-cache-dir --upgrade "jax[cuda11_pip]==0.4.14" -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html
.tools/envs/open_structure_007/bin/pip install --no-cache-dir --no-deps colabfold==1.5.3
.tools/envs/open_structure_007/bin/pip install --no-cache-dir alphafold-colabfold==2.3.5
.tools/envs/open_structure_007/bin/pip install --no-cache-dir 'dm-haiku==0.0.9' 'pandas<2.0.0,>=1.3.4' 'absl-py<2.0.0,>=1.0.0' 'importlib-metadata<5.0.0,>=4.8.2' 'protobuf<5.0.0,>=3.20.3' 'keras<2.13,>=2.12.0' 'typing-extensions<4.6.0,>=3.6.6'
.tools/envs/open_structure_007/bin/pip uninstall -y tensorflow-cpu
.tools/bin/micromamba install -y --force-reinstall -p .tools/envs/open_structure_007 -c conda-forge tensorflow=2.12.1 tensorflow-base=2.12.1 tensorflow-estimator=2.12.1 keras=2.12.0 protobuf=4.21.12 typing-extensions=4.5.0
```

Rationale:

- `biopython>=1.88` removed `Bio.Data.SCOPData`, which breaks ColabFold 1.5.3.
- `dm-haiku 0.0.17` expects newer JAX APIs than ColabFold 1.5.3/JAX 0.4.14.
- GPU prediction uses the CUDA 11 JAX wheel because the cluster exposes CUDA 11/12-era NVIDIA drivers and the Conda JAX build was CPU-only.

Exact observed package snapshot is recorded in:

`results/open_structure_007/pip_freeze_open_structure_007.txt`
