## amazon-product-image-wan27

基于 wan2.7-image 的 Amazon 商品图生成 Skill（main/scene/detail/A+），核心是“严格提示词规则 + 参考图一致性 + 文案唯一文本规则”。

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
```

##### 用户可输入的选项（字段说明）

- `ProductInfo`（建议填写）
  - `name`（必填）
  - `category`（可选）
  - `material`（可选）
  - `dimensions`（可选）
  - `useCase`（可选）
  - `targetAudience`（可选）
- `StyleProfile`（可选，默认 minimal_modern）
  - `minimal_modern`
  - `japanese_soft`
  - `luxury_editorial`
- `References`（必填，1–3 个）
  - `file: /abs/or/relative/path.png`
  - `url: https://...`（公网 https 链接）
  - `oss: oss://...`（已上传的 OSS 链接）
- `Generate`（必填，至少一种）
  - `main | scene | detail | aplus`
  - 每种类型支持：
    - `count`：生成张数
    - `size`：分辨率，如 `"1600*1600"`、`"1K"`、`"2K"`，A+ 常用 `"1200*600"`
    - `copy`（可选，仅 scene/detail/aplus）：字符串数组，长度建议与 `count` 一致；每条必须单行且严格逐字一致（图片中只允许出现这一条文本且只出现一次）

然后提供以下信息（越完整越稳定）：

- ProductInfo：name / category / material / dimensions / useCase / targetAudience
- References：1–3 张参考图（本地文件 / https URL / oss:// URL）
- 需要生成的类型与数量：main/scene/detail/aplus
- 每张图的文案（可选）：仅用于 scene/detail/aplus，且必须单行且严格逐字一致
- Style profile（可选）：minimal_modern / japanese_soft / luxury_editorial

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
- Prompt Rules（四类图片提示词模板）
- Wan2.7 调用（依赖与使用）

执行即可。
