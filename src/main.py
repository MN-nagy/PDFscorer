import argparse
import fitz
from parser import parse_mcqs, parse_mcqs_all
from highlight_poc import extract_highlight, extract_highlight_all


def main():
    parser = argparse.ArgumentParser(description="PDF MCQ parser + scorer")
    parser.add_argument("pdf_file", help="Path to the PDF file")
    parser.add_argument(
        "--page-start",
        type=int,
        default=0,
        help="Page number to start from (default: 0)",
    )
    parser.add_argument(
        "--page-end",
        type=int,
        default=None,
        help="Page number to end at (default: end of document)",
    )
    parser.add_argument(
        "--chapter-num",
        type=int,
        default=0,
        help="Chapter number to get score for",
    )
    parser.add_argument(
        "-w", "--whole", action="store_true", help="Process the entire PDF file"
    )
    parser.add_argument(
        "-f", "--file", action="store_true", help="Show score and answers in a file"
    )
    parser.add_argument(
        "-t",
        "--terminal",
        action="store_true",
        help="Show score and answers in terminal",
    )
    args = parser.parse_args()

    # Handle PDF logic
    doc = fitz.open(args.pdf_file)

    # if args.whole:
    #     mcqs = parse_mcqs_all(doc)
    #     highlights = extract_highlight_all(doc)
    # else:
    #     mcqs = parse_mcqs(doc, args.page_start, args.page_end)
    #     highlights = extract_highlight(doc, args.page_start, args.page_end)

    mcqs = parse_mcqs_all(doc)
    highlights = extract_highlight_all(doc)

    doc.close()


if __name__ == "__main__":
    main()
