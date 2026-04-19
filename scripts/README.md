# Amazon Product Image Enhancement Scripts

This directory contains scripts to enhance the functionality of the `amazon-product-image-wan27` skill, providing advanced features like multi-language support, style mapping, prompt optimization, and batch image editing.

## Scripts Overview

### 1. `enhancer.py`

**Purpose**: Main enhancement module that provides a comprehensive set of tools for the amazon-product-image-wan27 skill.

**Key Features**:
- Language detection for input text
- Style mapping between different languages
- Prompt compression and optimization
- Prompt caching for improved performance
- Text rendering analysis
- Batch image editing

**Usage**:
```python
from scripts.enhancer import AmazonProductImageEnhancer

enhancer = AmazonProductImageEnhancer()

# Detect language
language = enhancer.detect_language("不锈钢保温杯")

# Map style
mapped_style = enhancer.map_style("极简现代", "zh")

# Optimize prompt
optimized_prompt = enhancer.generate_optimized_prompt(long_prompt, ["image1.jpg"])

# Batch edit images
results = enhancer.batch_edit_images(["IMG-001", "IMG-002"], "Move text to top-left")
```

### 2. `style_mapper.py`

**Purpose**: Handles style mapping between different languages and provides style recommendations based on product type.

**Key Features**:
- Style mapping for Chinese, French, and Japanese
- Supported language detection for each style
- Style validation
- Product-based style recommendations

**Usage**:
```python
from scripts.style_mapper import StyleMapper

mapper = StyleMapper()

# Map Chinese style to English
mapped = mapper.map_style("极简现代", "zh")

# Get supported languages for a style
languages = mapper.get_supported_languages("minimal_modern")

# Get recommended style for a product
recommended = mapper.get_recommended_style("Luxury Watch")
```

### 3. `prompt_optimizer.py`

**Purpose**: Optimizes prompts for AI image generation by compressing long prompts and caching results.

**Key Features**:
- Prompt compression while preserving key information
- Prompt caching for faster reuse
- Language-specific enhancements
- Batch prompt optimization
- Cache management

**Usage**:
```python
from scripts.prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer()

# Optimize a single prompt
optimized = optimizer.optimize_prompt(long_prompt, ["image1.jpg"])

# Batch optimize multiple prompts
prompts = ["Generate a mug", "Create a desk organizer"]
images = [["mug.jpg"], ["organizer.jpg"]]
optimized_prompts = optimizer.batch_optimize_prompts(prompts, images)

# Clear cache
optimizer.clear_cache()
```

### 4. `batch_editor.py`

**Purpose**: Provides batch editing functionality for multiple images and maintains edit history.

**Key Features**:
- Batch editing of multiple images
- Edit history tracking
- Version control and reverting
- Automatic edit instruction generation

**Usage**:
```python
from scripts.batch_editor import BatchImageEditor

editor = BatchImageEditor()

# Batch edit images
results = editor.batch_edit(["IMG-001", "IMG-002"], "Move text to top-left")

# Get edit history
history = editor.get_edit_history("IMG-001")

# Revert to a previous version
revert_result = editor.revert_to_version("IMG-001-EDIT-1")

# Generate edit instructions
instruction = editor.generate_edit_instructions("tumbler", "Change text to 'Keep cool'")
```

## Installation

1. Ensure Python 3.7+ is installed
2. No additional dependencies required (uses standard library only)
3. The scripts are automatically available when the skill is installed

## Integration with SKILL.md

These scripts can be integrated into the SKILL.md file by adding the following sections:

### Input Processing

```markdown
## 高级输入处理

### 多语言支持
- 自动检测输入语言（中文/英文/法语/日语）
- 自动映射风格术语到英文风格档案
- 为不同语言提供优化的提示词模板

### 智能参数推荐
- 基于产品类型自动推荐风格
- 基于历史数据优化提示词参数
- 批量处理多图生成请求
```

### Output Processing

```markdown
## 高级输出处理

### 文案渲染质量检测
- 自动检测文案渲染质量
- 识别并标记错字和排版问题
- 提供重生成建议

### 编辑历史管理
- 跟踪所有图片编辑历史
- 支持版本回溯和比较
- 批量应用相同编辑到多张图片
```

## Testing

To test the scripts, run them directly:

```bash
# Test enhancer.py
python3 scripts/enhancer.py

# Test style_mapper.py
python3 scripts/style_mapper.py

# Test prompt_optimizer.py
python3 scripts/prompt_optimizer.py

# Test batch_editor.py
python3 scripts/batch_editor.py
```

## Troubleshooting

### Common Issues

1. **Cache not working**: Ensure the `cache` directory has write permissions
2. **Language detection incorrect**: Check that the input text contains language-specific characters
3. **Style mapping not found**: Verify that the style term exists in the mapping table
4. **Batch editing fails**: Ensure image IDs are in the correct format (e.g., IMG-001)

### Logs

The scripts do not generate logs by default, but you can enable logging by adding the following to the scripts:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Future Enhancements

- Integration with OCR services for better text rendering analysis
- Machine learning model for improved style recommendations
- Support for additional languages and style profiles
- Web interface for easier script management
- Integration with cloud storage for persistent edit history