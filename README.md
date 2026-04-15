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

打开 `SKILL.md`，按其中的：

- Input Intake（输入逻辑）
- Prompt Rules（四类图片提示词模板）
- Wan2.7 调用（依赖与使用）

执行即可。
