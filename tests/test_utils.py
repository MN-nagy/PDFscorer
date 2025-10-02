import unittest
from src.utils import number_answers
from src.parser import parse_mcqs
from src.highlight_poc import extract_highlight
import fitz


pdf_file = "/mnt/e/ArchForTests/MCQ-example1-1-17.pdf"

doc = fitz.open(pdf_file)


class TestUtils(unittest.TestCase):

    def test_number_list(self):
        mcqs = parse_mcqs(doc, 0, 1)
        highlighted = extract_highlight(doc, 0, 1)

        numbered_q = number_answers(mcqs, highlighted)

        numbered_q_example = {
            1: "b) Company sells directly to qualified buyers",
            2: "b) Operate only locally",
            3: "c) Combine both digital and physical operations",
            4: "b) Enhancing social media likes",
            5: "c) Increase the cost of marketing",
        }

        self.assertEqual(numbered_q, numbered_q_example)


if __name__ == "__main__":
    unittest.main()
    doc.close()
