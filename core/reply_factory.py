
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    """
    Validates and stores the answer for the current question in the Django session.

    Args:
        answer (str): The user's answer.
        current_question_id (int): The ID of the current question.
        session (django.contrib.sessions.backends.base.SessionBase): The Django session.

    Returns:
        Tuple[bool, str]: A tuple indicating whether the answer was successfully recorded (True/False)
                         and an optional error message (empty string if no error).
    """
    try:
        # Validate the answer (you can customize this validation logic)
        # For example, check if the answer is not empty or meets specific criteria.
        if not answer:
            return False, "Answer cannot be empty."

        # Store the answer in the session (you can adapt this to your specific use case)
        session[f"question_{current_question_id}_answer"] = answer

        # Return success
        return True, ""
    except Exception as e:
        # Handle any unexpected errors (e.g., session storage failure)
        return False, f"Error: {str(e)}"


def get_next_question(current_question_id):
    """
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.

    Args:
        current_question_id (int): The ID of the current question.

    Returns:
        Tuple[str, int]: A tuple containing the next question (as a string) and the ID of the next question.
                        If there are no more questions, return an empty string and -1.
    """
    # Replace this with your actual list of quiz questions
    PYTHON_QUESTION_LIST = [
        "What is Python?",
        "What is a list comprehension?",
        "How does Python handle exceptions?",
        # Add more questions here...
    ]

    # Check if the current_question_id is within valid bounds
    if 0 <= current_question_id < len(PYTHON_QUESTION_LIST):
        next_question_id = current_question_id + 1
        return PYTHON_QUESTION_LIST[current_question_id], next_question_id
    else:
        # No more questions
        return "", -1


def generate_final_response(session, correct_answers):
    """
    Creates a final result message including a score based on the user's answers.

    Args:
        session (dict): The Django session containing user answers.
        correct_answers (list): A list of correct answers corresponding to each question.

    Returns:
        str: A result message with the user's score.
    """
    try:
        # Retrieve user answers from the session
        user_answers = [session.get(f"question_{i}_answer", "") for i in range(len(correct_answers))]

        # Calculate the score
        num_correct = sum(user_ans.lower() == correct_ans.lower() for user_ans, correct_ans in zip(user_answers, correct_answers))
        total_questions = len(correct_answers)
        score_percentage = (num_correct / total_questions) * 100

        # Generate the result message
        result_message = f"Your quiz score: {num_correct}/{total_questions} ({score_percentage:.2f}%)."

        # You can add more personalized feedback based on the score if desired

        return result_message
    except Exception as e:
        return f"Error calculating score: {str(e)}"
