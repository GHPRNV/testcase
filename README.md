---
title: Automated Test Case Generator
emoji: 🧪
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.19.2
app_file: app.py
pinned: false
license: mit
python_version: 3.10
---

# Automated Test Case Generator

An AI-powered system that automatically generates comprehensive test cases for programming problems using Large Language Models.

## Features

- Generates three types of test cases:
  - **Normal Cases**: Typical inputs following expected format
  - **Edge Cases**: Unusual inputs like empty arrays, single elements
  - **Boundary Cases**: Limits of constraints and stress tests

- Structured JSON output for seamless integration
- Multiple model options (CodeLlama, Mistral)
- User-friendly Gradio interface
- Download test cases as JSON

## Usage

1. Select your preferred model
2. Enter a programming problem description
3. Click "Generate Test Cases"
4. Review and download the JSON output

## Model Options

- **CodeLlama 7B**: Fastest, good for quick generation
- **CodeLlama 13B**: Better quality, slightly slower
- **Mistral 7B**: Alternative model with different style

## JSON Output Format

```json
{
  "normal_cases": [
    {
      "input": "...",
      "expected_output": "...",
      "description": "..."
    }
  ],
  "edge_cases": [...],
  "boundary_cases": [...]
}
```

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

## License

MIT License
