from difflib import SequenceMatcher


def normalize_text(s: str) -> str:
    return s.strip(" :.,;'\"").lower()


def similarity(a: str, b: str) -> bool:
    sim = SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()
    if sim >= 0.7:
        return True
    return False


def match_highlight_question(mcqs: dict, answers: list) -> dict:
    matched = {}
    answer_index = 0

    for chapter in mcqs.keys():
        if chapter == 200:
            continue
        if chapter not in matched:
            matched[chapter] = {}
        for question in mcqs[chapter].keys():
            matched[chapter][question] = -1
            if answer_index >= len(answers):
                continue
            for option, text in mcqs[chapter][question]["options"].items():
                if similarity(text, answers[answer_index]):
                    matched[chapter][question] = option
                    answer_index += 1
                    break

    return matched


def score(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


def match_highlight_fallback(mcqs: dict, answers: list) -> dict:
    matched = {}

    for chapter in mcqs.keys():
        if chapter == 200:
            continue
        if chapter not in matched:
            matched[chapter] = {
                q_num: -1 for q_num in mcqs[chapter].keys() if q_num != 200
            }
        for highlight in answers:
            flag = 0
            best_match = {
                "score": 0.7,
                "q_num": 0,
                "q_answer": "",
            }
            for question in mcqs[chapter].keys():
                for option, text in mcqs[chapter][question]["options"].items():
                    q_score = score(text, highlight)
                    # to skip if a perfect match is found
                    if q_score >= 1:
                        matched[chapter][question] = option
                        flag = 1
                        break
                    if q_score > best_match["score"]:
                        best_match["score"] = q_score
                        best_match["q_num"] = question
                        best_match["q_answer"] = option
                if flag == 1:
                    break
            if flag == 0:
                matched[chapter][best_match["q_num"]] = best_match["q_answer"]

    return matched
