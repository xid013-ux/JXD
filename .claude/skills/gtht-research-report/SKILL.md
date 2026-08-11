---
name: gtht-research-report
description: GTHT内部研究报告 —— 按国泰海通投行内部研究报告的体例撰写行业/产业链/公司研究报告（Word 正文 + Excel 图表数据底稿 + 数据来源清单 + 研究提纲memo）。当用户要求写行业研究、产业链研究、拜访前研究、公司尽调材料、投行内部研究报告，或要求"按我们部门/老板的格式"出研究报告时使用。
---

# GTHT 内部研究报告

## 这个 skill 是什么

把国泰海通投行内部研究报告的**体例、文风、取数纪律和排版参数**固化下来，
使每次产出的报告不需要再经过多轮返工就能贴近领导定稿版本。

规范来源：领导对《中国人形机器人产业链研究》定稿版的实际修改（2026-08）。
以下所有规则都是从他"改了什么、删了什么"里反推出来的，不是凭空设计的模板。

## 什么时候用

- 行业研究 / 产业链研究 / 赛道扫描
- 拜访前的标的研究、公司尽调材料
- 资本化进度盘点、券商关联关系梳理
- 任何用户说"按上次那个格式""按部门模板"写的研究报告

## 最先要记住的五条

领导改稿的取向高度一致，先记住这五条，能避掉 80% 的返工：

1. **给事实，不给判断。** 不写"小结""启示""特征归纳"这类由作者推论出来的段落。
   判断留在口头汇报，不落纸。
2. **拿不准的不写。** 不用"待核实""建议复核""或有"这类标注 —— 核实不了就整条删掉，
   不给读者留半成品。
3. **不留内部痕迹。** 正文里不出现"本次拜访""对我司的意义""可对接的客户资源"
   这类内部语。拜访关注点集中写在最后的专章，不散落在行业章节里。
4. **人和公司比交易参数重要。** 履历、组织、产品线这类硬事实优先；
   发行价、市盈率、战略配售明细这类交易参数除非题目就是它，否则不占篇幅。
5. **用词跟他的习惯走。** 例如数据来源写"Wind 金融数据库整理成果"，不要自作主张
   改成"Wind 数据库"；哪怕读着略拗口也不动。

详细规则见 `references/写作规范.md`，**动笔前必读**。

## 工作流程

### 第 0 步：先出提纲 memo，等确认

不要直接开写。先产出一份**写作前的研究提纲**（≤2 页、纯文字、不要表格），
说明：研究问题、章节划分、每章打算解决什么、数据分几类、大致从哪些渠道取、时间安排。
数据来源只写类别和渠道，不要逐条列。这份是给领导看"工作方式和节奏对不对"的，
不是给报告做说明的。确认后再写正文。

### 第 1 步：搭骨架

沿用 `references/报告结构.md` 里的九章骨架，按题目增删。
标题层级只用两级：`一、`（自动编号）+ `1.1`（手写编号）。

### 第 2 步：取数与写作

- 每一个观点、每一个数字都要有出处，见 `references/数据与来源规范.md`
- 口径不同的数据**并列呈现，绝不平均、绝不合并**
- 边写边把数据落进 Excel 底稿，不要最后补

### 第 3 步：构建交付物

用 `assets/` 里的代码生成 Word（见下），Excel 底稿和来源清单用 openpyxl。
排版参数见 `references/排版规范.md`。

### 第 4 步：自检

```bash
python3 .claude/skills/gtht-research-report/scripts/check_report.py <报告.docx>
```

再人工过一遍 `references/写作规范.md` 末尾的定稿检查清单。

### 第 5 步：交付

四份文件：正文 Word、图表数据底稿 Excel、数据来源清单 Excel、研究提纲 memo。
用户可能只要其中一部分，按要求给。见 `references/交付物与IBD.md`。

## 用 assets/ 生成 Word

`assets/` 里是已经跑通的构建代码，直接复用，不要从零写 python-docx：

- `报告模板.docx` —— 样式载体（Heading 2/3、Normal Indent、表格后说明、TOC 样式全在里面）
- `_helpers.py` —— 导入即得一个清空正文、保留样式和页面设置的 `doc`，
  并提供 `title/h2/h3/para/note/table/figure/blank/make_toc`
- `_fixup.py` —— **必须最后 import**，做 OOXML 子元素顺序修正并保存

```python
import sys, os
SK = '.claude/skills/gtht-research-report/assets'
sys.path.insert(0, SK)
os.environ['DOCX_OUT'] = 'output/报告.docx'
os.environ['DOCX_CHARTS'] = 'output/charts'   # figure() 从这里取图
from _helpers import *

title('中国 XX 产业链研究')
h2('产业概述')
h3('1.1 行业简介')
para('正文段落……')
table(headers=['公司','环节','主营业务情况'],
      rows=[['A','谐波减速器','……']],
      widths=[20, 20, 60],
      caption='表1：XX 一览',
      source='数据来源：Wind 金融数据库整理成果，国泰海通投资银行部整理',
      aligns=['center','center','left'])
figure('fig1.png', '图1：XX 趋势', '数据来源：……')

make_toc(doc)      # 目录必须在正文全部写完后再生成
import _fixup      # 保存在这里发生
```

**关键约束**

- `make_toc(doc)` 一定在所有 `h2/h3` 之后调用，它靠 `HEADINGS` 列表生成目录项
- `import _fixup` 一定是最后一行；缺它会 XSD 校验失败（子元素顺序违规）
- 不要手动往 `pPr`/`tblPr` 里 append 元素后就直接保存，顺序必须过 `_fixup`
- 校验：`python3 /mnt/skills/public/docx/scripts/office/validate.py <file>`

环境不确定时先跑冒烟测试，确认工具链可用：

```bash
python3 .claude/skills/gtht-research-report/scripts/smoke_test.py /tmp/smoke
```

## 已知环境限制（要如实告诉用户，不要假装做到了）

- LibreOffice 在本环境无法加载 docx，**无法渲染 PDF、无法核对页数和视觉效果**
- 外部下载常被拦截，**招股书/年报等原始文件往往打不包**，只能给带 URL 的来源清单
- **IBD Tools 是用户机器上的 Word 加载项，我这边调用不了**；
  做法是产出"插件友好"的文件让用户在 Word 里一键美化，见 `references/交付物与IBD.md`

## 参考文件

| 文件 | 内容 |
|---|---|
| `references/写作规范.md` | 领导的编辑取向、文风、禁忌、定稿检查清单 **（必读）** |
| `references/报告结构.md` | 九章骨架、各章该写什么、目录体例 |
| `references/排版规范.md` | 字体字号、页面、表格、图、来源注、目录的全部参数 |
| `references/数据与来源规范.md` | 取数纪律、口径处理、来源标注写法、复核流程 |
| `references/交付物与IBD.md` | 四份交付物的规格、Excel 体例、IBD Tools 衔接 |
