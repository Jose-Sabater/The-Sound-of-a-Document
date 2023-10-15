import streamlit as st
from logic import QuestionHandler


def get_answer_for_question(question: str, model: str = "gpt-3.5-turbo") -> dict:
    """call the logic to get the answer to the question"""
    question_handler = QuestionHandler(question, model)
    answer = question_handler.get_answer()
    return answer


def main():
    """
    This function creates a Streamlit app for a question-answering system. It allows the user to input a question,
    select a model to use, and get an answer. It also displays previous questions and answers.

    Returns:
    None
    """
    st.title("Question-Answering App")

    # Input for the user to type in their question
    question = st.text_input("Enter your question:")

    # Model selection
    model = st.selectbox(
        "Select the model you want to use:",
        ["gpt-3.5-turbo"],
    )

    # Button to get the answer
    if st.button("Get Answer"):
        if question:
            answer = get_answer_for_question(question, model)
            if answer["Missing_information"]:
                st.warning(
                    "Missing information to answer the question. Please try again."
                )
            else:
                st.write(f"Answer: {answer['Answer']}")
        else:
            st.warning("Please enter a question.")

    # Display past questions and answers
    with st.expander("Previous Questions and Answers"):
        # Store questions and answers in session state
        if not hasattr(st.session_state, "qa_pairs"):
            st.session_state.qa_pairs = []

        for qa_pair in st.session_state.qa_pairs:
            st.write(f"Q: {qa_pair['question']}")
            st.write(f"A: {qa_pair['answer']}")

        # Update session state with current question and answer
        if question:
            st.session_state.qa_pairs.append(
                {
                    "question": question,
                    "answer": get_answer_for_question(question, model).get(
                        "Answer", ""
                    ),
                }
            )


if __name__ == "__main__":
    main()
