import gradio as gr
import json
from test_case_generator import TestCaseGenerator
import os

# Initialize the generator (will be loaded when the app starts)
generator = None


def initialize_model(model_choice):
    """Initialize the model based on user selection"""
    global generator

    model_map = {
        "CodeLlama 7B (Fast)": "codellama/CodeLlama-7b-Instruct-hf",
        "CodeLlama 13B (Better)": "codellama/CodeLlama-13b-Instruct-hf",
        "Mistral 7B": "mistralai/Mistral-7B-Instruct-v0.2",
    }

    model_name = model_map.get(model_choice, "codellama/CodeLlama-7b-Instruct-hf")

    try:
        generator = TestCaseGenerator(model_name=model_name)
        return f"Model {model_choice} loaded successfully!"
    except Exception as e:
        return f"Error loading model: {str(e)}"


def generate_test_cases(problem_description, model_choice):
    """Generate test cases from problem description"""
    global generator

    if not problem_description.strip():
        return "Please provide a problem description.", ""

    # Initialize model if not already done
    if generator is None:
        status = initialize_model(model_choice)
        if "Error" in status:
            return status, ""

    try:
        # Generate test cases
        test_cases_dict = generator.generate_test_cases(problem_description)

        # Format as JSON
        json_output = json.dumps(test_cases_dict, indent=2)

        # Create a formatted display
        display_text = format_test_cases_display(test_cases_dict)

        return display_text, json_output

    except Exception as e:
        return f"Error generating test cases: {str(e)}", ""


def format_test_cases_display(test_cases):
    """Format test cases for display"""
    display = "# Generated Test Cases\n\n"

    categories = [
        ("normal_cases", "Normal Test Cases"),
        ("edge_cases", "Edge Test Cases"),
        ("boundary_cases", "Boundary/Stress Test Cases"),
    ]

    for key, title in categories:
        display += f"## {title}\n\n"
        cases = test_cases.get(key, [])

        if not cases:
            display += "No test cases generated for this category.\n\n"
            continue

        for i, case in enumerate(cases, 1):
            display += f"### Test Case {i}\n"
            display += f"**Description:** {case.get('description', 'N/A')}\n\n"
            display += f"**Input:**\n```\n{case.get('input', 'N/A')}\n```\n\n"
            display += f"**Expected Output:**\n```\n{case.get('expected_output', 'N/A')}\n```\n\n"
            display += "---\n\n"

    return display


def download_json(json_output):
    """Prepare JSON for download"""
    return json_output


# Example problems
EXAMPLES = [
    [
        """Problem: Two Sum
        
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

Constraints:
- 2 <= nums.length <= 10^4
- -10^9 <= nums[i] <= 10^9
- -10^9 <= target <= 10^9
- Only one valid answer exists."""
    ],
    [
        """Problem: Palindrome Checker

Write a function that takes a string as input and returns true if it's a palindrome, false otherwise. A palindrome is a word, phrase, or sequence that reads the same backward as forward.

Constraints:
- 1 <= s.length <= 1000
- s consists of only printable ASCII characters"""
    ],
    [
        """Problem: Binary Search

Implement binary search algorithm that finds the position of a target value within a sorted array.

Input: sorted array of integers, target integer
Output: index of target in array, or -1 if not found

Constraints:
- 1 <= array.length <= 10^4
- -10^4 <= array[i], target <= 10^4
- Array is sorted in ascending order"""
    ],
]

# Create Gradio interface
with gr.Blocks(title="Automated Test Case Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # Automated Test Case Generator
        
        Generate comprehensive test cases for programming problems using AI.
        
        This system uses Large Language Models to analyze problem descriptions and automatically generate:
        - **Normal Cases**: Typical inputs following expected format
        - **Edge Cases**: Unusual inputs like empty arrays, single elements, special characters
        - **Boundary Cases**: Limits of constraints (min/max values, large inputs, stress tests)
        
        The output is provided in strict JSON format for seamless integration into automated evaluation pipelines.
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            model_choice = gr.Dropdown(
                choices=["CodeLlama 7B (Fast)", "CodeLlama 13B (Better)", "Mistral 7B"],
                value="CodeLlama 7B (Fast)",
                label="Select Model",
                info="Choose the base model for test case generation",
            )

            problem_input = gr.Textbox(
                label="Problem Description",
                placeholder="Enter your programming problem description here...",
                lines=10,
                info="Provide a clear problem statement with constraints",
            )

            generate_btn = gr.Button(
                "Generate Test Cases", variant="primary", size="lg"
            )

            gr.Examples(
                examples=EXAMPLES, inputs=problem_input, label="Example Problems"
            )

        with gr.Column(scale=3):
            output_display = gr.Markdown(
                label="Generated Test Cases", value="Test cases will appear here..."
            )

    with gr.Row():
        json_output = gr.Code(
            label="JSON Output (Ready for Integration)", language="json", lines=15
        )

    with gr.Row():
        download_btn = gr.DownloadButton(label="Download JSON", value="test_cases.json")

    # Event handlers
    generate_btn.click(
        fn=generate_test_cases,
        inputs=[problem_input, model_choice],
        outputs=[output_display, json_output],
    )

    json_output.change(fn=lambda x: x, inputs=[json_output], outputs=[download_btn])

    gr.Markdown(
        """
        ---
        ### How to Use
        1. Select your preferred model (CodeLlama 7B is faster, 13B provides better quality)
        2. Enter your problem description with constraints
        3. Click "Generate Test Cases" and wait for results
        4. Review the generated test cases
        5. Download the JSON output for integration into your evaluation pipeline
        
        ### Tips for Best Results
        - Include clear problem constraints (input/output ranges, data types)
        - Specify edge cases you're particularly interested in
        - Provide examples if available
        - Be specific about input/output format
        """
    )

if __name__ == "__main__":
    # Pre-load the default model for faster first generation
    print("Pre-loading default model...")
    initialize_model("CodeLlama 7B (Fast)")

    # Launch the app
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
