# Live-Tutor — 自适应私人教师 v1.6.1

> 基于 Claude Code Skill 的智能学习系统，支持 Markdown/PDF/PPT/AI 生成四种输入源。

[![Version](https://img.shields.io/badge/version-1.6.1-blue)](SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 功能

- **四入口**：上传教材 PDF/PPT/Markdown，或仅输入科目名由 AI 生成全部内容
- **自适应等级**：L1（基础）→ L2（巩固）→ L3（提升）→ L4（全面），按章独立跟踪
- **单文件双 Tab**：学习手册 + 章节小测合并为单个 HTML，MathJax + Mermaid 渲染
- **JS 自动评卷**：MCQ 即时评分 + 简答大模型评判，剪贴板 + 文件下载双通道回传
- **IP 角色语音**：懒羊羊/哪吒/小小怪下士/灰太狼四种教学风格
- **SM-2 间隔复习**：基于艾宾浩斯遗忘曲线的知识点追踪

## 架构

```
live-tutor/
├── SKILL.md                    # 工作流骨架（6步 + 2插入点）
├── iron-rules.md               # 52条铁律规则 + 29条反模式
├── persona.md                  # 5种Persona教学风格
├── character-voices.md         # 4种IP角色语音系统
├── extraction.md               # 内容获取管线（4路径路由）
├── progress_schema.json        # 进度数据结构 JSON Schema
├── progress_template.json      # 进度初始化模板
├── agents/                     # Agent调度层
│   ├── tutor_agent.md          # 学习手册生成 + 小测出题
│   ├── assess_agent.md         # 测评 + 评卷
│   └── exam_agent.md           # 最终综合检测
├── templates/                  # 输出模板
│   ├── learning-manual.md      # 学习手册（六段式 + HTML质量准则）
│   ├── quiz.md                 # 测验模板
│   ├── error-collection.md     # 错题集
│   └── pre-exam-memo.md        # 考前备忘录
├── scripts/
│   └── review_calc.py          # SM-2间隔复习计算工具
└── books/                      # 教材源文件（Markdown）
```

## 快速开始

1. 在 Claude Code 中加载 skill
2. 输入触发词：`live-tutor`、`私人教师`、`备考`、`帮我复习`
3. 选择内容来源：[A] 上传教材 / [B] AI 直接生成 / [C] 课程库
4. 选择 Persona + IP 角色 + 渲染模式
5. 开始自适应学习

## 版本演进

| 版本 | 日期 | 核心主题 |
|------|------|---------|
| v1.6.1 | 2026-07-14 | 单文件双 Tab + 质量体系完善 + HTML 全流程覆盖 |
| v1.6 | 2026-07-13 | Markdown 输入源 + 路径 M 提取管线 |
| v1.5.1 | 2026-07-07 | ISBN/教材信息精准匹配 |
| v1.5 | 2026-07-07 | 无 PDF 启动：三入口架构 |
| v1.4 | 2026-07-06 | IP 角色语音系统 |
| v1.3 | 2026-07-06 | SM-2 间隔复习系统 |
| v1.2 | 2026-07-04 | 模块化重构 + 按章定级 |
| v1.1 | — | Persona 五人格系统 |
| v1.0 | — | 六步工作流 + 四级自适应 |

详见 [CHANGELOG.md](CHANGELOG.md)