"""Test Cases for all functions"""
import sys
import project
sys.path.insert(1, "/Users/aryanmalhotra/Desktop/cs222/course-project-pynance/main")

def test_exists():
    """Tests the exists function"""
    print("Running test_exists()...")
    print(".....\n"*3)
    stock_names = ["GOOG", "AAPL","UAL","VWAGY","TSLA","AMZN"]
    expected_results = [True, False, False, False, True, True]
    actual_results = []
    for i in stock_names:
        result = project.exists(i)
        actual_results.append(result)
    for i,j in enumerate(expected_results):
        assert actual_results[i] == expected_results[i]
        j += '1'
        j -= '1'
    print("test_exists(): ALL ASSERTIONS PASSED")

test_exists()
