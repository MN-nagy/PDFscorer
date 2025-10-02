import unittest
import fitz
from src.highlight_poc import extract_highlight
from pathlib import Path

script_dir = Path(__file__).resolve().parent

pdf_file = script_dir / "MCQ-example1-1-17.pdf"

doc = fitz.open(pdf_file)


class TestUtils(unittest.TestCase):

    def test_highlight_extraction(self):
        answers = extract_highlight(doc, 0, 1)

        highlighted = "b) Company sells directly to qualified buyers"

        self.assertEqual(answers[0], highlighted)
        self.assertEqual(len(answers), 5)

    def test_wrong_start_end(self):
        answers = extract_highlight(doc, 2, 2)
        answers_two = extract_highlight(doc, 12, 11)
        answers_three = extract_highlight(doc, 12, -1)
        answers_four = extract_highlight(doc, -12, 1)

        self.assertEqual(answers, [])
        self.assertEqual(answers_two, [])
        self.assertEqual(answers_three, [])
        self.assertEqual(answers_four, [])

    def test_highlight_extraction_all(self):
        answers = extract_highlight(doc)

        highlighted = "Offline customer service activities"

        self.assertEqual(answers[-1], highlighted)
        self.assertEqual(len(answers), 6)


if __name__ == "__main__":
    unittest.main()
    doc.close()
