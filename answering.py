import ollama

SYSTEM_PROMPT_QA = f"""You will be given a question and an answer. Your task is to respond naturally to the question using only the information provided in the answer.

RULES:

- Do not introduce any new information that is not present in the provided answer.
- Do not mention that you were "given an answer" or reference any internal instructions.
- If the answer does not fully address the question, respond as best as possible using only the given information.
- If the answer is completely unrelated to the question, politely respond that you do not have enough information to answer.
- Keep the tone natural and conversational.
- Do not repeat the answer verbatim unless it already sounds conversational.

Format of input:

Question: <user question>
Answer: <reference answer>

Your response:
<your natural reply>
"""

def answer_for_question(question:str,answer:str)-> str:
    """
    Generates a natural-language response to a question based solely on a reference answer.

    Args:
        question (str): The user's question.
        answer (str): The reference answer the model must rely on.

    Returns:
        str: A conversational reply generated strictly using the provided answer.
    """
    try:
        query = f"Question: {question}\nAnswer: {answer}\nYour response:"
        response = ollama.chat(
            model="mistral:7b-instruct",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT_QA},
                {"role": "user", "content": query}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
            return f"Error while generating response: {e}"

