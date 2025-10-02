import unittest
import fitz
from src.parser import parse_mcqs, parse_mcqs_all


pdf_file = "/mnt/e/ArchForTests/MCQ-example1.pdf"
pdf_file_sec = "/mnt/e/ArchForTests/MCQ-example1-1-17.pdf"

doc = fitz.open(pdf_file)
doc_sec = fitz.open(pdf_file_sec)


class TestUtils(unittest.TestCase):

    def test_parsing_mcqs(self):
        parsed = parse_mcqs(doc, 0, 1)

        mcq_one = {
            "question": "Which of the following is a feature of a sell-side e-marketplace?",
            "options": {
                "a": "Open marketplace for all buyers",
                "b": "Company sells directly to qualified buyers",
                "c": "Multi-vendor auction",
                "d": "Physical storefront only",
            },
        }
        self.assertEqual(parsed[1], mcq_one)
        self.assertEqual(len(parsed.keys()), 5)

    def test_parse_modle_answer(self):
        parsed = parse_mcqs_all(doc_sec)

        mcq_one = {
            "question": "Which of the following is a feature of a sell-side e-marketplace?",
            "options": {
                "a": "Open marketplace for all buyers",
                "b": "Company sells directly to qualified buyers",
                "c": "Multi-vendor auction",
                "d": "Physical storefront only",
            },
        }

        print(parsed)

        self.assertEqual(next(iter(parsed.keys())), "2")
        self.assertEqual(len(parsed["2"].keys()), 86)
        self.assertEqual(parsed["2"][1], mcq_one)


if __name__ == "__main__":
    unittest.main()
    doc.close()
    doc_sec.close()
