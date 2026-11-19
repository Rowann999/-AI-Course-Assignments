# 同伴复现记录（待实际完成）

复现者：
复现日期：
操作系统 / Python版本：
运行命令：`python -m pip install -r requirements.txt`，`python src/naive_bayes.py`
能否生成 `outputs/metrics.json`：
核对指标：
遇到的问题：
修改与对应 Git commit：

> 此文件是记录模板，不能代替真实的同伴复现。

## 个人复现记录（Self-Reproduction）

**复现日期：** 2026年11月19日

**复现方式：** 在本地 VS Code 中，使用 Anaconda Python 环境运行 GitHub 项目的分析程序。

**运行环境：**
- 操作系统：Windows
- Python 环境：Anaconda（E:\Anaconda3）
- 开发工具：Visual Studio Code
- Python 具体版本：3.14.6

**运行命令：**

`python src/naive_bayes.py`

**复现结果：**

成功运行分析程序，并获得以下结果：

- 训练集、验证集和测试集样本数分别为72、24和24。
- 分类阈值为0.5。
- 验证集 Accuracy = 1.000，Log loss = 0.0872。
- 测试集 Accuracy = 1.000，Log loss = 0.0745。
- 固定查询样本的阳性预测概率为0.986576。
- 将腰痛特征额外复制5次后，验证集 Accuracy 下降至0.750，Log loss 上升至0.3854。

**复现结论：**

本次个人复现成功。程序生成的主要评价指标与课程 Worksheet 中的报告结果一致，说明该项目在当前本地环境下具有可重复运行性。

**研究局限：**

本次复现使用的是同一份课程数据及预先确定的数据划分，属于已有结果的重复验证，不能视为独立外部数据验证。由于数据规模较小且具有教学数据特征，模型的临床泛化能力仍需进一步评估。

**同伴复现状态：**

尚未开展。后续将邀请其他同学在独立环境中按照 README 运行程序，并记录实际结果及遇到的问题。