from read_mac import SystemMonitor
from understand_question import ask
from answering import answer_for_question


def interactive_mode() -> None:
    """
    Launches an interactive Q&A loop where users can ask system-related questions.
    Type 'exit' or 'quit' to stop the program.
    """
    print("\n=== Hello !! Ask me about my battery,disk and memory metrics ===")
    print("Type 'exit' or 'quit' to end the session.\n")

    monitor = SystemMonitor()

    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nMac Assist: Session terminated.\n")
            break

        if question.lower() in {"exit", "quit"}:
            print("\nMac Assist: Goodbye!\n")
            break

        context = ask(question)

        if isinstance(context, list):
            answer = "".join(monitor.get_report(metric) for metric in context)
            reply = answer_for_question(question, answer)
            print("Mac Assist:", reply, "\n")
        else:
            print("Mac Assist:", context, "\n")


if __name__ == "__main__":
    interactive_mode()
