import re


def parse_mcqs_all(doc, start: int = 0, end: int = 0) -> dict:

    if end == 0:
        end = len(doc)

    if start >= end or start < 0 or end < 0:
        return {}

    mcqs = {}
    current_chapter = None
    model_answer = None
    current_q = None
    q_text = ""
    current_options = {}
    last_seen = ""

    for page_num in range(start, end):
        page = doc[page_num]
        text = page.get_text("text").strip()

        lines = text.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Match chapter "Chapter 1"
            chapter_match = re.match(r"^Chapter\s+(\d+)", line)
            if chapter_match:
                current_chapter = chapter_match.group(1)
                if current_chapter not in mcqs:
                    mcqs[current_chapter] = {}
                continue

            # Gured for None current_chapter
            if current_chapter is None:
                continue

            # Match model answer
            model_match = re.match(r"^Model Answer.*$", line)
            if model_match:
                model_answer = 200
                if model_answer not in mcqs:
                    mcqs[current_chapter][model_answer] = {}
                continue

            if model_answer:
                ans_match = re.match(r"^(\d+)\.\s*([a-zA-Z])\)\s*(.+)$", line)
                if ans_match:
                    number = int(ans_match.group(1))
                    answer = ans_match.group(2).lower()
                    text = ans_match.group(3)
                    mcqs[current_chapter][model_answer][number] = {
                        "answer": answer,
                        "text": text,
                    }
                    last_seen = "model"
                    continue

            # Match question start "1)"
            q_match = re.match(r"^(\d+)\)\s*(.+)$", line)
            if q_match:
                if current_q is not None and current_chapter is not None:
                    mcqs[current_chapter][current_q] = {
                        "question": q_text,
                        "options": current_options,
                    }
                current_q = int(q_match.group(1))
                q_text = q_match.group(2).strip()
                current_options = {}
                last_seen = "question"
                continue

            # Match options "a)"
            # No need for seperate logic to handle multi option lines PyMuPDF handles it (maybe)
            opt_match = re.match(r"^([a-zA-Z])\)\s*(.+)$", line)
            if opt_match and current_q is not None:
                opt_letter = opt_match.group(1).lower()
                opt_text = opt_match.group(2).strip()
                current_options[opt_letter] = opt_text
                last_seen = "option"
                continue

            # if not opt_match and not q_match:
            if current_q is not None:
                if last_seen == "question":
                    q_text += " " + line.strip()
                elif last_seen == "option":
                    last_key = list(current_options.keys())[-1]
                    current_options[last_key] += " " + line.strip()
                elif last_seen == "model":
                    last_key = list(mcqs[current_chapter][model_answer].keys())[-1]
                    mcqs[current_chapter][model_answer][last_key]["text"] += (
                        " " + line.strip()
                    )

        if current_q is not None and current_chapter is not None:
            mcqs[current_chapter][current_q] = {
                "question": q_text,
                "options": current_options,
            }
            current_q = None

    return mcqs
