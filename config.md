# Configuration for Test Case Generator

## Model Configuration

# Available models and their characteristics
MODELS = {
    "codellama-7b": {
        "name": "codellama/CodeLlama-7b-Instruct-hf",
        "size": "7B parameters",
        "memory": "~14GB",
        "recommended_hardware": "CPU Basic or GPU T4",
        "speed": "Fast",
        "quality": "Good"
    },
    "codellama-13b": {
        "name": "codellama/CodeLlama-13b-Instruct-hf",
        "size": "13B parameters",
        "memory": "~26GB",
        "recommended_hardware": "GPU T4 or A10G",
        "speed": "Medium",
        "quality": "Better"
    },
    "mistral-7b": {
        "name": "mistralai/Mistral-7B-Instruct-v0.2",
        "size": "7B parameters",
        "memory": "~14GB",
        "recommended_hardware": "CPU Basic or GPU T4",
        "speed": "Fast",
        "quality": "Good"
    }
}

## Generation Configuration

# Default generation parameters
DEFAULT_MAX_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.95

# Test case requirements
MIN_NORMAL_CASES = 3
MIN_EDGE_CASES = 3
MIN_BOUNDARY_CASES = 3

## Hardware Recommendations

# For Hugging Face Spaces
HARDWARE_RECOMMENDATIONS = {
    "cpu_basic": {
        "models": ["codellama-7b", "mistral-7b"],
        "expected_time": "30-60 seconds per generation",
        "cost": "Free"
    },
    "cpu_upgrade": {
        "models": ["codellama-7b", "mistral-7b"],
        "expected_time": "15-30 seconds per generation",
        "cost": "~$0.03/hour"
    },
    "gpu_t4": {
        "models": ["codellama-7b", "codellama-13b", "mistral-7b"],
        "expected_time": "5-10 seconds per generation",
        "cost": "~$0.60/hour"
    },
    "gpu_a10g": {
        "models": ["codellama-13b"],
        "expected_time": "3-5 seconds per generation",
        "cost": "~$3.15/hour"
    }
}

## Environment Variables (Optional)

# Set these in your Hugging Face Space Settings → Variables and secrets

# HF_TOKEN - Your Hugging Face access token (for private models)
# MODEL_NAME - Override default model
# MAX_TOKENS - Override default max tokens
# TEMPERATURE - Override default temperature
