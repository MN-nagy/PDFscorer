import fitz
import re
from collections import OrderedDict

pdf_file = "/mnt/e/ArchForTests/MCQ-example.pdf"

doc = fitz.open(pdf_file)


def parse_mcqs(text):
    lines = text.strip().split("\n")
    mcqs = OrderedDict()
    current_q = None
    q_text = ""
    current_options = {}
    last_seen = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Match question start "1)"
        q_match = re.match(r"^(\d+)\)\s*(.+)$", line)
        if q_match:
            if current_q is not None:
                mcqs[current_q] = {"question": q_text, "options": current_options}
            current_q = int(q_match.group(1))
            q_text = q_match.group(2).strip()
            current_options = {}
            last_seen = "question"
            continue

        # Match options "a)"
        opt_match = re.match(r"^([a-zA-Z])\)\s*(.+)$", line)
        if opt_match and current_q is not None:
            opt_letter = opt_match.group(1).lower()
            opt_text = opt_match.group(2).strip()
            current_options[opt_letter] = opt_text
            last_seen = "option"

        if not opt_match and not q_match:
            if last_seen == "question":
                q_text += " " + line.strip()
            elif last_seen == "option":
                last_key = list(current_options.keys())[-1]
                current_options[last_key] += " " + line.strip()

    if current_q is not None:
        mcqs[current_q] = {"question": q_text, "options": current_options}

    return mcqs


if doc:
    page_num = 1
    page = doc[page_num]
    page_text = page.get_text("text").strip()
    mcq_dict = parse_mcqs(page_text)

    print(mcq_dict)

doc.close()
