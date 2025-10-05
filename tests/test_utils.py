import unittest
from src.utils import match_highlight_question, similarity
from src.parser import parse_mcqs_all
from src.highlight_poc import extract_highlight
import fitz
from pathlib import Path

script_dir = Path(__file__).resolve().parent

pdf_file = script_dir / "MCQ-example1-1-17.pdf"

doc = fitz.open(pdf_file)


class TestUtils(unittest.TestCase):

    def test_similar(self):
        sim = similarity(
            "b) Company sells directly to qualified buyers",
            "b) Company sells directly to qualified buyers",
        )

        sim_two = similarity(
            "b) Company sells directly to qualified buyers",
            "c) Combine both digital and physical operations",
        )

        self.assertEqual(sim, 1)
        self.assertEqual(sim_two, 0)

    def test_match_highlight_question(self):
        mcqs = parse_mcqs_all(doc, 0, 2)
        highlighted = extract_highlight(doc, 0, 2)

        matched = match_highlight_question(mcqs, highlighted)

        example = {
            "2": {
                1: "b",
                2: "b",
                3: "c",
                4: "b",
                5: "c",
                6: "c",
                7: -1,
                8: -1,
                9: -1,
                10: -1,
            }
        }

        self.assertEqual(example, matched)


if __name__ == "__main__":
    unittest.main()
    doc.close()
