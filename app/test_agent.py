from app.agent.agent import simple_agent

while True:
    user_input = input("User: ")
    response = simple_agent(user_input)
    print("Agent:", response)