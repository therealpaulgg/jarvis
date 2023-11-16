from assistant.ai_model import Jarvis

jarvis_instance = Jarvis()

conversation_active = True

while conversation_active:
    user_input = input("You (type 'exit' to exit): ")
    if user_input == "exit":
        conversation_active = False
    else:
        jarvis_instance.new_command(user_input)