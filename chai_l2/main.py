import time
import os
from db_wrappers.mongodb_manager import MongoDBManager


def main():
    """
    Main function to run the Chai AI chat application with MongoDB.
    """
    print("Welcome to Chai (MongoDB Edition)!")

    # Update this connection string for your MongoDB setup
    # For local: "mongodb://localhost:27017/"
    # For Atlas: "mongodb+srv://username:password@cluster.mongodb.net/"

    # example for Mongo Atlas
    # **IMPORTANT** You must set the environment variable MONGO_KEY from your terminal if you are using Atlas
    # This is something that does not persist from one terminal session to another, so remember to do it!
    # For Windows Command Prompt: set MONGO_KEY=password_here
    # For Windows PowerShell: $env:MONGO_KEY = "password_here"
    # For Mac/Linux: export MONGO_KEY="password_here"
    #user = "tom" # replace with your username in Atlas
    #password = os.getenv("MONGO_KEY")
    #Edit the url to use the url it gives you - remember to enter username and password as is done below
    #connection_string = f"mongodb+srv://{user}:{password}@cluster0.3walskx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # example for Local mongodb
    connection_string = "mongodb://localhost:27017/"

    db_manager = MongoDBManager(connection_string=connection_string, database_name="chai_db")

    user_id = input("Please enter your user ID to begin: ")

    threads = db_manager.list_user_threads(user_id) 

    for i, thread_name in enumerate(threads):
        print(f"{i}. {thread_name}")
    print(f"{len(threads)}. Create new thread")
    user_selection = input("Enter a thread number:")

    if not user_selection.isdigit():
        print("Not a number, exiting")
        return

    choice = int(user_selection)

    if choice > len(threads):
        print("Selection is too large of a number")
        return

    thread_name = ""
    if not threads or choice == len(threads):
        # prompt for thread name
        thread_name = input("Enter thread name:")
        # Store new thread name
        db_manager.save_conversation(user_id, thread_name, [])
    else:
        thread_name = threads[choice]

    run_chat(db_manager, user_id, thread_name)

    db_manager.close()


def run_chat(db_manager: MongoDBManager, user_id: str, thread_name: str) -> None:
    """
    Runs the chat loop for a specific conversation thread.
    """
    start_time = time.perf_counter()
    messages = db_manager.get_conversation(user_id, thread_name)
    end_time = time.perf_counter() 
    duration = end_time - start_time

    if messages:
        print(f"\n--- Conversation History ({len(messages)} messages) ---")
        for message in messages:
            role = message['role'].capitalize()
            print(f"{role}: {message['content']}")
        print(f"Load time: {duration:.4f} seconds\n")

    print(f"Conversation: '{thread_name}'. Type 'exit' to quit.")

    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        start_time = time.perf_counter()

        # Append user message
        user_message = {"role": "user", "content": user_input}
        db_manager.append_message(user_id, thread_name, user_message)

        # Create and append AI response
        ai_response = "This is a mock response from the AI."
        ai_message = {"role": "assistant", "content": ai_response}
        db_manager.append_message(user_id, thread_name, ai_response)

        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"AI: {ai_response}")
        print(f"(Operation took {duration:.4f} seconds)")


if __name__ == "__main__":
    main()