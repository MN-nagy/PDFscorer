import argparse
import os
import fitz
from parser import parse_mcqs_all
from highlight_poc import extract_highlight
from quiz import grade
from utils import get_page_from_to, log_data


def main():
    parser = argparse.ArgumentParser(description="PDF MCQ parser + scorer")

    parser.add_argument("pdf_file", help="Path to the PDF file")

    parser.add_argument(
        "chapter_num",
        type=int,
        nargs="?",
        default=0,
        help="Chapter number to get score for (proccess whole file if not provided)",
    )

    parser.add_argument(
        "-w",
        "--wrong",
        action="store_true",
        help="Print wrongly answered questins with answers",
    )

    args = parser.parse_args()
    file_path = os.path.abspath(args.pdf_file)

    # Handle PDF logic
    doc = fitz.open(file_path)

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

    if args.chapter_num:
        chapter_answers = grades[str(args.chapter_num)]
        log_data(str(args.chapter_num), chapter_answers, args.wrong)
    else:
        for chapter in grades:
            chapter_answers = grades[chapter]
            log_data(chapter, chapter_answers, args.wrong)

    doc.close()


if __name__ == "__main__":
    main()
