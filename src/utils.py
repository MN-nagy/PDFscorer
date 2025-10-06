from difflib import SequenceMatcher


def normalize_text(s: str) -> str:
    return s.strip(" :.,;'\"").lower()


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize_text(a), normalize_text(b)).ratio()


def match_highlight_question(mcqs: dict, answers: list) -> dict:
    matched = {}

    for chapter in mcqs.keys():
        if chapter not in matched:
            matched[chapter] = {
                q_num: "No Answer" for q_num in mcqs[chapter].keys() if q_num != 200
            }
        for highlight in answers:
            flag = 0
            best_match = {
                "score": 0.7,
                "q_num": 0,
                "q_answer": "",
            }
            for question in mcqs[chapter].keys():
                if question == 200:
                    continue
                for option, text in mcqs[chapter][question]["options"].items():
                    q_score = similarity(text, highlight)
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


def get_page_from_to(match: str, keys: list) -> tuple[int, int]:
    start = 0
    end = 0

    indecator = 0
    for key in keys:
        if match == key:
            break
        indecator += 1

    # wrong chapter number proccess whole chapter
    if indecator > len(keys) - 1:
        end = 0
    # proccess last chapter
    elif indecator == len(keys) - 1:
        start = indecator
        end = 0
    # proccess any other chapter
    elif indecator < len(keys) - 1:
        start = indecator
        end = indecator + 1

    return start, end


def log_data(chapter: str, chapter_answers: dict, wrong: bool) -> None:

    print(f" -- Chapter {chapter} grades")

    print(" " * 20)
    print(f" Score: {int(chapter_answers["score"])}%")
    print(f" Correct Answers: {chapter_answers["correct"]} ")
    print(f" Total Questions: {chapter_answers["total"]} ")

    if wrong:
        print(f" Wrongly Answered Questions: ")
        print(" " * 20)

        for answer in chapter_answers["wrong_answers"]:
            print(" " * 20)

            print(f" Question Number: {answer["question_number"]}")
            print(f" Question: {answer["question_text"]}")
            print(f" Your Answer: {answer["user_answer"]}")
            print(f" Correct Answer: {answer["correct_answer"]}")
            print(f"  -> {answer["explination"]}")

            print("_" * 20)
            print(" " * 20)
