import json
import re
from typing import Dict, List, Any
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


class TestCaseGenerator:
    """
    Automated Test Case Generator using Large Language Models
    Generates normal, edge, and boundary/stress test cases from problem descriptions
    """

    def __init__(self, model_name: str = "codellama/CodeLlama-7b-Instruct-hf"):
        """
        Initialize the test case generator with a specified model

        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"Loading model: {model_name}")
        print(f"Using device: {self.device}")

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Load model with optimizations for CPU/GPU
        if self.device == "cuda":
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                load_in_8bit=True,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name, torch_dtype=torch.float32, low_cpu_mem_usage=True
            )

        print("Model loaded successfully!")

    def create_prompt(self, problem_description: str) -> str:
        """
        Create a structured prompt for test case generation

        Args:
            problem_description: The programming problem description

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an expert test case generator for programming problems. Given a problem description, generate comprehensive test cases in JSON format.

Problem Description:
{problem_description}

Generate test cases in the following JSON structure:
{{
  "normal_cases": [
    {{"input": "...", "expected_output": "...", "description": "..."}}
  ],
  "edge_cases": [
    {{"input": "...", "expected_output": "...", "description": "..."}}
  ],
  "boundary_cases": [
    {{"input": "...", "expected_output": "...", "description": "..."}}
  ]
}}

Rules:
1. Normal cases: Typical inputs that follow the expected format
2. Edge cases: Unusual inputs like empty arrays, single elements, special characters
3. Boundary cases: Limits of constraints (min/max values, large inputs, stress tests)
4. Provide at least 3 test cases for each category
5. Include clear descriptions for each test case
6. Output ONLY valid JSON, no additional text

Generate the test cases:"""

        return prompt

    def generate_test_cases(
        self, problem_description: str, max_tokens: int = 2048
    ) -> Dict[str, Any]:
        """
        Generate test cases for a given problem description

        Args:
            problem_description: The programming problem description
            max_tokens: Maximum tokens to generate

        Returns:
            Dictionary containing structured test cases
        """
        try:
            # Create prompt
            prompt = self.create_prompt(problem_description)

            # Tokenize input
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_tokens,
                    temperature=0.7,
                    top_p=0.95,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                )

            # Decode output
            generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract JSON from the generated text
            test_cases = self.extract_json(generated_text)

            # Validate and structure the output
            structured_output = self.validate_and_structure(test_cases)

            return structured_output

        except Exception as e:
            print(f"Error generating test cases: {e}")
            return self.get_default_structure()

    def extract_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON from generated text

        Args:
            text: Generated text containing JSON

        Returns:
            Parsed JSON dictionary
        """
        try:
            # Find JSON in the text
            json_match = re.search(r"\{[\s\S]*\}", text)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                return self.get_default_structure()
        except json.JSONDecodeError:
            print("Failed to parse JSON, using default structure")
            return self.get_default_structure()

    def validate_and_structure(self, test_cases: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and ensure proper structure of test cases

        Args:
            test_cases: Raw test cases dictionary

        Returns:
            Validated and structured test cases
        """
        required_keys = ["normal_cases", "edge_cases", "boundary_cases"]

        # Ensure all required keys exist
        for key in required_keys:
            if key not in test_cases:
                test_cases[key] = []

        # Validate each test case has required fields
        for category in required_keys:
            if not isinstance(test_cases[category], list):
                test_cases[category] = []

            validated_cases = []
            for case in test_cases[category]:
                if isinstance(case, dict):
                    validated_case = {
                        "input": case.get("input", ""),
                        "expected_output": case.get("expected_output", ""),
                        "description": case.get("description", ""),
                    }
                    validated_cases.append(validated_case)

            test_cases[category] = validated_cases

        return test_cases

    def get_default_structure(self) -> Dict[str, Any]:
        """
        Get default test case structure

        Returns:
            Default structured dictionary
        """
        return {
            "normal_cases": [
                {
                    "input": "Example input",
                    "expected_output": "Example output",
                    "description": "Basic test case - please provide a valid problem description",
                }
            ],
            "edge_cases": [
                {
                    "input": "Edge input",
                    "expected_output": "Edge output",
                    "description": "Edge case - please provide a valid problem description",
                }
            ],
            "boundary_cases": [
                {
                    "input": "Boundary input",
                    "expected_output": "Boundary output",
                    "description": "Boundary case - please provide a valid problem description",
                }
            ],
        }

    def generate_and_format(self, problem_description: str) -> str:
        """
        Generate test cases and return as formatted JSON string

        Args:
            problem_description: The programming problem description

        Returns:
            Formatted JSON string
        """
        test_cases = self.generate_test_cases(problem_description)
        return json.dumps(test_cases, indent=2)
