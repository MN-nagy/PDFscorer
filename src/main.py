import argparse
import fitz
from parser import parse_mcqs, parse_mcqs_all
from highlight_poc import extract_highlight


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
        default=0,
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

    page_num_end = args.page_end
    if not args.page_end:
        page_num_end = len(doc)

    mcqs = parse_mcqs_all(doc)
    highlights = extract_highlight(doc, args.page_start, page_num_end)

    doc.close()


if __name__ == "__main__":
    main()
