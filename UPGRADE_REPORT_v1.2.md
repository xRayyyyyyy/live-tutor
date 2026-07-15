# Live-Tutor v1.2 提升报告

> 升级日期：2026-07-04
> 版本：v1.1.0 → v1.2.0
> 修改范围：14 个文件（5 个重写 + 8 个新建 + 1 个迁移工具）

---

## 一、变更概览

| 指标 | v1.1 | v1.2 | 变化 |
|------|------|------|------|
| SKILL.md 行数 | 654 | 379 | **↓42%** |
| 文件数（不含 output） | 6 | 14 | +8 |
| 总代码行数 | ~1,200 | 1,886 | +57%（功能显著增加） |
| Agent 定义数 | 3（死代码） | 3（活跃调度） | 全部重写 |
| 模板文件数 | 0 | 4 | 新增 |
| JSON Schema | 无 | 有 | 新增 |
| 迁移工具 | 无 | 有 | 新增 |

---

## 二、12 项优化详细报告

### ✅ 1. SKILL.md 模块化拆分

**问题**：v1.1 的 SKILL.md 是一个 654 行的单文件，每次加载消耗大量 context window。

**解决方案**：将 SKILL.md 精简为 379 行的工作流骨架，抽取为 7 个独立模块文件：

| 新文件 | 行数 | 内容 |
|--------|------|------|
| `persona.md` | 100 | Persona A-E 定义、行为矩阵、切换机制 |
| `iron-rules.md` | 79 | 铁律规则 + 12 条反模式 |
| `extraction.md` | 44 | PDF/PPT 内容提取管线 |
| `templates/learning-manual.md` | 146 | 学习手册输出模板 |
| `templates/quiz.md` | 174 | 四类测验模板 |
| `templates/error-collection.md` | 49 | 错题集模板 |
| `templates/pre-exam-memo.md` | 64 | 考前备忘录模板 |

**效果**：SKILL.md 每次加载只需 379 行 context，其余文件按需引用。

---

### ✅ 2. Agent 定义激活

**问题**：v1.1 的 3 个 agent 文件存在但未被 SKILL.md 调度，属于死代码。

**解决方案**：
- SKILL.md 工作流中明确标注每个 Step 调用哪个 Agent（共 4 处调度点）
- 每个 Agent 文件头部增加 `Dispatch point` 字段，标明被哪个 Step 调用
- `assess_agent.md` 从 2 种模式扩展为 4 种模式（摸底/章节小测/微测试/章节预检）
- `tutor_agent.md` 新增错误注入、视觉辅助插入逻辑
- `exam_agent.md` 新增 WebSearch 过滤规则和错题改编逻辑

---

### ✅ 3. progress.json Schema 统一

**问题**：v1.1 的 `progress_template.json` 与实际产出字段不一致（缺少 persona、current_mode 等）。

**解决方案**：
- 新增 `progress_schema.json`（206 行，JSON Schema Draft-07）
- 定义了全部 required 字段、enum 约束、嵌套对象结构
- `progress_template.json` 重写以匹配 schema
- 提供 `migrate_v11_to_v12.py` 迁移脚本，自动升级旧数据

**验证结果**：
- ✅ template 包含所有 required 字段
- ✅ 迁移后的 `随机信号分析/progress.json` 完全符合 v1.2 schema

---

### ✅ 4. 跨会话恢复机制

**问题**：v1.1 用户关闭会话后无法恢复学习进度。

**解决方案**：
- Step 0 增加「进度恢复」分支
- 启动时检查 `output/{科目}/progress.json` 是否存在
- 提供三个选项：继续上次进度 / 重新开始 / 换科目
- 展示进度摘要（已完成章节数、当前等级、上次学习日期）

---

### ✅ 5. 按章调整等级系统

**问题**：v1.1 使用全局 current_level，无法反映学生在不同章节的差异。

**解决方案**：
- 移除全局 `current_level` 和 `current_mode`
- 每个 chapter 对象新增 `current_level` 和 `precheck_level` 字段
- 新增 Step 2.5（章节预检）：每章开始前用 2-3 道快速题判定起始等级
- 评分规则：全对→L3/L4、对2/3→L2、对0-1/3→L1
- `tutor_agent.md` 中等级过滤改为读取 `per_chapter_level`

---

### ✅ 6. 错题间隔复习机制

**问题**：v1.1 错题集生成后从未被引用，学习闭环断裂。

**解决方案**（三处联动）：
1. **重学注入**：Step 3 生成手册时，读取本章错题集，插入「⚠️ 上次易错点」专栏
2. **复习计划**：错题集模板新增「📅 复习建议」段（1天/3天/考前 三轮复习）
3. **最终检测加权**：exam_agent 从各章错题集中抽取 20-30% 改编纳入最终考试
4. **数据结构**：`progress.json` 新增 `error_review_schedule` 数组跟踪复习进度

---

### ✅ 7. Persona 切换

**问题**：v1.1 规则 R-PERSONA-4 禁止中途切换 Persona，过于僵化。

**解决方案**：
- 修订 R-PERSONA-4：允许在章节间切换，章节内不可切换
- `persona.md` 新增「🔄 Persona 切换机制」段
- 章节间选择"继续下一章"时，额外提供切换选项
- `progress.json` 新增 `persona_history` 数组记录切换历史（含原因）

---

### ✅ 8. 快速/深度双模摸底

**问题**：v1.1 深度摸底需扫描全书，token 消耗大，启动慢。

**解决方案**：
- Step 1 新增双模选择
- **快速摸底**：5 道概念题，仅基于目录标题，约 5 分钟
- **深度摸底**：保持 v1.1 方案（8-10 题全书扫描）
- `assess_agent.md` 新增 Mode 1 的快速子流程
- `templates/quiz.md` 新增快速摸底输出模板
- `progress.json` 的 `diagnostic.mode` 记录所选模式

---

### ✅ 9. 考前备忘录

**问题**：v1.1 缺少全书知识汇总，学生考前没有速查工具。

**解决方案**：
- 新增 Step 5.5（考前备忘录）
- `templates/pre-exam-memo.md` 定义输出模板
- 内容包含：
  - 全书必背公式一览（按章汇总 ⭐⭐⭐ 公式）
  - 高频错题 TOP N（从各章错题集筛选）
  - 易混淆概念对比表
  - 各章学习轨迹可视化
  - 个性化考试策略建议

---

### ✅ 10. 视觉辅助

**问题**：v1.1 学习手册纯文字+公式，缺少图形化辅助。

**解决方案**：
- `templates/learning-manual.md` 新增「🔄 可视化辅助」段
- 支持 5 种图表类型：

| 场景 | 图表类型 |
|------|---------|
| 概念关系（蕴含/等价/对比） | Mermaid graph LR |
| 推导链条 ≥ 3 步 | Mermaid flowchart TD |
| 信号/函数形状 | ASCII 波形图 |
| 状态转移 | Mermaid stateDiagram |
| 分类层次 | ASCII 树状图 |

- 规则：每章最多 3-5 个图表，Mermaid 不可用时回退 ASCII

---

### ✅ 11. WebSearch 过滤规则

**问题**：v1.1 搜索试卷质量不可控，可能纳入无关或超纲题目。

**解决方案**：
- `templates/quiz.md` 和 `exam_agent.md` 新增 6 条过滤规则：
  1. 域名优先（`.edu.cn`、`.edu`）
  2. 格式优先（PDF）
  3. 时效性（近 5 年）
  4. 关键词匹配（科目全称）
  5. **知识点比对校验**（超纲题目排除）
  6. 回退策略（有效结果 < 3 条时回退到自生成）
- 搜索查询模板使用 `site:edu.cn` 和 `filetype:pdf` 限定

---

### ✅ 12. 微测试功能

**问题**：v1.1 从学习手册到章节小测之间缺少即时反馈环节。

**解决方案**：
- Step 4（用户自学）中新增可选微测试入口
- 每个小节结束后可做 1-2 道快速题
- `assess_agent.md` 新增 Mode 3（Micro-Quiz）
- `templates/quiz.md` 新增微测试输出模板
- **核心约束**：不计入等级评定，仅提供即时反馈
- `progress.json` 中 history 条目新增 `micro_quizzes` 数组记录

---

## 三、新增文件结构

```
live-tutor/
├── SKILL.md                        # 工作流骨架（379 行，↓42%）
├── persona.md                      # 🆕 Persona 系统 + 切换机制
├── iron-rules.md                   # 🆕 铁律规则 + 反模式
├── extraction.md                   # 🆕 内容提取管线
├── progress_schema.json            # 🆕 JSON Schema (Draft-07)
├── progress_template.json          # ✏️ 重写 (v1.2 schema)
├── migrate_v11_to_v12.py           # 🆕 v1.1→v1.2 迁移工具
├── agents/
│   ├── tutor_agent.md              # ✏️ 重写 (active dispatch + error injection + visuals)
│   ├── assess_agent.md             # ✏️ 重写 (4 modes: 摸底/小测/微测试/预检)
│   └── exam_agent.md               # ✏️ 重写 (filtering + error adaptation)
├── templates/                      # 🆕 新建目录
│   ├── learning-manual.md          # 🆕 学习手册模板
│   ├── quiz.md                     # 🆕 测验模板（4 类）
│   ├── error-collection.md         # 🆕 错题集模板
│   └── pre-exam-memo.md            # 🆕 考前备忘录模板
└── output/
    └── {教材名}/
        ├── progress.json
        ├── *.v11.bak               # 迁移自动备份
        └── ...
```

---

## 四、微测试结果

| 测试项 | 结果 |
|--------|------|
| 文件结构完整性（14 个文件全部存在） | ✅ PASS |
| 交叉引用一致性（所有引用文件均存在） | ✅ PASS |
| JSON Schema 与 Template 匹配 | ✅ PASS |
| JSON Schema 与迁移后数据匹配 | ✅ PASS |
| SKILL.md 行数缩减 | ✅ PASS（654→379，↓42%） |
| Agent 调度点明确标注 | ✅ PASS（4 处调度点） |
| 12 项优化全部覆盖 | ✅ PASS（grep 验证每项均有代码引用） |
| v1.1 数据迁移成功 | ✅ PASS（随机信号分析 progress.json 已迁移） |
| Symlink 完好 | ✅ PASS |

---

## 五、已知限制与后续建议

1. **Schema 校验未运行时执行**：当前 `progress.json` 的写入依赖 LLM 自觉遵守 schema，建议在 progress 更新流程中嵌入 JSON Schema 校验步骤
2. **Mermaid 渲染依赖前端**：Mermaid 图表在纯终端中无法渲染，已提供 ASCII 回退方案
3. **间隔复习提醒**：`error_review_schedule` 目前仅记录计划，暂无主动提醒机制（需要外部 cron 或手动检查）
4. **多科目并行**：当前每个科目独立管理，尚未实现跨科目学习分析
