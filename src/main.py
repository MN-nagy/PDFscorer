import argparse
import fitz
from parser import parse_mcqs_all
from highlight_poc import extract_highlight
from quiz import grade
from utils import get_page_from_to


def main():
    parser = argparse.ArgumentParser(description="PDF MCQ parser + scorer")

    parser.add_argument("pdf_file", help="Path to the PDF file")

    parser.add_argument(
        "--chapter-num",
        type=int,
        default=0,
        help="Chapter number to get score for (proccess whole file if not provided)",
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

    mcqs, chapter_pages = parse_mcqs_all(doc)
    highlights_to_proccess = []

    if args.chapter_num and str(args.chapter_num) in mcqs.keys():
        mcq_to_proccess = {str(args.chapter_num): mcqs[str(args.chapter_num)]}
        start, end = get_page_from_to(str(args.chapter_num), list(mcqs.keys()))
        highlights_to_proccess = extract_highlight(
            doc, chapter_pages[start], chapter_pages[end]
        )
    else:
        mcq_to_proccess, chapter_pages = parse_mcqs_all(doc)
        highlights_to_proccess = extract_highlight(doc)

    grades = grade(mcq_to_proccess, highlights_to_proccess)

    for key, value in grades.items():
        # TODO: implement logic to log this info
        pass

    doc.close()


if __name__ == "__main__":
    main()
