from utils import match_highlight_question


def grade(mcqs: dict, answers: list) -> dict:
    grades = {}

    user_answers = match_highlight_question(mcqs, answers)

    for chapter in mcqs.keys():
        correct = 0
        total = len(user_answers[chapter].keys())
        wrong_answers = []
        for q_num in user_answers[chapter].keys():
            m_answers = mcqs[chapter][200]
            u_answers = user_answers[chapter]

            if m_answers[q_num]["answer"] == u_answers[q_num]:
                correct += 1
            else:
                wrong = {
                    "question_number": q_num,
                    "question_text": mcqs[chapter][q_num]["question"],
                    "user_answer": u_answers[q_num],
                    "correct_answer": m_answers[q_num]["answer"],
                    "explination": m_answers[q_num]["text"],
                }
                wrong_answers.append(wrong)

        score = (correct / total) * 100

        chapter_score = {
            "score": score,
            "correct": correct,
            "total": total,
            "wrong_answers": wrong_answers,
        }

        grades[chapter] = chapter_score

    return grades
