# 数据说明

数据源：UCI Machine Learning Repository, Acute Inflammations（课程压缩包提供的教学划分）。共120条专家构造记录，并非已核实的独立临床患者。

- `train.csv`：72条带标签训练记录。
- `validation.csv`：24条带标签验证记录。
- `locked-test-features.csv`：24条测试特征。
- `locked-test-labels.csv`：教师提供的24条测试标签，仅用于固定教学测试复现。

模型输入字段：`fever_ge_38`, `nausea`, `lumbar_pain`, `urine_pushing`, `micturition_pain`, `burning_urethra`，均为0/1；目标字段 `bladder_inflammation` 为0/1。`temperature_c` 不直接进入模型；`nephritis` 不作为输入。`sample_id` 仅用于记录匹配。

数据来自用户上传的第七课压缩包，保留原始课程划分，未对原始数据重新随机划分。使用与再分发时请核对 UCI 原始数据集的署名和许可要求。
