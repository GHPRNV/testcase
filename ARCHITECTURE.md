# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Interface                           │
│                      (Gradio Web App)                            │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────────┐    │
│  │  Problem   │  │    Model     │  │    Example          │    │
│  │  Input     │  │  Selection   │  │    Problems         │    │
│  └────────────┘  └──────────────┘  └─────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Test Case Generator                           │
│                  (Core Logic Layer)                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  1. Receive Problem Description                           │  │
│  │  2. Create Structured Prompt                              │  │
│  │  3. Tokenize Input                                        │  │
│  │  4. Generate with LLM                                     │  │
│  │  5. Extract & Validate JSON                               │  │
│  │  6. Structure Output                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LLM Backend                                 │
│                  (Hugging Face Models)                           │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐    │
│  │ CodeLlama   │  │ CodeLlama    │  │    Mistral         │    │
│  │   7B        │  │   13B        │  │     7B             │    │
│  └─────────────┘  └──────────────┘  └────────────────────┘    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Output Layer                               │
│  ┌──────────────────┐  ┌────────────────┐  ┌──────────────┐   │
│  │   Formatted      │  │   JSON Code    │  │   Download   │   │
│  │   Display        │  │   Viewer       │  │   Button     │   │
│  └──────────────────┘  └────────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌──────────────┐
│   User       │
│   Input      │
└──────┬───────┘
       │
       │ Problem Description
       ▼
┌──────────────────┐
│  Prompt          │
│  Engineering     │
└──────┬───────────┘
       │
       │ Structured Prompt
       ▼
┌──────────────────┐
│  Tokenization    │
└──────┬───────────┘
       │
       │ Token IDs
       ▼
┌──────────────────┐
│  LLM Inference   │
│  (CodeLlama)     │
└──────┬───────────┘
       │
       │ Generated Text
       ▼
┌──────────────────┐
│  JSON            │
│  Extraction      │
└──────┬───────────┘
       │
       │ Raw JSON
       ▼
┌──────────────────┐
│  Validation &    │
│  Structuring     │
└──────┬───────────┘
       │
       │ Validated JSON
       ▼
┌──────────────────┐
│  Output          │
│  Formatting      │
└──────┬───────────┘
       │
       │ Display + Download
       ▼
┌──────────────────┐
│   User           │
│   Review         │
└──────────────────┘
```

## Component Interaction

```
app.py
  │
  ├─> initialize_model()
  │    │
  │    └─> TestCaseGenerator.__init__()
  │         │
  │         ├─> Load Tokenizer
  │         └─> Load Model (8-bit quantized)
  │
  └─> generate_test_cases()
       │
       ├─> TestCaseGenerator.generate_test_cases()
       │    │
       │    ├─> create_prompt()
       │    ├─> tokenize()
       │    ├─> model.generate()
       │    ├─> extract_json()
       │    └─> validate_and_structure()
       │
       └─> format_test_cases_display()
            │
            └─> Return (Markdown, JSON)
```

## JSON Schema

```
{
  "type": "object",
  "properties": {
    "normal_cases": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "input": {"type": "string"},
          "expected_output": {"type": "string"},
          "description": {"type": "string"}
        },
        "required": ["input", "expected_output", "description"]
      }
    },
    "edge_cases": {
      "type": "array",
      "items": { /* same as normal_cases */ }
    },
    "boundary_cases": {
      "type": "array",
      "items": { /* same as normal_cases */ }
    }
  },
  "required": ["normal_cases", "edge_cases", "boundary_cases"]
}
```

## Deployment Architecture (Hugging Face Spaces)

```
┌─────────────────────────────────────────────────────────────┐
│                    Hugging Face Space                        │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │               Docker Container                      │    │
│  │                                                     │    │
│  │  ┌──────────────────────────────────────────┐     │    │
│  │  │         Python 3.10 Runtime              │     │    │
│  │  │                                          │     │    │
│  │  │  ┌────────────┐  ┌──────────────────┐  │     │    │
│  │  │  │   app.py   │  │  test_case_      │  │     │    │
│  │  │  │            │  │  generator.py    │  │     │    │
│  │  │  └────────────┘  └──────────────────┘  │     │    │
│  │  │                                          │     │    │
│  │  │  ┌────────────────────────────────┐    │     │    │
│  │  │  │    HuggingFace Models          │    │     │    │
│  │  │  │    (Cached in /models)         │    │     │    │
│  │  │  └────────────────────────────────┘    │     │    │
│  │  └──────────────────────────────────────────┘     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              Hardware Layer                         │    │
│  │  CPU Basic / CPU Upgrade / GPU T4 / GPU A10G      │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    Internet Users                            │
│         https://huggingface.co/spaces/USERNAME/SPACE        │
└─────────────────────────────────────────────────────────────┘
```

## Optimization Techniques

```
┌─────────────────────────────────────────────┐
│         Model Optimizations                  │
├─────────────────────────────────────────────┤
│ • 8-bit Quantization (50% memory reduction) │
│ • Device Auto-detection (CPU/GPU)           │
│ • Lazy Loading (load on first request)      │
│ • Model Caching (HF automatic)              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│       Generation Optimizations               │
├─────────────────────────────────────────────┤
│ • Temperature tuning (0.7)                  │
│ • Top-p sampling (0.95)                     │
│ • Max tokens limit (2048)                   │
│ • Early stopping on JSON completion         │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│          UI Optimizations                    │
├─────────────────────────────────────────────┤
│ • Pre-loading default model                 │
│ • Async generation (non-blocking UI)        │
│ • Progressive display (streaming)           │
│ • Example problem templates                 │
└─────────────────────────────────────────────┘
```

## Error Handling Flow

```
generate_test_cases()
  │
  ├─ Try: Generate with LLM
  │   │
  │   ├─ Success → Extract JSON
  │   │              │
  │   │              ├─ Valid JSON → Validate Structure
  │   │              │                │
  │   │              │                ├─ Valid → Return
  │   │              │                └─ Invalid → Fix & Return
  │   │              │
  │   │              └─ Invalid JSON → Return Default
  │   │
  │   └─ Exception → Log Error → Return Default
  │
  └─ Return: Structured JSON (always)
```

## Scaling Considerations

```
┌───────────────────────────────────────────────────┐
│              Traffic Level                         │
├───────────────────────────────────────────────────┤
│ Low (< 100 req/day)    → CPU Basic (Free)        │
│ Medium (100-1k req/day) → CPU Upgrade or GPU T4  │
│ High (> 1k req/day)     → GPU T4/A10G + Caching  │
│ Very High (> 10k/day)   → Multiple instances     │
└───────────────────────────────────────────────────┘

┌───────────────────────────────────────────────────┐
│           Scaling Strategies                       │
├───────────────────────────────────────────────────┤
│ 1. Horizontal: Multiple HF Spaces w/ load balancer│
│ 2. Vertical: Upgrade to larger GPU                │
│ 3. Caching: Store common problem test cases       │
│ 4. Async: Queue system for batch processing       │
└───────────────────────────────────────────────────┘
```

## Integration Points

```
┌──────────────────────────────────────────────────┐
│         External System Integration               │
├──────────────────────────────────────────────────┤
│                                                   │
│  REST API                                         │
│  ├─ POST /api/predict                            │
│  └─ Response: JSON test cases                    │
│                                                   │
│  Python SDK                                       │
│  ├─ TestCaseGenerator class                      │
│  └─ Direct programmatic access                   │
│                                                   │
│  CLI Tool (optional future feature)              │
│  └─ testgen --problem "description"              │
│                                                   │
│  GitHub Action (optional future feature)         │
│  └─ Auto-generate tests on PR                    │
│                                                   │
└──────────────────────────────────────────────────┘
```

## Technology Stack

```
┌────────────────────────────────────────┐
│         Frontend Layer                  │
│  • Gradio 4.19.2                       │
│  • HTML/CSS (auto-generated)           │
│  • JavaScript (Gradio built-in)        │
└────────────────────────────────────────┘
           ▼
┌────────────────────────────────────────┐
│         Application Layer               │
│  • Python 3.10                         │
│  • Custom business logic               │
│  • Error handling & validation         │
└────────────────────────────────────────┘
           ▼
┌────────────────────────────────────────┐
│         ML/AI Layer                     │
│  • Transformers 4.38.1                 │
│  • PyTorch 2.2.0                       │
│  • Accelerate 0.27.2                   │
│  • Bitsandbytes 0.42.0                 │
└────────────────────────────────────────┘
           ▼
┌────────────────────────────────────────┐
│         Model Layer                     │
│  • CodeLlama 7B/13B                    │
│  • Mistral 7B                          │
│  • 8-bit quantized                     │
└────────────────────────────────────────┘
           ▼
┌────────────────────────────────────────┐
│         Infrastructure Layer            │
│  • Hugging Face Spaces                 │
│  • Docker containers                   │
│  • CPU/GPU hardware                    │
└────────────────────────────────────────┘
```

This architecture provides a scalable, maintainable, and production-ready system for automated test case generation.
