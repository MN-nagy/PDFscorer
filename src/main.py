import argparse
from parser import parse_mcqs
from highlight_poc import extract_highlight


def main():
    parser = argparse.ArgumentParser(description="PDF MCQ parser + scorer")
    parser.add_argument("pdf_file", help="path to pdf file")
    parser.add_argument(
        "-t", "--terminal", action="store_true", help="Show score + answers in terminal"
    )
    parser.add_argument(
        "-f", "--file", action="store_true", help="Show score + answers in terminal"
    )
    args = parser.parse_args()

    # Get pdf
    import fitz

    doc = fitz.open(args.pdf_file)

    mcqs = parse_mcqs(doc)
    highlights = extract_highlight(doc)

    score = 0
    correct = 0
    wrong = []
