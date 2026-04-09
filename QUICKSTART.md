# Quick Start Guide

## Local Testing (Before Deployment)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Locally

```bash
python app.py
```

The app will start on `http://localhost:7860`

**Note**: First run will download the model (~13GB for CodeLlama 7B), which may take several minutes.

### 3. Test the Interface

1. Open your browser to `http://localhost:7860`
2. Try one of the example problems
3. Click "Generate Test Cases"
4. Review the output and download JSON

---

## Deploy to Hugging Face Spaces

### Quick Deploy (5 minutes)

1. **Create Account**
   - Go to https://huggingface.co/join if you don't have an account

2. **Create New Space**
   - Visit https://huggingface.co/new-space
   - Name: `test-case-generator`
   - SDK: Select "Gradio"
   - Hardware: CPU basic (free)

3. **Upload Files**
   - Drag and drop these files:
     - `app.py`
     - `test_case_generator.py`
     - `requirements.txt`
     - `README.md`

4. **Wait for Build** (5-10 minutes)
   - Watch the "Logs" tab for progress
   - Space will auto-start when ready

5. **Test Your Space**
   - Click "App" tab
   - Try generating test cases
   - Share the URL with your team!

---

## Example Usage

### Example 1: Two Sum Problem

**Input:**
```
Problem: Two Sum

Given an array of integers nums and an integer target, 
return indices of the two numbers such that they add up to target.

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
```

**Generated Output:**
```json
{
  "normal_cases": [
    {
      "input": "nums = [2,7,11,15], target = 9",
      "expected_output": "[0,1]",
      "description": "Basic case with solution at beginning"
    }
  ],
  "edge_cases": [
    {
      "input": "nums = [3,3], target = 6",
      "expected_output": "[0,1]",
      "description": "Two identical numbers"
    }
  ],
  "boundary_cases": [
    {
      "input": "nums = [-1000000000, 1000000000], target = 0",
      "expected_output": "[0,1]",
      "description": "Maximum constraint values"
    }
  ]
}
```

---

## Integration with Your Pipeline

### Python Integration

```python
import requests
import json

# Your Hugging Face Space URL
API_URL = "https://YOUR_USERNAME-test-case-generator.hf.space/api/predict"

def generate_tests(problem_description):
    response = requests.post(
        API_URL,
        json={"data": [problem_description, "CodeLlama 7B (Fast)"]}
    )
    return response.json()

# Use it
problem = "Your problem description here..."
test_cases = generate_tests(problem)
print(json.dumps(test_cases, indent=2))
```

### Automated Grading System Integration

```python
import json
from your_grading_system import evaluate_submission

# Load generated test cases
with open('test_cases.json', 'r') as f:
    test_cases = json.load(f)

# Run all test cases
for category in ['normal_cases', 'edge_cases', 'boundary_cases']:
    for test in test_cases[category]:
        result = evaluate_submission(
            input_data=test['input'],
            expected=test['expected_output']
        )
        print(f"{test['description']}: {'PASS' if result else 'FAIL'}")
```

---

## Tips for Best Results

1. **Be Specific**: Include exact input/output formats
2. **List Constraints**: Specify ranges, sizes, data types
3. **Provide Examples**: Show 1-2 example cases if available
4. **Describe Edge Cases**: Mention special scenarios you care about
5. **Use Clear Language**: Avoid ambiguous problem statements

---

## Troubleshooting

### Model Loading is Slow
- **First time**: Model downloads (~13GB), wait 5-10 minutes
- **Subsequent times**: Should be fast (model cached)
- **Solution**: Use GPU hardware for faster loading

### Generation Takes Too Long
- **CPU**: 30-60 seconds is normal
- **Solution**: Upgrade to GPU hardware in Space settings

### JSON Output is Incomplete
- **Cause**: Token limit reached
- **Solution**: Increase `max_tokens` in test_case_generator.py

### Out of Memory Error
- **Cause**: Model too large for hardware
- **Solution**: Use CPU basic with CodeLlama 7B only, or upgrade hardware

---

## Next Steps

- Read [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions
- Check [config.md](config.md) for configuration options
- Review the code in `test_case_generator.py` to customize prompts
- Join the Hugging Face community for support

---

## Support & Feedback

- Issues: Create an issue in your Space repository
- Questions: Ask in Hugging Face Forums
- Documentation: https://huggingface.co/docs/hub/spaces

Happy Testing!
