## amazon-product-image-wan27

基于 wan2.7-image 的 Amazon 商品图生成 Skill（main/scene/detail/A+/dimension/fusion），核心是“严格提示词规则 + 参考图一致性 + 文案唯一文本规则”。

### Source Project

本 skill 来源项目（完整功能实现与可视化界面）：https://github.com/colddew-yj/amz-product-img-gen

### Files

- `SKILL.md`：主 Skill 文档（输入逻辑、提示词模板、调用方式）

### Dependency

- `wan2.7-image-skill`（本机通常在 `~/.trae/skills/wan2.7-image-skill`）
- 环境变量：
  - `DASHSCOPE_API_KEY`（必填）
  - `DASHSCOPE_BASE_URL`（可选）

### Install (Recommended)

把本仓库放到你的全局 skills 目录：

```bash
mkdir -p ~/.trae/skills/amazon-product-image-wan27
cp -R ./* ~/.trae/skills/amazon-product-image-wan27/
```

### Usage

#### 方式 1：在对话中调用 Skill（推荐）

在支持 Skills 的对话/Agent 里，直接输入：

```
Use Skill: amazon-product-image-wan27
```

##### Agent 会话示例（可直接复制改写）

```
Use Skill: amazon-product-image-wan27

ProductInfo:
  name: "Stainless Steel Insulated Tumbler"
  category: "Tumbler"
  material: "304 stainless steel"
  dimensions: "20oz"
  useCase: "commuting, office, gym"
  targetAudience: "men and women, 18-45"

StyleProfile: minimal_modern

References:
  - file: /path/to/ref1.png

Generate:
  main:
    count: 1
    size: "1600*1600"
  scene:
    count: 2
    size: "1600*1600"
    copy:
      - "Keeps drinks cold for 24 hours"
      - "Leak-proof lid"
  detail:
    count: 1
    size: "1600*1600"
    copy:
      - "Double-wall vacuum"
  aplus:
    count: 1
    size: "1200*600"
    copy:
      - "Built for every day"
  dimension:
    count: 1
    size: "1600*1600"
```

##### 用户可输入的选项（字段说明）

- `ProductInfo`（建议填写）
  - `name`（必填）
  - `category`（可选）
  - `material`（可选）
  - `dimensions`（可选；不知道精确尺寸也建议给近似描述，如 “约 8cm” / “palm-sized” / “fits on a fridge door”）
  - `useCase`（可选）
  - `targetAudience`（可选）
- `StyleProfile`（可选，默认 minimal_modern）
  - `minimal_modern`：极简现代（偏"干净电商"）- 支持中文/英文/日语
  - `japanese_soft`：日系柔和（偏"手写/刷字艺术体"）- 支持日文/中文/韩语文
  - `luxury_editorial`：奢华编辑（偏"高端杂志/现代衬线"）- 支持英文/法文/中文
  - `rounded_bold`：圆润大粗体（偏"可爱友好/粗壮饱满"）- 支持中文/英文/日语
  - `yahoma_light`：雅黑light（偏"纤细轻量/现代简洁"）- 支持中文/英文/日语/法文
- `References`（必填，1–3 个）
  - `file: /abs/or/relative/path.png`
  - `url: https://...`（公网 https 链接）
  - `oss: oss://...`（已上传的 OSS 链接）
- `Generate`（必填，至少一种）
  - `main | scene | detail | aplus | dimension`
  - 每种类型支持：
    - `count`：生成张数
    - `size`：分辨率，如 `"1600*1600"`、`"1K"`、`"2K"`，A+ 常用 `"1200*600"`
    - `copy`（可选，仅 scene/detail/aplus）：字符串数组，长度建议与 `count` 一致
      - 必须严格逐字一致（包含大小写/空格/标点/换行）
      - 必须只出现一次，且只能作为一个连续的文字块（禁止拆成“标题 + 副标题”两块）
      - 允许你用 `\n` 手动换行来控制排版（模型不得额外换行）；不写也可以，skill 会自动做排版判定

##### 文案与版式的自动规则（无需填写额外字段）

- 默认文字模式：文字准确优先（只有当用户明确说“艺术体/手写/刷字/海报感”时才偏向艺术表现）
- 默认位置：自动选择四角中最干净的留白区；如无法判断，默认右上角
- 默认版式参数：safe margin 约 8%，最大宽度约 45%，右上角默认右对齐
- 长文案处理：若文案很长且容易触发错字，skill 可自动在冒号/逗号等自然断点处插入 1 个换行用于排版（不改写任何字符）

##### 高级覆盖（可选）

- `CopyMode`
  - `strict`：文字准确优先（推荐默认）
  - `artistic`：艺术表现优先（错字风险更高，需要更多重试）
- `TextLayout`
  - `corner_top_left | corner_top_right | corner_bottom_left | corner_bottom_right`
  - 可附加：`maxWidthPct`（建议 40–55），`safeMarginPct`（建议 6–10），`align`（left/right）

##### 文案建议（避免模型拼写错误）

- 尽量短：建议 < 45 个字符；过长更容易自动换行或出现错别字/漏字
- 避免复杂字符：少用特殊符号、花体、非 ASCII 字符
- 字体策略：根据想要的效果选 style profile（有文案时更建议短文本 + 多次重试）
  - `japanese_soft`（日系柔和）：更明显的手写/刷字艺术体风格
  - `luxury_editorial`（奢华编辑）：高级编辑风格（现代衬线/高对比）
  - `minimal_modern`（极简现代）：干净现代电商风格（几何无衬线）
- 验收标准：只要出现拼写错误（例如 Fridge→Fnidge），必须重生成，不接受“近似文本”
  - 可直接在提示里追加：no line breaks, no word wrap, no hyphenation, no ligatures, no perspective warp
  - 文案过长时：优先缩短文案，而不是让模型自动换行
- 长文案排版：如果必须保留长句，建议你主动在文案里插入换行 `\n`（例如分两行），并要求模型按换行逐行渲染（仍然逐字一致）
- 重试建议：错字/黑边/居中标题都属于硬失败，建议自动或手动重试多次，并更换角落位置与 typography 候选
- 禁止拆分：不允许把一句文案拆成两个区域（例如顶部做短标题，底部再放完整句）；必须只出现一次且是一个连续的文字块

##### 尺寸与比例（没有 dimensions 也要真实）

- 未提供 `dimensions` 时：模型必须根据“参考图 + 类目 + 使用场景”推断合理的真实尺寸与比例，避免把小物件生成成巨物或迷你玩具
- 推荐做法：在场景图里加入自然比例参照（如冰箱门把手、便签、马克杯、手部等），并要求产品尺寸与参照物符合常识

##### 尺寸标注图（dimension）

- 仅当提供 `dimensions` 时生成
- 自动添加尺寸标注：长度、宽度、高度
- 使用黑色或深灰色细线箭头
- 标注格式：仅数字和单位（如 "17cm"），无中文标记

#### 编号规则

- **默认图**：`IMG-001`、`IMG-002`...，每次生成自动递增
- **融合图**：`IMG-F001`、`IMG-F002`...，序号在会话中独立递增
- **编辑图**：`IMG-001-EDIT-1`、`IMG-001-EDIT-2`...，基于原图编号
- **【强制】每张生成的图片都会分配唯一编号**，确保可追踪性

#### 核心功能

##### 默认图生产品图功能

- 基于参考图生成各类产品图片
- 支持 main（白底主图）、scene（场景图）、detail（细节图）、aplus（营销图）、dimension（尺寸图）
- 保持商品身份一致性，确保颜色、材质、结构不变
- 支持文案渲染和风格定制

##### 融合生图（Fusion Mode）

- 支持多个参考图的自然融合
- 保持每个产品的身份一致性
- 自动处理产品的前后层次和自然遮挡
- 统一的光线方向和氛围
- **支持输入方式**：图片编号、HTTP/HTTPS URL、oss:// URL，以及混合输入
- **输出编号**：使用 IMG-Fxxx 格式（如 IMG-F001），序号在会话中独立递增

##### 图片编辑模式

- 支持对已生成图片进行编辑
- 输入格式：`[编辑模式] + 图片编号 + 修改意见`
- 自动沿用原图的场景和风格
- **输出编号**：编辑版本使用 IMG-{原编号}-EDIT-{序号} 格式（如 IMG-003-EDIT-1）

然后提供以下信息（越完整越稳定）：

- ProductInfo：name / category / material / dimensions / useCase / targetAudience
- References：1–3 张参考图（本地文件 / https URL / oss:// URL）
- 需要生成的类型与数量：main/scene/detail/aplus/dimension
- 每张图的文案（可选）：仅用于 scene/detail/aplus，且必须单行且严格逐字一致
- Style profile（可选）：minimal_modern / japanese_soft / luxury_editorial / rounded_bold / yahoma_light（均支持多语言）

如果你的环境需要重新加载 skills，请重启或刷新 skills 列表后再调用。

#### 方式 2：直接按文档手动跑 wan2.7（可复现/便于脚本化）

1) 把参考图上传为 `oss://...`（本地文件场景）：

```bash
python3 ~/.trae/skills/wan2.7-image-skill/scripts/file_to_oss.py \
  --file /path/to/reference.png \
  --model wan2.7-image
```

2) 打开 `SKILL.md` 复制对应类型的 prompt 模板，替换占位符后调用：

```bash
python3 ~/.trae/skills/wan2.7-image-skill/scripts/image-generation-editing.py \
  --user_requirement "<PUT_PROMPT_HERE>" \
  --input_images "oss://..." \
  --n 1 \
  --size "1600*1600"
```

#### 文档入口

打开 `SKILL.md`，按其中的：

- Input Intake（输入逻辑）
- Prompt Rules（五类图片提示词模板）
- Wan2.7 调用（依赖与使用）
- Fusion Mode（融合生图模式）
- Image Editing Mode（图片编辑模式）

执行即可。
