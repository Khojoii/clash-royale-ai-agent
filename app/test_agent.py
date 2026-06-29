from app.agent.agent import invoke_agent

print("Clash Royale AI Coach - Interactive REPL")
print("Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ("quit", "exit"):
        break
    response = invoke_agent(user_input)
    print(f"\nCoach: {response}\n")
