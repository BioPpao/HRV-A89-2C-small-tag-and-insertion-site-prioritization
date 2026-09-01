# Codex Long Task — Task 011

## 9A5-bound monomer + hexamer context re-evaluation of HRV-A89 2C internal-tag candidates

你现在执行一个持续到**产生最终科学结果、完成仓库更新并 push GitHub**为止的长任务。

不要只完成“数据检查”“写脚本”“建立目录”或“给出下一步建议”就停止。

用户休息期间不方便回答问题。除非遇到无法通过服务器现有文件、两个 Git 仓库、Git 历史、项目文档和已有结果解决的真正硬性阻塞，否则：

**不要等待用户确认，不要中途停下来提问。**

采用保守、可追踪、科学上可辩护的方法继续执行，直到能够给出当前数据支持下的最终候选判断。

---

# 0. 核心原则：SEARCH FIRST, COMPUTE LAST

本任务最重要的资源原则：

> **任何结构、模型、MD endpoint、对接结果、tagged construct、表格或分析，只要服务器和两个项目中已经存在可靠版本，就直接复用。不要重新计算。**

计算前必须按以下顺序检索：

1. 两个服务器本地仓库中的 tracked files
2. 两个 GitHub 仓库及其 Git history
3. 仓库中记录的 server-only / raw-output absolute paths
4. project inventory / provenance / registry / reports 中引用的历史输出
5. 服务器上与这些项目直接对应的已有计算目录
6. 只有确认现有结果缺失、损坏、已被 REJECTED，或者不能回答当前问题时，才允许新增计算

严禁因为“重新跑比较方便”而重复：

* AlphaFold / ColabFold
* 9A5 docking
* hexamer construction
* 已完成 MD
* 已存在的 tagged monomer prediction
* 已存在的 rigid hexamer placement
* 已完成 SASA / clash / interface 分析

先证明“现有数据不够”，再启动新计算。

---

# 1. 两个服务器项目

## Source repository — read mostly

```bash
/public/home/yukang/HRV_Oligomers
```

GitHub：

`BioPpao/HRV-Oligomers`

这个仓库负责提供：

* HRV-A89 full-length 2C monomers
* full-length 2C hexamers
* 9A5–2C historical monomer/core complexes
* current 1×9A5 + full-length 2C hexamer
* independent 1×9A5 refinement endpoints
* historical docking/refinement analyses
* relevant scripts and provenance

本 Task 011 的新结果原则上不要写入这个仓库。

---

## Target repository — all final results go here

```bash
/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization
```

GitHub：

`BioPpao/HRV-A89-2C-small-tag-and-insertion-site-prioritization`

这是本任务唯一的正式结果仓库。

所有：

* scripts
* TSV
* Markdown reports
* figures
* provenance
* candidate re-ranking
* PROJECT_STATE
* DECISIONS
* ANALYSIS_INDEX
* TODO
* task records

统一更新到这里。

---

# 2. Git 初始化和新 branch

先检查两个仓库：

```bash
git status
git remote -v
git branch -a
git log -10 --oneline --decorate
git fetch origin --prune
```

记录：

* repository
* local branch
* local HEAD
* origin branch
* origin HEAD
* commit SHA
* dirty/clean status

不要执行：

```bash
git reset --hard
git clean -fd
```

不要破坏用户任何未提交内容。

Target repo 优先以最新：

```text
origin/analysis/experimental-review-cleanup-010a
```

为 base。

创建：

```text
analysis/9a5-monomer-hexamer-context-011
```

如果 branch 已存在，先审计已有内容再继续，不覆盖已有分析。

如果 target worktree 有用户未提交修改且无法安全切 branch：

创建新的 git worktree，而不是覆盖/stash 用户文件。

最终结果仍必须 push 到：

```text
analysis/9a5-monomer-hexamer-context-011
```

不要 merge 到 main。

---

# 3. 科学问题

当前 small-tag 项目已经有一套 Priority A / Priority B / conflict-control / hard-negative 候选。

现在必须回答：

> 在真正考虑 9A5 与 2C 单体结合，以及 9A5 与 2C 六聚体结合以后，现有优先 tag 插入构建是否仍然合理？

这次不是重新从 320 junction 从零筛选。

而是新增：

```text
9A5-bound complex-context evidence layer
```

然后重新审查现有候选。

---

# 4. 必须同时分析两个结构状态

## Layer M

### 2C monomer + 9A5

评估 tag 插入对：

* 9A5 直接空间占位
* epitope geometry
* CDR–epitope interface
* tag exposure
* antibody accessibility

的影响。

---

## Layer H

### 2C hexamer + 9A5

进一步评估：

* tag ↔ 9A5
* tag ↔ adjacent protomer
* tag ↔ other protomers
* tag ↔ tag
* tag ↔ oligomer interface
* tag ↔ pore environment
* 9A5 ↔ neighboring tagged protomers

最终单体和六聚体必须独立报告，再综合判定。

不能简单平均成一个总分。

---

# 5. 已知已经存在的重要结构，但必须程序化验证

不要重新生成这些结构，除非验证后发现它们不可用。

## A. 1×9A5 + full-length 2C hexamer

优先检索：

```text
HRV_A89_2C_HEXAMER/results_summary/
SHOWCASE_1x_9A5_D_chain_after_npt_100ps_pbc_fixed.pdb
```

以及：

```text
selected_1x_9A5_weakposres_1ns_rep1_endpoint.pdb
selected_1x_9A5_weakposres_1ns_rep2_endpoint.pdb
selected_1x_9A5_weakposres_1ns_rep3_endpoint.pdb
```

预期：

```text
A–F = 2C
G/H = 9A5 VH/VL
```

但不要只根据文件名/旧报告假设。

程序化验证：

* chain sequence
* chain identity
* residue range
* atom count
* finite coordinates
* epitope contact
* PBC state

---

## B. Free full-length 2C hexamers

优先检索：

```text
selected_hexamer_01_md_representative.pdb
selected_hexamer_02_md_representative.pdb
```

以及：

```text
selected_hexamer_01_md_representative_5ns_rep1.pdb
selected_hexamer_01_md_representative_5ns_rep2.pdb
selected_hexamer_01_md_representative_5ns_rep3.pdb
```

不要重新构建 hexamer。

---

## C. 2C monomer/core + 9A5 existing complexes

优先检索：

```text
for_windows_download/current_candidate_structures/
07_C04_LEAD_9A5_2C_final30_complex.pdb

for_windows_download/current_candidate_structures/
08_C01_COMPARATOR_9A5_2C_final30_complex.pdb
```

并在整个：

```bash
/public/home/yukang/HRV_Oligomers
```

和 target repository 中继续搜索所有：

```text
*9A5*
*C01*
*C04*
*complex*
*monomer*
*Fv*
*scFv*
```

不要假设 C01/C04 是 full-length。

必须确定：

* 2C residue range
* 是否 1–321
* 是否 core fragment
* VH/VL identity
* pose orientation
* refinement history
* 是否存在比上述文件更新的 monomer–9A5 complex

如果服务器已经存在 full-length 2C monomer + 9A5 structure：

**直接使用。**

只有在确认不存在 full-length monomer complex，而且当前科学问题确实需要 full-length context 时，才允许从已有 9A5 complex 向 full-length monomer 做结构转移。

不要重新 blind docking。

---

# 6. 开始分析前必须建立一个完整的 existing-data inventory

生成至少：

```text
data/9a5_context_structure_inventory_v1.tsv
```

字段至少包含：

```text
source_repository
source_commit
absolute_path
relative_path
filename
sha256
structure_class
2c_state
2c_residue_range
n_2c_chains
antibody_present
antibody_type
VH_chain
VL_chain
refinement_state
registry_status
usable_for_primary_analysis
reason
```

`structure_class` 至少区分：

```text
2C_monomer
2C_core
free_hexamer
1x9A5_monomer_complex
1x9A5_core_complex
1x9A5_hexamer_complex
2x9A5_hexamer_complex
tagged_monomer
tagged_hexamer_proxy
ATP_Mg_state
```

同时生成 provenance：

```text
data/9a5_context_input_provenance_v1.tsv
```

---

# 7. 检索服务器已有计算资产

除了 Git tracked files，还必须阅读：

* PROJECT_INVENTORY
* STRUCTURE_REGISTRY
* PROJECT_STATE
* DECISIONS
* ANALYSIS_INDEX
* README
* reports
* scripts
* raw/server-only path records

在服务器上搜索项目明确引用的已有计算结果。

搜索时注意避免扫描整个 `/public`。

范围限定到：

```bash
/public/home/yukang/HRV_Oligomers
/public/home/yukang/wf/HRV-A89-2C-small-tag-and-insertion-site-prioritization
```

以及这两个项目文档明确引用的关联目录。

可以使用：

```bash
find
rg
grep
git log
git ls-files
```

但不要无差别扫描用户整个 home。

---

# 8. Target small-tag repository 全量审计

读取当前最新：

* candidate panel
* shortlist
* tagged structure outputs
* junction metrics
* functional map
* conservation
* homolog direct evidence
* EV-A71 evidence
* PLM/tag compatibility
* monomer structure results
* hexamer rigid-placement results
* binder accessibility
* MD results
* audit results

尤其确认所有当前：

* Priority A
* Priority B
* conflict controls
* hard-negative

不要依赖聊天中的历史列表。

必须从仓库实际最新 TSV 自动确定候选集合。

---

# 9. Monomer + 9A5 analysis

优先复用 existing 2C–9A5 complex。

对于每个 candidate tagged structure：

构建或读取：

```text
tagged 2C monomer + 9A5
```

如果 tagged monomer structure 已经存在：

直接复用。

不要重新 ColabFold。

如果需要将 9A5 pose 转移到 existing tagged monomer：

通过 native 2C residues 做 Kabsch/structural alignment。

不要按插入后的 residue numbering 直接粗暴对应。

明确识别：

```text
native 2C residue
inserted tag residue
```

---

## Monomer 层计算

### tag ↔ 9A5

分别计算：

```text
tag ↔ VH
tag ↔ VL
tag ↔ whole Fv
```

至少：

* minimum heavy-atom distance
* atom pairs <2.0 Å
* atom pairs <2.5 Å
* contacts ≤4.5 Å
* contacts ≤5.0 Å
* closest atoms/residues

### epitope preservation

使用项目正式 9A5 epitope 定义。

计算：

* epitope CA RMSD
* local backbone RMSD
* epitope SASA/rSASA
* CDR–epitope contacts
* minimum antibody–epitope distance
* key-interface contact preservation

### tag exposure

计算：

* tag SASA
* tag burial
* tag–native nonlocal contacts
* tag local crowding

输出：

```text
data/9a5_monomer_tag_compatibility_v1.tsv
```

---

# 10. Monomer pose sensitivity

如果 C01/C04 是两种仍有科学价值的 9A5 poses：

不要只选一个。

至少分析：

```text
Pose C01
Pose C04
```

如果只有一个 pose 与 full-length monomer / hexamer 几何兼容：

明确记录另一 pose 被排除的理由。

如果两个都合理：

报告：

* best case
* worst case
* median / range
* pose sensitivity

分类：

```text
POSE_ROBUST
POSE_SENSITIVE
POSE_CONFLICT
```

---

# 11. Hexamer + 9A5 analysis

主分析使用当前：

```text
1×9A5 + full-length 2C hexamer
```

以及 independent refinement endpoints。

不要重新 docking 9A5。

---

# 12. 关键原则：六聚体六个 2C protomer 都要带同一个 tag

实际 tagged 2C homohexamer 应建模为：

```text
A = tagged 2C
B = tagged 2C
C = tagged 2C
D = tagged 2C
E = tagged 2C
F = tagged 2C
```

而不是只把一个 tagged monomer 放进去。

对于每个 candidate，优先用已有 tagged monomer model，通过 native 2C residues 对齐到 A–F。

生成：

```text
6×tagged 2C + 1×9A5
```

结构 proxy。

不要为了这一层重新运行 AlphaFold multimer，除非现有数据完全不能解决问题。

---

# 13. Hexamer 层指标

对所有六个 tag 都计算：

### tag ↔ 9A5

* min heavy atom distance
* <2.0 Å clash pairs
* <2.5 Å clash pairs
* ≤4.5 Å contacts
* ≤5 Å contacts
* which protomer tag is closest

### tag ↔ other 2C protomers

* adjacent-protomer clash
* nonadjacent contacts
* minimum distance
* burial

### tag ↔ tag

检查六个 tag 之间：

* pairwise minimum distance
* hard clash
* crowding

### oligomer environment

* interface contact retention proxy
* local burial
* pore radial proxy if applicable
* gross ring geometry change only if structure was relaxed

输出：

```text
data/9a5_hexamer_tag_compatibility_v1.tsv
```

---

# 14. Ensemble first，不做单 snapshot 判断

优先利用已有：

## Free-hexamer ensemble

3 × 5 ns endpoints 或其他正式 repeat structures

## 1×9A5-bound ensemble

3 × 1 ns refined endpoints

对每个 candidate / metric 汇总：

* n structures
* min
* max
* median
* mean
* SD
* pass fraction
* conflict fraction

生成：

```text
data/9a5_context_ensemble_summary_v1.tsv
```

---

# 15. 2×9A5 只作为 stress test

现有 2×9A5 structures 如果 registry 为：

```text
NEGATIVE
AUDIT_ONLY
REJECTED
```

不得用于主正向 biological conclusion。

可以作为：

```text
high-occupancy spatial stress test
```

但必须与主结果分开。

不要因为 2×模型失败就宣布 tag 不可用。

---

# 16. ATP/Mg 暂不进入主分析

即使现成存在：

```text
1×9A5 + ATP/modelled Mg
```

也不要默认加入主 ranking。

本任务第一目标是：

```text
antibody context
```

而不是：

```text
antibody + nucleotide-state mechanism
```

除非某个结论只能通过现有 ATP/Mg matched state 解释，否则不扩展。

---

# 17. Candidate controls

必须包括：

## hard negative

当前正式 9A5 epitope-region hard-negative，例如 `155|156` construct。

如果 pipeline 完全不能识别该 construct 的 antibody-context risk：

优先检查算法错误。

## WT / untagged reconstruction control

重新使用 existing structures 验证 mapping pipeline 不会自己产生 artificial clash。

## free versus antibody-bound matched comparison

不要比较来自完全不同 source / numbering 的不匹配结构而不校正。

---

# 18. 不要只看“直接撞不撞抗体”

一个候选即使 tag 距 9A5 很远，也可能因为 insertion 导致：

* epitope geometry 改变
* local backbone rearrangement
* epitope exposure 改变
* protomer interface改变
* tag burial
* neighboring-protomer crowding

所以 final classification 必须结合：

```text
direct antibody sterics
+
epitope integrity
+
monomer context
+
hexamer context
+
ensemble reproducibility
```

---

# 19. Existing tag-binder accessibility 只作为已有辅助证据

不要把：

```text
9A5
```

和：

```text
anti-HA / anti-MAP8 / anti-G196 binder
```

混在一起。

本 Task 主问题是：

```text
tagged 2C ↔ 9A5 compatibility
```

已有 binder accessibility proxy 可以在 final integration 中保留。

如果没有成熟 binder complex structure：

不要重新大规模 docking。

继续标记：

```text
geometry/accessibility proxy only
```

---

# 20. 修复 9A5 feature field 一致性

检查 dedicated：

```text
nineA5_epitope_context
```

是否仍然被代码写成 outdated/unknown 状态。

如果存在：

修改 source-generation script。

不要手工编辑 TSV。

生成新版本 feature matrix。

必须明确区分：

```text
sequence-defined_9A5_epitope_context
```

与：

```text
3D_9A5_complex_context
```

---

# 21. 优先避免新计算

整个任务默认：

```text
NO NEW LONG MD
NO NEW BLIND DOCKING
NO NEW ALPHAFOLD
NO NEW COLABFOLD
NO MEMBRANE
NO RNA
```

只有当：

1. 所有现有数据检索完成；
2. 当前 Priority A/B 的关键结论仍无法判定；
3. 缺口不能通过已有结构转移/静态分析解决；

才考虑新增轻量计算。

---

# 22. 允许的最重补充计算

如果少数候选 rigid-placement 存在明显人工 clash，但无法判断是：

```text
real conflict
```

还是：

```text
unrelaxed geometry artifact
```

可以考虑：

* local minimization
* restrained minimization
* very short matched relaxation

必须有：

* WT matched control
* identical protocol
* complete QC

不要直接跑 50–100 ns。

---

# 23. Final integration

产生：

```text
data/final_candidate_panel_v6_9a5_context.tsv
```

不要覆盖旧版本。

字段至少包括：

```text
construct
junction
tag
previous_priority

monomer_9a5_class
monomer_pose_sensitivity
monomer_min_tag_ab_distance
monomer_clash_fraction
monomer_epitope_effect

hexamer_9a5_class
hexamer_tag_ab_clash
hexamer_tag_protomer_clash
hexamer_tag_tag_clash
hexamer_ensemble_consistency

existing_structural_class
existing_conservation_class
existing_homolog_evidence
existing_md_context
existing_binder_accessibility

complex_context_decision
new_priority
decision_reason
limitations
```

---

# 24. 不使用 opaque weighted score

不要把所有证据加权成一个无法解释的总分。

建议 classification：

```text
ROBUST_9A5_CONTEXT

MONOMER_CONTEXT_SENSITIVE

HEXAMER_CONTEXT_SENSITIVE

POSE_SENSITIVE

ANTIBODY_STERIC_CONFLICT

TAG_TAG_HEXAMER_CONFLICT

EPITOPE_PERTURBATION_RISK

STATE_DEPENDENT

INSUFFICIENT_EVIDENCE
```

最后再做 expert-evidence adjudication：

```text
retain Priority A
retain A with caution
A → B
B → A
move to control
remove from preferred set
```

不要为了“必须有变化”而重排。

原 ranking 如果经新分析后仍成立，也应明确作为结果。

---

# 25. 必须重点比较

最终报告必须专门回答：

```text
289|290
versus
248|249
```

在：

```text
monomer + 9A5
hexamer + 9A5
```

两个状态下谁更稳健。

同时回答：

* Priority B 有没有比 Priority A 更抗 9A5-context 的 construct
* 原 conflict controls 是否仍表现为 conflict
* hard negative 是否有效识别
* tag identity 是否改变同一 junction 的 antibody-context compatibility

---

# 26. 输出文档

至少：

```text
tasks/9A5_MONOMER_HEXAMER_CONTEXT_011.md

docs/9A5_MONOMER_CONTEXT_V1.md
docs/9A5_HEXAMER_CONTEXT_V1.md
docs/9A5_COMPLEX_CONTEXT_INTEGRATION_V1.md
```

主 integration report 必须开头就有：

```text
Executive conclusion
```

直接说最终候选变化。

---

# 27. Figures

根据真实数据生成至少：

1. candidate × structural state heatmap
2. monomer vs hexamer paired comparison
3. tag–9A5 clash/distance comparison
4. ensemble reproducibility
5. old priority → new priority
6. representative structures：

   * strongest retained candidate
   * candidate downgraded by antibody context
   * hard negative

如果所有 Priority A 都保留，也照实展示。

---

# 28. 项目状态更新

更新 target repo：

```text
PROJECT_STATE.md
DECISIONS.md
ANALYSIS_INDEX.md
TODO.md
README.md
active task pointer
provenance/evidence registry
```

只做必要更新，不重写历史。

---

# 29. Commit strategy

中途及时 commit，避免长任务结果丢失。

示例：

```text
task011: inventory existing 9A5 monomer and hexamer assets

task011: implement reused-data monomer antibody context analysis

task011: complete all-tagged 1x9A5 hexamer ensemble analysis

task011: integrate 9A5 context into candidate priorities

task011: finalize reports project state and QC
```

安全情况下及时 push。

---

# 30. “完成”的严格定义

以下情况都不算任务完成：

* “已经找到结构”
* “脚本已经写完”
* “建议下一步运行”
* “等待用户选择”
* “分析框架已经建立”
* “部分数据已经生成”

只有同时满足以下条件才允许结束：

1. 已完整检索两个项目已有数据；
2. 已确认 monomer–9A5 可用结构及其限制；
3. 已确认 1×9A5 full-length hexamer structures；
4. 已分析全部当前 Priority A/B/control；
5. 已完成 monomer + 9A5 layer；
6. 已完成 hexamer + 9A5 layer；
7. 已完成 ensemble summary；
8. 已形成新的 candidate decision；
9. 已生成 machine-readable TSV；
10. 已生成科学报告；
11. 已更新 target repo project state；
12. 已 commit；
13. 已 push GitHub；
14. 已确认服务器本地 branch 与 GitHub branch 一致。

---

# 31. 最终 Codex terminal response

最终回复必须直接提供结果。

## A. Repository

```text
source repo HEAD:
target base:
new branch:
final commit:
push:
working tree:
```

## B. Existing data reused

列出：

* monomer/core + 9A5 structures
* full-length monomer + 9A5 是否已有
* free hexamers
* 1×9A5 full-length hexamers
* repeat endpoints
* tagged monomer models
* existing analyses reused

并说明避免了哪些重复计算。

## C. Candidate result table

```text
construct
previous priority
monomer + 9A5
hexamer + 9A5
ensemble consistency
new priority
final decision
```

## D. Direct answer

明确回答：

> 当前有抗体存在时，哪些 tag insertion 仍然最合理？

以及：

> 如果现在必须下单做实验，推荐顺序是什么？

## E. Changes

哪些：

* retained
* promoted
* downgraded
* moved to control
* rejected

## F. Scientific limitations

必须明确哪些只是：

```text
structural proxy
```

而不是：

```text
biological proof
```

## G. Generated outputs

列出关键：

* TSV
* scripts
* docs
* figures

## H. Next work

只有真正仍未解决的问题才列为下一步。

如果本 Task 已足够回答 candidate prioritization：

明确写：

```text
No additional generic long MD is required for the current tag-prioritization decision.
```

---

最重要：充分利用两个项目已经完成的大量结构和计算资产。

**不要为了“做得更多”而重新计算已经存在的内容。**

本任务的评价标准是：

> 用最少必要的新计算，把现有 2C–9A5 单体结构、1×9A5–2C 六聚体结构和 small-tag candidate evidence 真正整合起来，最后得到可以直接指导实验构建选择的结果。
