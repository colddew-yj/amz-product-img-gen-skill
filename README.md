## amazon-product-image-wan27

基于 wan2.7-image 的 Amazon 商品图生成 Skill（main/scene/detail/A+），核心是“严格提示词规则 + 参考图一致性 + 文案唯一文本规则”。

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
