import unittest
import fitz
from src.highlight_poc import extract_highlight


pdf_file = "/mnt/e/ArchForTests/MCQ-example1.pdf"

doc = fitz.open(pdf_file)


class TestUtils(unittest.TestCase):

    def test_highlight_extraction(self):
        answers = extract_highlight(doc, 0, 1)

        highlighted = "b) Company sells directly to qualified buyers"
        self.assertEqual(answers[0], highlighted)
        self.assertEqual(len(answers), 5)


if __name__ == "__main__":
    unittest.main()
    doc.close()
