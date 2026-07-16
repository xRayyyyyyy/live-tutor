# 合并速查表模板

## 触发时机

每 3 个 session 完成边界探测后自动生成，将本轮 3 个 session 的内容压缩为一张速查表。

## 输出格式

### Markdown 模式

```markdown
# 📄 合并速查表 — Session {N}-{M}

> 本轮探测级别：Level {current}
> 生成日期：{date}

---

## Session {N}: {标题}

**一句话总结**：{one_liner}

### 核心概念
| 概念 | 定义 | 关键公式/关系 |
|------|------|-------------|
| {concept1} | {definition} | {formula} |
| {concept2} | {definition} | {formula} |

### 核心"为什么"
| 问题 | 原理回答 |
|------|---------|
| {why_question1} | {answer1} |

---

## Session {N+1}: {标题}

（同上结构）

---

## Session {N+2}: {标题}

（同上结构）

---

## 🔴 本轮探测薄弱点（重点复习）

| 概念 | 探测得分 | 补漏状态 | 复习建议 |
|------|---------|---------|---------|
| {weak1} | {score}/10 | {已补漏/未补} | {suggestion} |
| {weak2} | {score}/10 | {已补漏/未补} | {suggestion} |

---

## ❓ 综合检验（5 题，跨 Session）

1. {cross_session_question1}
2. {cross_session_question2}
3. {cross_session_question3}
4. {cross_session_question4}
5. {cross_session_question5}

<details>
<summary>📝 点击查看答案</summary>
1. {answer1}
...
</details>
```

### HTML 模式

HTML 模式下，合并速查表输出为完整 HTML5 文档：

- 暗色主题（与学习手册一致）
- 3 个 session 以卡片式布局展示，每个卡片含核心概念表 + "为什么"表
- 薄弱点区域红色高亮
- 综合检验题带折叠答案
- MathJax 公式渲染
- 生成后 `open` 自动打开

文件命名：`合并速查表_Session{N}-{M}.{md|html}`

## 设计原则

1. **压缩而非复制**：不是把 3 张速查表拼在一起，而是提炼每个 session 最重要的 3-5 个概念
2. **跨 session 连接**：综合检验题必须跨越多个 session 的知识点
3. **薄弱点突出**：探测中暴露的薄弱概念用红色高亮，附带复习建议
4. **10 分钟可复习**：整张合并速查表可在 10 分钟内快速过一遍
