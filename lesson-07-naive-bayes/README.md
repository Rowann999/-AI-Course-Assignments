# Lesson 07 — 六症状朴素贝叶斯分类的构建与评价

## 研究问题

基于六项二元症状，Bernoulli 朴素贝叶斯能否预测教学数据中的膀胱炎症标签？高准确率是否意味着概率可靠、能够推广到新患者？

## 数据与方法

使用 UCI Acute Inflammations 的120条专家构造记录，沿用课程提供的固定划分：训练72条、验证24条、测试24条。模型为 `BernoulliNB(alpha=1)`，先验与症状条件概率仅在训练集估计。验证集按照“敏感度≥0.90 → 特异度最大 → 阈值最接近0.5（再并列取较小值）”选阈值。

六项输入为发热（体温≥38℃）、恶心、腰痛、尿急、排尿痛、尿道灼痛；预测标签为 `bladder_inflammation`。

## 文件结构

```text
lesson-07-naive-bayes/
├── README.md
├── requirements.txt
├── pbl/student-worksheet.md
├── data/                 # 课程原始划分及数据说明
├── notebooks/naive_bayes_analysis.ipynb
├── src/naive_bayes.py
├── outputs/              # 程序生成的图表、CSV、JSON
└── report/bys.docx       # 已完成的课程 Worksheet
```

## 如何复现（Python 3.10+）

在本项目根目录运行：

```bash
python -m pip install -r requirements.txt
python src/naive_bayes.py
```

若希望交互式查看：

```bash
jupyter notebook notebooks/naive_bayes_analysis.ipynb
```

按顺序运行 Notebook 的所有单元格。运行后 `outputs/` 中将生成 `metrics.json`、`threshold_grid.csv`、`duplicate_feature.csv`、`validation_predictions.csv`、`test_predictions.csv` 和 `validation_confusion_matrix.png`。

## 结果与证据链

- 数据定义：`data/README.md` 与 `data/*.csv`
- 模型训练、阈值选择、评价：`src/naive_bayes.py`
- 逐条预测：`outputs/validation_predictions.csv` 和 `outputs/test_predictions.csv`
- 汇总指标：`outputs/metrics.json`
- 可视化：`outputs/validation_confusion_matrix.png`
- 研究解释：`report/bys.docx`

关键核对目标（来自课程报告）：验证与测试 accuracy 均为1.000；验证 log loss≈0.0872、测试≈0.0745；固定查询 `x=(0,0,0,1,1,1)` 的阳性概率≈0.986576；额外复制腰痛5次后验证 accuracy≈0.750、log loss≈0.3854。**以实际运行输出为准**。

## 局限与复现边界

这是专家构造的教学数据，不能作为真实临床诊断效能的证明。验证和测试数据的二元输入组合与训练集存在重复，无法充分检验未见症状组合的泛化。教师测试标签已经包含在课程资料中，本仓库属于固定教学测试的结果复现，不宣称独立外部验证。

## 版本历史与同伴复现

按照真实进展分阶段提交：目录与数据 → 代码及可运行结果 → 复现反馈与修正。请将实际尝试、失败原因和下一步写入 `reflection.md`，并在 `reproduction.md` 中记录同伴真实的运行环境、反馈和修订；不要虚构复现经历。

## 来源

- UCI Machine Learning Repository: [Acute Inflammations](https://archive.ics.uci.edu/dataset/184/acute+inflammations)
- 课程材料：`pbl/student-worksheet.md`
