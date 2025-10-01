import unittest
from src.utils import number_answers
from src.parser import parse_mcqs
from src.highlight_poc import extract_highlight
import fitz


pdf_file = "/mnt/e/ArchForTests/MCQ-example.pdf"

doc = fitz.open(pdf_file)


class TestUtils(unittest.TestCase):

    # TODO: finish test
    def test_number_list(self):
        mcqs = parse_mcqs(doc, 0, 17)
        answers = extract_highlight(doc, 0, 17)

        numbered = number_answers(mcqs, answers)
        numbers = {
            "2": {
                "1": "b) Company sells directly to qualified buyers",
                "2": "b) Operate only locally",
                "3": "c) Combine both digital and physical operations",
                "4": "b) Enhancing social media likes",
                "5": "c) Increase the cost of marketing",
            },
        }
        self.assertEqual(numbered, numbers)


if __name__ == "__main__":
    unittest.main()
    doc.close()
