from difflib import SequenceMatcher


def normalize_text(s: str) -> str:
    return s.strip(" :.,;'\"").lower()


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


# TODO: index out of range fix
def number_answers(mcqs: dict, answers: list) -> dict:
    numbered_answers = {}
    i = 0
    for chapter in mcqs.keys():
        if chapter not in numbered_answers:
            numbered_answers[chapter] = {}
        for q_number in mcqs[chapter]:
            numbered_answers[chapter][q_number] = answers[i]
            i += 1
    return numbered_answers
