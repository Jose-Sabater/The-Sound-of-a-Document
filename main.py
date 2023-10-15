# Main logic for the project
import argparse
import logging
from logic import QuestionHandler


def setup_logging(verbose):
    # Set the logging level based on verbosity.
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(level=level, format="%(message)s")
    logging.debug("Logging is set to DEBUG mode")


def ask_question():
    question = input("Type your question: ")
    return question


def main():
    parser = argparse.ArgumentParser(description="Arguments for the text generation")
    # check if question is in args
    parser.add_argument(
        "-q", "--question", type=str, nargs="?", help="The question you want to ask"
    )
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="gpt-3.5-turbo",
        help="The model you want to use.",
    )
    # add verbosity
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increase output verbosity",
    )

    args = parser.parse_args()
    setup_logging(args.verbose)

    question = args.question if args.question else ask_question()
    model = args.model

    logging.debug(f"Your question is: {question}")
    logging.debug(f"Your model is: {model}")

    question_handler = QuestionHandler(question, model)

    answer = question_handler.get_answer()
    return answer


if __name__ == "__main__":
    answer = main()
    if answer["Missing_information"]:
        print("Missing information to answer the question. Please try again.")
        exit()
    print(answer["Answer"])
