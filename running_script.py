from read_mac import SystemMonitor
from understand_question import ask
from replying import answer_for_question

print("\nInteractive Q&A Mode. Type 'exit' to quit.\n")
monitor = SystemMonitor()
while True:
    question = input("You: ")
    if question.lower() in ["exit", "quit"]:
        print("\t\t\t\t\t\tGoodbye!")
        break

    # verify question
    context = ask(question)
    answer = ""
    if type(context) == list:
        for metric in context:
            answer += monitor.get_report(metric)
    else:
        print("Mac Assist:", context, "\n")
        continue
    reply = answer_for_question(question, answer)

    print("Mac Assist:", reply, "\n")