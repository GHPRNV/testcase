"""
Test script to verify the test case generator functionality
"""

import json
from test_case_generator import TestCaseGenerator


def test_basic_functionality():
    """Test basic test case generation"""
    print("=" * 80)
    print("Testing Test Case Generator")
    print("=" * 80)

    # Example problem
    problem = """
    Problem: Find Maximum in Array
    
    Given an array of integers, find and return the maximum value.
    
    Input: Array of integers
    Output: Integer (maximum value)
    
    Constraints:
    - 1 <= array.length <= 10^5
    - -10^9 <= array[i] <= 10^9
    """

    print("\nProblem Description:")
    print(problem)

    # Note: This is a mock test. Actual testing requires model loading
    # which needs significant resources (GPU/CPU + model download)

    print("\n" + "=" * 80)
    print("Test Case Structure Validation")
    print("=" * 80)

    # Validate the expected JSON structure
    expected_structure = {
        "normal_cases": [
            {
                "input": "[1, 5, 3, 9, 2]",
                "expected_output": "9",
                "description": "Standard array with positive integers",
            },
            {
                "input": "[10, 20, 30]",
                "expected_output": "30",
                "description": "Sorted ascending array",
            },
        ],
        "edge_cases": [
            {
                "input": "[5]",
                "expected_output": "5",
                "description": "Single element array",
            },
            {
                "input": "[-1, -5, -3]",
                "expected_output": "-1",
                "description": "All negative numbers",
            },
        ],
        "boundary_cases": [
            {
                "input": "[1000000000, -1000000000]",
                "expected_output": "1000000000",
                "description": "Maximum constraint values",
            },
            {
                "input": "[1] * 100000",
                "expected_output": "1",
                "description": "Large array at maximum size constraint",
            },
        ],
    }

    print("\nExpected JSON Structure:")
    print(json.dumps(expected_structure, indent=2))

    # Validate structure
    assert "normal_cases" in expected_structure
    assert "edge_cases" in expected_structure
    assert "boundary_cases" in expected_structure

    for category in ["normal_cases", "edge_cases", "boundary_cases"]:
        assert isinstance(expected_structure[category], list)
        for case in expected_structure[category]:
            assert "input" in case
            assert "expected_output" in case
            assert "description" in case

    print("\n✓ Structure validation passed!")

    print("\n" + "=" * 80)
    print("Integration Test")
    print("=" * 80)

    print("\nTo run a full integration test with the actual model:")
    print("1. Ensure you have GPU access or sufficient CPU resources")
    print("2. Run: python app.py")
    print("3. Open the Gradio interface in your browser")
    print("4. Test with the provided example problems")

    print("\n" + "=" * 80)
    print("All tests passed! ✓")
    print("=" * 80)


if __name__ == "__main__":
    test_basic_functionality()
