---
name: amazon-product-image-wan27
description: Use when generating Amazon listing images (main/scene/detail/A+) from user specs and reference images, and you must call wan2.7-image with strict Amazon-compliant prompt rules.
---

# Amazon 商品图生成（Wan2.7 可复用 Skill）

## Overview

将“用户输入 + 参考图”转成可执行的 Amazon 商品图生成方案：先做需求澄清与结构化输入，再按图片类型生成严格约束的提示词，最后通过 `wan2.7-image-skill` 调用生成并输出可直接用于 Amazon Listing 的图片。

**REQUIRED SUB-SKILL:** `wan2.7-image-skill`

## When to Use

- 需要生成 Amazon Listing 的商品主图、场景图、细节图、A+ 图
- 用户提供了 1–3 张参考图，要求保持“同一商品身份一致性”
- 需要把“营销文案”以严格规则渲染到图片里（只允许出现指定文本，且只出现一次）
- 需要把生成流程做成可复用的标准化输入 + 提示词 + 调用方式

## Outputs

- 每张图：`{type, size, prompt, image_url}`（推荐同时保留 prompt 便于复现）
- 推荐输出集合：
  - `main` 1–2 张（白底主图）
  - `scene` 1–4 张（生活方式/场景图）
  - `detail` 1–4 张（细节特写）
  - `aplus` 1–4 张（A+ 氛围营销图）

## Input Intake（输入逻辑）

### 1) 必填信息（最少可开工）

- 商品名称（用于提示词的语义锚点）
- 参考图 1–3 张（本地文件 / 公网 https URL / 已上传的 oss:// URL）
- 需要生成的图片类型与数量（main/scene/detail/aplus）

### 2) 强烈建议补充（显著提升可控性）

- 类目（category）、材质（material）、尺寸（dimensions）
- 使用场景（useCase）、目标人群（targetAudience）
- 风格档案（style profile）：`minimal_modern` / `japanese_soft` / `luxury_editorial`

### 3) 文案（可选）

对 `scene/detail/aplus` 单张图可填写一条“要渲染到图里”的文案（description）。该文案必须满足：

- 单行文本
- 必须逐字逐符号完全一致（不得改写、翻译、补字、加标点）
- 图片中除该文案外不得出现任何其他文字

## Generation Settings（生图设定）

### 分辨率建议

- `main/scene/detail`：建议 `1600*1600`（或 `1K/2K`）
- `aplus`：建议宽幅，如 `1200*600`、`1464*600` 等（按 A+ 模板需要调整）

### 一致性策略

- 参考图用于“主体一致性”：在所有类型中使用同一组参考图作为输入（1–3 张）
- 提示词中强制声明“同一商品身份不改变”：形状、颜色、材质、细节不变

## Prompt Rules（所有图片生成规则与提示词）

下述模板写成可直接投喂给 `wan2.7-image` 的自然语言指令。把其中占位符替换为实际信息即可。

### 通用占位符

- `{PRODUCT_NAME}`：商品名称
- `{CATEGORY}`：类目（可空）
- `{MATERIAL}`：材质（可空）
- `{COPY}`：要渲染到图里的文案（仅 scene/detail/aplus 可选）
- `{TYPOGRAPHY}`：字体风格描述（由 style profile 决定）

### 共同硬规则（所有类型都适用）

- 基于参考图生成，保持“同一商品身份一致性”，不得变成其他商品
- 画面必须是“真实摄影感/电商摄影感”，透视与光线要合理
- 禁止：水印、logo（除非用户明确提供并要求保留）、二维码、UI 截图、网页布局、边框、拼接分栏、白边留空面板、海报模板边框
- 如需渲染 `{COPY}`：必须严格执行“唯一文本规则”（见下）

### 唯一文本规则（仅当 `{COPY}` 非空时启用）

把以下内容放在提示词最前面作为最高优先级锚点：

```
CRITICAL TEXT TO RENDER (EXACT, HIGHEST PRIORITY)
TEXT_TO_RENDER_BEGIN
{COPY}
TEXT_TO_RENDER_END
Rules: render this text exactly once, character-by-character, no translation, no paraphrase, no extension, no added punctuation, single line, no other text anywhere.
Typography must follow: {TYPOGRAPHY}.
```

并在提示词末尾重复一次：

```
TEXT_TO_RENDER_REPEAT: {COPY}
```

### 1) Main（白底主图）提示词模板

```
Based on the reference image, create an Amazon white background main product photo.
The reference image shows {PRODUCT_NAME}{CATEGORY:+, a {CATEGORY}}{MATERIAL:+, made of {MATERIAL}}.
Keep the exact same product identity and appearance from the reference image (same object, same shape, same color, same material, same details). Do NOT change it into any other product.
Tight framing: the product should fill at least 85% of the image area, minimal white margins, subtle natural shadow only.
Pure white background (#FFFFFF), professional studio lighting, high-end e-commerce photography, ultra sharp focus.
No text, no logo, no watermark.
```

### 2) Scene（场景图）提示词模板

```
Based on the reference image showing {PRODUCT_NAME}{CATEGORY:+, a {CATEGORY}}{MATERIAL:+, made of {MATERIAL}}, create an Amazon lifestyle product photo.
Place this exact product (same identity and appearance from reference) in a real, natural lifestyle scene with coherent lighting and perspective.
Product is the hero element, realistic environment, premium atmosphere.
Full-bleed, edge-to-edge composition: the scene must fill 100% of the canvas.
No screenshot, no UI, no webpage layout, no poster mockup, no inset image, no padding, no border, no frame, no white margins, no header bar, no top title strip.
If text is required, follow the unique text rule and place the text in corner negative space; avoid centered placement; do NOT cover the product.
```

### 3) Detail（细节特写）提示词模板

```
Based on the reference image showing {PRODUCT_NAME}{MATERIAL:+, made of {MATERIAL}}, create an Amazon product detail close-up.
Extreme macro / close-up shot with tight crop: focus on the most important detail area and show fine texture and craftsmanship.
The detail subject should fill 60–80% of the frame.
Do NOT do wide shot. Do NOT show the full product. Do NOT use a lifestyle scene composition.
Background is allowed but must be strongly blurred (bokeh), shallow depth of field, minimal and unobtrusive.
Premium lighting, ultra sharp focus on the detail.
If text is required, follow the unique text rule and keep text small, placed in corner negative space; never center; do NOT cover the key detail area.
```

### 4) A+（营销氛围图）提示词模板

```
Based on the reference image showing {PRODUCT_NAME}{CATEGORY:+, a {CATEGORY}}, create an Amazon A+ marketing poster image.
Feature this exact product (same identity and appearance from reference) in a premium lifestyle scene with cohesive composition and strong marketing mood.
Full-frame content: no empty side panels, no split panels.
If text is required, follow the unique text rule and keep it as a single strong headline in corner negative space; do NOT cover the product.
```

## Style Profile（风格档案 → Typography）

目的：当需要渲染 `{COPY}` 时，指定更稳定的“字体气质”以减少模型胡乱出字形的概率。

- `minimal_modern`：现代几何无衬线、瑞士现代风格、克制、可读性优先
- `japanese_soft`：柔和手写/圆润无衬线、温柔、轻量
- `luxury_editorial`：高对比现代衬线、编辑感、克制但高级

输出时把 typography 写成一句英文描述（示例）：

- minimal_modern: `neo-grotesque sans-serif title (Swiss modern), clean grid typography, bold weight, not cursive, not handwritten`
- japanese_soft: `rounded minimal sans-serif with a soft friendly feel, warm tone, subtle`
- luxury_editorial: `high-contrast modern serif headline (editorial), premium and restrained, bold weight`

## Wan2.7 调用（依赖与使用）

### 依赖

- 已安装 `wan2.7-image-skill`（本机默认位置通常为 `~/.trae/skills/wan2.7-image-skill`）
- 环境变量：
  - `DASHSCOPE_API_KEY`（必填）
  - `DASHSCOPE_BASE_URL`（可选，默认 `https://dashscope.aliyuncs.com/api/v1/`）

### 参考图上传（本地文件 → oss://）

```bash
python3 ~/.trae/skills/wan2.7-image-skill/scripts/file_to_oss.py \
  --file /path/to/reference.png \
  --model wan2.7-image
```

### 生成单张图（推荐：图生图以保证一致性）

```bash
python3 ~/.trae/skills/wan2.7-image-skill/scripts/image-generation-editing.py \
  --user_requirement "<PUT_PROMPT_HERE>" \
  --input_images "oss://..." "oss://..." \
  --n 1 \
  --size "1600*1600"
```

## Common Mistakes

- 主图出现道具/场景/文字：主图必须白底且无任何文字元素
- 文案被模型自动改写：必须使用“唯一文本规则”锚定，且文案只能单行且必须完全一致
- 画面像网页截图/带边框留白：提示词必须明确 full-bleed、禁止 UI/海报模板/边框/白边
- 商品变形/变成其他商品：必须反复强调“同一商品身份一致性”，并始终提供参考图
- 在图片里生成品牌 logo：除非用户明确要求，否则要禁止 logo/watermark/text

## Minimal Example（最小复用示例）

用户输入（示例）：

- 商品：Stainless Steel Insulated Tumbler
- 参考图：1 张
- 生成：main 1 张（无文案）；scene 2 张（分别有文案）
- 风格：minimal_modern

执行步骤：

1. 把参考图上传成 `oss://...`
2. 用 main 模板生成主图 prompt 并调用生成
3. 用 scene 模板生成 2 条 prompt（每条带不同 `{COPY}`），每条都带“唯一文本规则”，分别调用生成

## Verification Checklist（交付前自检）

- main：背景纯白（接近 #FFFFFF）、无文字、无道具、商品占画面约 85%+、仅有自然阴影
- scene/detail/aplus：无边框/无网页截图感/无拼接分栏/无多余文字
- copy：图片中仅出现 `{COPY}` 一次，逐字逐符号一致，且为单行
- 一致性：所有图中的商品外观与参考图一致（颜色/材质/结构/关键细节不变）

## Red Flags（出现即停止并改 Prompt）

- “顺便加点 slogan / badge / 促销字样”：违反唯一文本规则
- “主图加点道具更好看”：主图应无道具无场景
- “参考图不重要，随便生成”：会导致商品身份漂移，必须保留参考图输入
