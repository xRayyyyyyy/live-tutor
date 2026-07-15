# Live-Tutor 更新换代日志

> 自适应私人教师 — 从基础工作流到 SM-2 间隔复习 + IP 角色语音的演进之路

---

## 版本总览

| 版本 | 日期 | 核心主题 | 文件数 | SKILL.md 行数 |
|------|------|---------|--------|---------------|
| **v1.6.1** | 2026-07-14 | 单文件双 Tab + 质量体系完善 + HTML 全流程覆盖 | 17 | ~600 |
| **v1.6** | 2026-07-13 | Markdown 输入源 + 路径 M 提取管线 | 17 | ~580 |
| **v1.5.1** | 2026-07-07 | ISBN/教材信息精准匹配：公开目录提取 + AI 填充 | 17 | ~570 |
| **v1.5** | 2026-07-07 | 方案 C：无 PDF 启动 + AI 内容生成 + 三入口架构 | 17 | ~550 |
| **v1.4** | 2026-07-06 | IP 角色语音系统 + 渲染模式选择 | 17 | ~498 |
| **v1.3** | 2026-07-06 | SM-2 间隔复习系统 | 16 | ~470 |
| **v1.2** | 2026-07-04 | 架构重构：模块化 + 按章定级 + 双模摸底 | 14 | 379 |
| **v1.1** | — | Persona 五人格系统 | 6 | 654 |
| **v1.0** | — | 初始版本：六步工作流 + 四级自适应 | ~4 | ~500 |

---

## v1.6.1 — 单文件双 Tab + 质量体系完善（2026-07-14）

### 🎯 问题

v1.6 的测验生成为独立 HTML 文件（学习手册 + 章节小测两个 Tab），存在：① 双文件知识点不一致风险 ② 输出文件命名规则仅覆盖 `.md` ③ 最终检测/错题集/备忘录无 HTML 输出规范。

### 🆕 方案

**单文件双 Tab 架构**：学习手册 + 章节小测合并为单个 HTML 文件，通过 JS `switchTab()` 切换。整理沉淀质量体系（R-CON-6/7、MathJax/Mermaid 兼容规则）。

### 改动摘要

| 文件 | 改动 |
|------|------|
| `SKILL.md` | Step 3 重写为单文件双 Tab + 实现要点（JS 切换/MathJax 兼容/Mermaid 兼容/质量铁律）<br>Step 5.5/6 新增 HTML 输出规范<br>HTML 规范从 8 条扩展为 9 条<br>版本 v1.6.0 → v1.6.1 |
| `iron-rules.md` | +R-CON-6（逐知识点展开）<br>+R-CON-7（单文件不压缩质量）<br>+R-SRC-9（图片嵌入）<br>R-FILE-1~7 全部更新为 `{md|html}` 扩展名 |
| `templates/learning-manual.md` | +HTML 版质量准则 8 条 |
| `templates/error-collection.md` | +HTML 模式规范 |
| `templates/pre-exam-memo.md` | +HTML 模式规范 |
| `agents/tutor_agent.md` | +Quiz Generation section（出题规则/遮罩层/文件输出） |
| `agents/assess_agent.md` | Mode 2 更新为"评卷+错题集"，移除出题职责 |
| `extraction.md` | +M.7 图片处理规范 |
| `CHANGELOG.md` | 本条目 |

### 质量体系

| 规则 | 内容 |
|------|------|
| R-CON-6 | 每个 ⭐⭐⭐ 独立 h3 + 公式块 + blockquote，不得压缩 |
| R-CON-7 | 单文件模式先保证手册质量再叠加小测，500+ 行可接受 |
| MathJax 兼容 | blockquote 内禁 `<br>` + `$` 混用，每行独立 `<p>` |
| Mermaid 兼容 | 手册 Tab 加 `style="display:block"`，JS 驱动切换 |

---

## v1.6 — Markdown 输入源（2026-07-13）

### 🎯 问题

用户已将教材 PDF 扫描转换为 Markdown 格式（预提取的结构化文本），但 live-tutor 不支持直接读取 Markdown 文件作为内容来源。用户只能走 PDF 路径（OCR 冗余）或 AI 生成路径（不对齐教材）。同时，这也是后续本地知识库（RAG）方案的前置基础。

### 🆕 方案

**新增 `source_type = "markdown"`**，归类为 Path A 的第三种文件格式（与 PDF/PPT 并列）。extraction.md 新增独立的「路径 M」处理管线。

### 路径 M 设计要点

- Markdown 已是结构化纯文本 + LaTeX 公式，**无需 OCR**
- 章节识别：解析 `#` `##` `###` 标题层级（含回退策略）
- 知识点提取：识别 `**定义**`、`**定理**`、`$...$` 公式、`**注意**` 误区
- 重要性判定和等级过滤规则与路径 A 完全一致
- 输出格式与路径 A 完全一致——下游 agent 无感知

### 📝 修改文件

| 文件 | 改动 |
|------|------|
| `extraction.md` | 路由表 +markdown 行<br>新增「路径 M：Markdown 提取」完整 section（M.1~M.6）<br>依赖说明新增路径 M |
| `SKILL.md` | 版本号 v1.5 → v1.6<br>description、模块索引、Step 0.2 入口、0.2A、0.3 初始化表、Step 2 路由表、Step 3、文件结构、后期补充教材 |
| `progress_schema.json` | `source_type` enum +`"markdown"`<br>title/description 更新 |
| `iron-rules.md` | R-SRC-1 更新为四个入口<br>+R-SRC-8（Markdown 格式规范） |
| `CHANGELOG.md` | 本条目 |

### 🛡️ 不改的文件（共 10 个）

`agents/*`（3 个）、`persona.md`、`character-voices.md`、`templates/*`（4 个）、`scripts/review_calc.py`、`progress_template.json`

---

## v1.5.1 — ISBN / 教材信息精准匹配（2026-07-07）

### 🎯 问题

v1.5 Path B 的大纲生成有两种模式：纯 AI 生成（通用但可能不对齐）和 WebSearch 增强（接近教学大纲但不够精准）。用户手上有教材时，希望内容**精确对齐特定教材的章节顺序**，但又不想上传整本 PDF。

### 🆕 方案

**ISBN → 公开目录提取 → AI 填充内容**

```
用户提供 ISBN 或"书名+作者+版次"
    ↓
WebSearch 搜索公开目录/图书馆 OPAC/出版社页面/Google Books
    ↓
提取真实章节目录（骨架）
    ↓
AI 按章生成知识点内容（血肉）
    ↓
用户确认 → 开课
```

### 改动摘要

- **Path B 新增第三选项**：0.2B.3 增加 [C] "教材信息精准匹配"，调用 extraction.md B.1.3
- **extraction.md B.1.3**：完整的 ISBN 查询管线（6 优先级查询策略、完整性检查、来源标注、法律约束）
- **0.2B.1 扩展**：基本信息收集阶段即可选填 ISBN/教材信息
- **Schema 扩展**：`syllabus_source` 新增 `"isbn_lookup"`，`ai_generation_meta` 新增 `isbn_lookup_meta`

### 📝 修改文件

| 文件 | 改动 |
|------|------|
| `SKILL.md` | 0.2B.1 新增教材信息输入<br>0.2B.3 新增 [C] 选项 + 三种模式对比表<br>工作流图、0.3 初始化表更新 |
| `extraction.md` | 新增 B.1.3 ISBN 精准匹配（6 优先级查询、完整性检查、法律约束） |
| `progress_schema.json` | `syllabus_source` +`"isbn_lookup"`<br>`ai_generation_meta` +`isbn_lookup_meta` |
| `iron-rules.md` | +R-SRC-6/7（公开源约束、来源标注）<br>+反模式 #24-25 |
| `CHANGELOG.md` | 本条目 |

### 法律与伦理设计

- ✅ 仅搜索公开可访问网页（出版社官网、图书馆 OPAC、Google Books 预览、豆瓣）
- ✅ 目录/知识点列表是事实信息，不受版权保护
- ❌ 不得尝试下载或抓取整本 PDF
- ❌ 不得访问付费/登录站点
- 展示大纲时须标注来源 URL

---

## v1.5 — 无 PDF 启动：三入口架构（2026-07-07）

### 🎯 问题

v1.4 及之前版本强制要求用户上传教材 PDF 才能开始学习。用户最大的流失点在第一步——"去找教材 PDF"。

### 🆕 核心方案

**方案 C（混合渐进）落地**：从"教材驱动"变为"课程驱动"，PDF 从必选项降级为可选项。

**三层入口**：

```
用户输入科目名
    ├─ Layer 1：预置课程库（秒开，未来实现）
    ├─ Layer 2：AI 自生成（输入科目名即可，本次核心）
    └─ Layer 3：PDF 上传（现有流程，保留为增强选项）
```

### 关键发现

下游 agents（tutor / assess / exam）完全不依赖 PDF——只消费结构化数据（知识点列表、章节大纲、学习手册）。唯一 PDF 依赖在 `extraction.md`。因此改动面极小：5 个文件修改，10 个文件完全不动。

### 🆕 新功能

- **Step 0 三入口**：用户可选 [A] 上传教材 / [B] 直接输科目名 / [C] 课程库
- **Path B AI 生成流程**：科目+考试类型 → Persona → IP角色 → 大纲生成 → 用户确认 → 开课
- **extraction.md 双管线**：路由表驱动，路径 A（PDF 提取）完整保留，路径 B（AI 生成）三阶段：生成大纲 → 用户确认 → 按章延迟生成知识点
- **WebSearch 增强**：可选搜索真实教学大纲交叉验证章节结构
- **后期补充教材**：AI 生成的课程后续可无缝切换/补充 PDF 内容
- **用户大纲编辑**：生成的章节目录支持增删改
- **知识盲区回退**：极冷门科目自动回退到 PDF 上传或手动输入

### 📝 修改文件

| 文件 | 改动 |
|------|------|
| `SKILL.md` | Step 0 完全重写（三入口 + Path B 完整流程）<br>Step 1 新增 AI 生成摸底限制<br>Step 2 改为路由表驱动<br>Step 3 新增 AI 生成分支<br>新增「后期补充教材」章节<br>新增「0.3 统一出口」初始化对照表<br>版本号 v1.4 → v1.5 |
| `extraction.md` | 完全重写：路由表 + 路径 A（保留）+ 路径 B（新增三阶段）+ 路径 C（占位）<br>从 44 行 → ~180 行 |
| `progress_schema.json` | `textbook` 从 required 移除<br>+`source_type` 字段（pdf/ppt/ai_generated/course_library）<br>+`syllabus_source` 字段<br>+`ai_generation_meta` 对象<br>多个字段允许空串/null 初始化<br>版本号 v1.2 → v1.5 |
| `progress_template.json` | +`character`/`render_mode`/`source_type`/`syllabus_source`/`knowledge_tracking`/`ai_generation_meta` 默认值 |
| `iron-rules.md` | +R-INT-7/8（大纲必须确认、考试类型必须询问）<br>+R-CON-5（知识点统一格式）<br>+来源规则 R-SRC-1~5（新增 section）<br>+反模式 #20-23 |

### 🛡️ 不改的文件（共 10 个）

`agents/*`（3 个）、`persona.md`、`character-voices.md`、`templates/*`（4 个）、`scripts/review_calc.py`

### 🧪 验证

- Schema 校验：`progress_template.json` 通过 `progress_schema.json` v1.5 验证 ✅
- 交叉引用：所有 module index 文件引用指向存在的文件 ✅
- 回归：Path A（PDF 上传）原有流程文本完全保留 ✅

---

## v1.4 — IP 角色语音系统（2026-07-06）

### 🆕 新功能

**IP 角色叠加到 Persona 教学策略**

Persona 决定"教什么"，IP 角色决定"怎么说"。首批 4 个角色：

| 角色 | 人设 | 最佳搭配 | 核心梗 |
|------|------|---------|--------|
| 🐑 懒羊羊 | 大智若愚的躺平学霸 | D 速成 + 懒羊羊 | "聪明羊不用太多时间也能学会" |
| 🔥 哪吒 | 逆天改命的狠人 | E 考研 + 哪吒 | "我命由我不由天" |
| 🫡 小小怪下士 | 永远打不倒的小兵 | A 标准 + 小小怪 | "大大怪将军说过……" |
| 🐺 灰太狼 | 我一定会回来的 | E 考研 + 灰太狼 | "本大王一定会回来的！" |

每个角色包含：
- 性格档案（5 关键词 + 说话方式描述）
- 口头禅库（13 个场景预设：开场、鼓励、批评、章节完成、错题、考前等）
- 教学行为特征（类比体系、专属术语）
- 与 5 个 Persona 的叠加效果说明
- 通用语气规则（台词密度 30% 角色 + 70% 知识）
- 对话模板（章节小测结果等高频场景）

**渲染模式选择**：Step 0 新增第 6 步——Markdown（纯文本通用）vs HTML（交互式组件）

### 📝 修改文件

| 文件 | 改动 |
|------|------|
| `character-voices.md` | 🆕 新建 — IP 角色语音系统完整定义（4 角色 × 13 场景） |
| `SKILL.md` | Step 0 新增第 5-6 步：选择 IP 角色 + 渲染模式<br>Step 2.5 新增预检反馈自然过渡语言指引<br>文件结构新增 `character-voices.md` |
| `persona.md` | 新增角色选择提示，引用 character-voices.md |
| `progress_schema.json` | +`character` 字段 +`render_mode` 字段（markdown/html） |
| `iron-rules.md` | +R-INT-6 过渡语言铁律<br>+过渡语言规则表（按分数段的反馈基调）<br>+反模式 #17 禁止机械式过渡语<br>+反模式 #18 禁止空洞夸奖<br>+反模式 #19 禁止归因于学生能力 |

### 🐛 修复

- **测评后过渡语生硬**：不再直接输出"L3 开始学习"，改为根据分数给出自然的、符合 IP 角色语气的评价反馈。高分夸具体行为，低分归因于客观因素，始终解释等级的含义。

---

## v1.3 — 间隔复习系统（2026-07-06）

### 🆕 新功能

**SM-2 间隔重复算法集成**

基于艾宾浩斯遗忘曲线，为每个 ⭐⭐⭐ 知识点独立追踪记忆衰减，跨会话自动调度复习。

- **`scripts/review_calc.py`**（~170 行）— SM-2 计算工具
  - `check`：读取 progress.json，计算所有知识点的保持率和到期状态，按紧迫度排序返回复习队列
  - `update`：根据用户答题质量（quality 0-5）更新 SM-2 参数（EF、interval、repetitions），答对延长间隔，答错重置
  - `init`：章节学习完成后批量注册知识点到 knowledge_tracking
  - 遗忘模型：指数衰减 $R = e^{-t/S}$，$S = \text{interval} \times \text{EF} / 2.5$
  - 间隔序列：1 → 3 → 7 → 15 → 30 天，之后按 `interval × EF` 递增

- **Step 0.5：间隔复习检查**
  - 每次进入逐章学习循环前自动运行 `review_calc.py check`
  - 有过期项：展示到期/超期知识点列表（保持率、超期天数），提供 2-3 道快题复习
  - 无过期项：零打扰，直接进入学习
  - 复习交互：MCQ 答题 → quality 映射（答对=4，答错=1）→ `review_calc.py update`
  - 复习完成后展示结果表（下次复习日期）

- **Step 5 扩展：knowledge_tracking 初始化**
  - 章节小测完成后，自动将该章所有 ⭐⭐⭐ 知识点写入 knowledge_tracking
  - 错题对应知识点标记 `is_error: true`，初始 EF 降为 2.0（优先复习）

### 📝 修改文件

| 文件 | 改动 |
|------|------|
| `scripts/review_calc.py` | 🆕 新建 — SM-2 计算工具（check / update / init） |
| `SKILL.md` | +Step 0.5 完整流程定义（触发时机、交互规则、quality 评分标准）<br>Step 5 新增第 5 步：初始化 knowledge_tracking<br>文件结构新增 `scripts/review_calc.py`<br>版本号 v1.2 → v1.3 |
| `iron-rules.md` | +6 条复习铁律（R-REVIEW-1 ~ R-REVIEW-6）<br>+4 条反模式（#13 不追踪时间戳 / #14 手动算日期 / #15 不初始化 tracking / #16 复习超纲） |
| `progress_schema.json` | +`knowledge_tracking` 字段（additionalProperties 模式，含 chapter/title/stars/learned_at/last_reviewed/repetitions/interval_days/ef/next_review/is_error/review_history） |

### 📊 Token 消耗

| 环节 | 消耗 |
|------|------|
| `review_calc.py check` 输出 | ~200 tokens |
| `review_calc.py update` 输出 | ~150 tokens |
| 复习交互（3 道题） | ~800-1200 tokens |
| **合计/会话** | **~1.2-1.5K tokens（约 +8-10%）** |

### 🧪 验证

- `check`：刚初始化的知识点无到期项 → review_queue 为空 ✅
- `update`：quality=4 → interval 1→3 天，EF 不变 ✅
- `update`：quality=5 → interval 1→3 天，EF 2.5→2.6 ✅
- `update`：quality=1 → interval 重置为 1 天，EF 2.5→1.96 ✅
- `check`：update 后无到期项 → review_queue 为空 ✅

---

## v1.2 — 自适应等级优化 & 架构重构（2026-07-04）

> 详见 [UPGRADE_REPORT_v1.2.md](UPGRADE_REPORT_v1.2.md)

### 改动摘要

**架构层面（3 项）**：
- **模块化拆分**：SKILL.md 654→379 行（↓42%），抽取 7 个独立模块（persona / iron-rules / extraction / 4 个 template）
- **Agent 激活**：3 个 agent 从死代码变为活跃调度（tutor / assess / exam），assess_agent 从 2 模扩展到 4 模
- **Schema 统一**：新增 `progress_schema.json`（JSON Schema Draft-07），提供 v1.1→v1.2 迁移工具

**功能层面（9 项）**：
- **per_chapter_level**：等级跟踪从全局改为按章独立
- **进度恢复**：Step 0 检测已有 progress.json，提供继续/重新开始/换科目选项
- **双模摸底**：Step 1 支持快速摸底（5 题）/ 深度摸底（8-10 题）
- **章节预检**：Step 2.5 每章开始前 2-3 道快速题判断起始等级
- **微测试**：Step 4 小节结束后可选做微测试（不计入等级）
- **可视化图表**：学习手册插入 Mermaid/ASCII 图表（5 种类型）
- **错题注入**：重学时在手册中注入上次易错点
- **考前备忘录**：Step 5.5 汇总公式/高频错题/易混淆概念
- **最终检测错题加权**：Step 6 含 20-30% 错题改编题

### 变更统计

| 指标 | v1.1 | v1.2 | 变化 |
|------|------|------|------|
| SKILL.md 行数 | 654 | 379 | ↓42% |
| 文件数（不含 output） | 6 | 14 | +8 |
| 总代码行数 | ~1,200 | 1,886 | +57% |
| Agent 定义数 | 3（死代码） | 3（活跃调度） | 全部重写 |
| 模板文件数 | 0 | 4 | 新增 |
| JSON Schema | 无 | 有 | 新增 |

---

## v1.1 — Persona 系统

### 改动摘要

- 五种 Persona（A 标准 / B 工程 / C 数学 / D 速成 / E 考研）
- Persona 对行为的影响矩阵（覆盖/公式/手册/自检/小测/错题集/语言风格）
- 章节小测题型比例按 Persona 表执行
- Persona 专属学习手册增强段落

---

## v1.0 — 初始版本

### 改动摘要

- 基础工作流：Step 0 → Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6
- 四级自适应等级系统（L1~L4：基础/巩固/提升/全面）
- 内容提取管线（PDF/PPT → OCR → 知识点标记）
- 学习手册六段式结构
- 章节小测 + 错题集
- 最终综合检测

---

## 版本演进路线图

```
v1.0                v1.1                v1.2                  v1.3              v1.4              v1.5              v1.5.1            v1.6
  │                   │                   │                     │                 │                 │                 │                 │
  ├─ 六步工作流       ├─ Persona A-E      ├─ 模块化拆分          ├─ SM-2 间隔复习  ├─ IP 角色语音    ├─ 三入口架构      ├─ ISBN 精准匹配  ├─ Markdown 输入源
  ├─ L1-L4 自适应     ├─ 行为矩阵         ├─ per_chapter_level   ├─ review_calc.py ├─ 4 角色×13 场景 ├─ AI 内容生成     ├─ 公开目录提取    ├─ 路径 M 提取管线
  ├─ PDF/PPT 提取     ├─ 题型比例         ├─ 双模摸底            ├─ Step 0.5       ├─ 渲染模式选择   ├─ 无 PDF 启动     ├─ Path B [C] 选项 ├─ 四路径路由
  ├─ 学习手册         ├─ 专属增强         ├─ 章节预检            ├─ knowledge      ├─ 过渡语言铁律   ├─ extraction 路由表├─ 来源标注约束    ├─ 无需 OCR
  ├─ 章节小测         │                   ├─ 微测试              │   _tracking     ├─ 反模式 #17-19  ├─ 大纲用户确认     ├─ 反模式 #24-25   └─ 下游无感知
  └─ 最终检测         │                   ├─ 可视化图表          │                 │                 ├─ 后期补充教材     └─ isbn_lookup_meta
                      │                   ├─ 考前备忘录          │                 │                 ├─ 知识盲区回退
                      │                   ├─ 进度恢复            │                 │                 └─ 反模式 #20-23
                      │                   └─ 错题注入            │                 │
```
