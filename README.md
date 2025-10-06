PDF Scorer 📝
PDF Scorer is a command-line tool that automatically grades multiple-choice question (MCQ) quizzes from a PDF file. It intelligently parses questions, options, and model answer keys directly from the document's text. It then matches a user's highlighted answers to the corresponding questions to calculate a score and provide a detailed report on any incorrect answers.

## Features
- **Automatic PDF Parsing:** Reads a PDF and uses regular expressions to intelligently extract chapters, questions, options, and model answer keys.  
- **Highlight Extraction:** Scans a PDF for highlight annotations and extracts the user's chosen answers in the correct, top-to-bottom order.  
- **Robust Answer Matching:** Uses a "best match" algorithm (`difflib.SequenceMatcher`) to accurately link each highlighted answer to its correct question, robustly handling imprecise highlights or skipped questions.  
- **Chapter-Specific Grading:** Can grade an entire multi-chapter document or focus on a single chapter specified by the user.  
- **Detailed Grade Reports:** Provides a summary of the score, total questions, and correct answers. It can also generate a detailed list of incorrectly answered questions with the user's answer, the correct answer, and the explanation.  

## Requirements
- Python 3.13+  
- `uv` (for environment and package management)  
- `PyMuPDF`  
- `pytest` (for development)  

## Installation
Clone the repository:
```bash
git clone <your-repository-url>
cd PDFscorer
```

Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate
```

Install the required dependencies:
```bash
uv pip install -e .
```

## Usage
The tool is run from the command line, pointing it to a PDF file. You can specify a chapter to grade or have it grade the entire document.

### Command Format
```bash
python src/main.py <path_to_pdf> [chapter_number] [-w]
```

### Arguments
- **pdf_file:** (Required) The path to the answered MCQ PDF file.  
- **chapter_num:** (Optional) The chapter number you wish to grade. If not provided, the entire document will be graded.  
- **-w, --wrong:** (Optional) A flag to display a detailed breakdown of all incorrectly answered questions.  

### Examples
1. Grade Chapter 2 of a PDF:
   ```bash
   python src/main.py "tests/MCQ-example1-1-17.pdf" 2
   ```

2. Grade Chapter 2 and show a detailed report of wrong answers:
   ```bash
   python src/main.py "tests/MCQ-example1-1-17.pdf" 2 -w
   ```

3. Grade all chapters in the entire document:
   ```bash
   python src/main.py "path/to/your/full_document.pdf"
   ```

## How It Works
The scoring process is handled in a multi-stage pipeline:

1. **Parsing (`src/parser.py`):**  
   The script first performs a full pass on the PDF document. It uses regular expressions to identify structural elements like `Chapter X`, question numbers `(1)`, `(2)`, options `(a)`, `(b)`, and the `Model Answer` section. This is all organized into a structured Python dictionary, which also tracks the starting page of each chapter.

2. **Highlight Extraction (`src/highlight_poc.py`):**  
   The PDF is scanned for highlight annotations. The text content within the bounding box of each highlight is extracted and sorted by its position on the page to ensure the correct order.

3. **Matching (`src/utils.py`):**  
   This is the core of the logic. To handle skipped questions or imprecise highlights, a highlight-centric "best match" algorithm is used. For each highlight, the script calculates its text similarity (`SequenceMatcher.ratio()`) against every single option in the target chapter, finding the one with the highest score above a set threshold (70%).

4. **Grading (`src/quiz.py`):**  
   Once each highlight is confidently matched to a question, the user's answers are compared against the parsed model answers. The script calculates the final score and compiles a list of any incorrect answers.

5. **Reporting (`src/main.py` & `src/utils.py`):**  
   The final grade data is formatted into a clean, human-readable report and printed to the terminal.

## Running Tests
The project includes a suite of unit tests to ensure the parser, highlight extractor, and utility functions work as expected. To run them, execute the provided shell script:
```bash
sh test.sh
```

## Project Structure
```
PDFscorer/
├── src/
│   ├── __init__.py
│   ├── main.py             # Main CLI entry point
│   ├── parser.py           # Logic for parsing MCQs from PDF
│   ├── highlight_poc.py    # Logic for extracting PDF highlights
│   ├── quiz.py             # Logic for grading answers
│   └── utils.py            # Helper functions (matching, reporting)
├── tests/
│   ├── test_highlight.py
│   ├── test_parser.py
│   ├── test_utils.py
│   └── MCQ-example1-1-17.pdf # PDF for testing
├── pyproject.toml          # Project configuration and dependencies
├── README.md
├── test.sh                 # Test runner script
└── uv.lock
```

