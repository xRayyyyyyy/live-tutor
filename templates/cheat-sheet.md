# 速查表模板

## 输出格式

### Markdown 模式

```markdown
# 📄 速查表 — {topic}

> ⏱️ 5 分钟快速复习 | 生成日期：{date}

---

## 📌 一句话定义

{topic} 是：{用通俗语言给出的一句话定义}

---

## 🔑 核心概念

| 概念 | 定义 | 关键点 |
|------|------|--------|
| {概念1} | {definition} | {key_point} |
| {概念2} | {definition} | {key_point} |
| ... | ... | ... |

---

## 📐 关键公式/规则（如适用）

| 公式/规则 | 含义 | 使用场景 |
|-----------|------|---------|
| $formula_1$ | {meaning} | {when_to_use} |
| $formula_2$ | {meaning} | {when_to_use} |

---

## 💡 3-5 个具体例子

**例1**：{real_world_example_1}

**例2**：{real_world_example_2}

**例3**：{real_world_example_3}

---

## ⚠️ 常见误区

| 误区 | 正确理解 |
|------|---------|
| {misconception1} | {correct_understanding1} |
| {misconception2} | {correct_understanding2} |

---

## ✅ 使用前检查清单

- [ ] 我理解 {concept_A} 的含义
- [ ] 我能区分 {concept_A} 和 {concept_B}
- [ ] 我知道 {formula} 的适用条件
- [ ] 我能举出一个实际应用的例子

---

## ❓ 快速记忆检验（5 题）

1. {question1}
2. {question2}
3. {question3}
4. {question4}
5. {question5}

<details>
<summary>答案</summary>

1. {answer1}
2. {answer2}
3. {answer3}
4. {answer4}
5. {answer5}

</details>
```

### HTML 模式

HTML 模式下，速查表输出为完整 HTML5 文档：

- 暗色主题，单页布局（适合打印或截图保存）
- 公式用 MathJax 渲染
- 答案区默认折叠（点击展开）
- 检查清单为可交互 checkbox
- 生成后 `open` 自动打开

文件命名：`速查表_{主题名}.{md|html}`

## 设计原则

1. **5分钟可读完**：严格控制信息密度，不放长篇解释
2. **结构优先**：用表格和列表代替段落文字
3. **通俗语言**：避免术语堆砌，用日常语言解释核心概念
4. **可独立使用**：每张速查表可脱离上下文独立理解
5. **公式精简**：只保留最关键的公式，附带使用场景说明
