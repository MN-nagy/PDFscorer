from difflib import SequenceMatcher


def normalize_text(s: str) -> str:
    return s.strip(" :.,;'\"").lower()


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def number_answers(mcqs: dict, answers: list) -> dict:
    numbered_answers = {}
    i = 0
    for key in mcqs.keys():
        if isinstance(key, str):
            if key not in numbered_answers:
                numbered_answers[key] = {}
            for q_number in mcqs[key]:
                if i < len(answers):
                    numbered_answers[key][q_number] = answers[i]
                    i += 1
                else:
                    numbered_answers[key][q_number] = "wrong"
        else:
            if i < len(answers):
                numbered_answers[key] = answers[i]
                i += 1
            else:
                numbered_answers[key] = "wrong"

    return numbered_answers
