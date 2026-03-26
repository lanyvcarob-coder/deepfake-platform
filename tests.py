import unittest
from deepfake import analyze_file

class TestDeepfake(unittest.TestCase):
    def test_analysis_output(self):
        result = analyze_file("test.jpg")
        self.assertIn("deepfake_probability", result)
        self.assertIn("explanation", result)

if __name__ == "__main__":
    unittest.main()
