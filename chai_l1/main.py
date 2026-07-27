import time
import os
from db_wrappers.flat_file_manager import FlatFileManager

def main():
    """
    Main function to run the Chai AI chat application.
    Handles the REPL (Read-Eval-Print Loop) for user interaction.
    """
    print("Welcome to Chai!")
    user_id = input("Please enter your user ID to begin: ")

    db_manager = FlatFileManager(storage_dir="data")
    
    conversation_id = f"{user_id}_conversation"

    existing_threads = db_manager.list_threads(conversation_id)

    if existing_threads:
        print(f"\n{len(existing_threads)} existing thread{'s' if len(existing_threads) > 1 else ''} found.")
        for i, option in enumerate(existing_threads, start=1):
            print(f"\t{i}. {option}")
        new_thread = len(existing_threads) + 1
        print(f"\t{new_thread}. new conversation")
        print(f"\t0. exit")

        user_choice = input("> ").strip()
        
        try:
            choice_int = int(user_choice)
        except:
            choice_int = new_thread
            
        if choice_int == 0:
            quit()
            
        if 1 <= choice_int <= len(existing_threads):
            thread_id = existing_threads[choice_int - 1]
        else:
            thread_id = f"thread_{new_thread:03d}"
    else:
        thread_id = "thread_001"
        
    run_chat(db_manager, user_id, conversation_id, thread_id)
    

def run_chat(db_manager: FlatFileManager, user_id: str, conversation_id: str, thread_id: str) -> None:
    start_time = time.perf_counter()
    messages = db_manager.get_conversation(conversation_id, thread_id)
    end_time = time.perf_counter()
    duration = end_time - start_time

    if messages:
        for message in messages:
            print(f"{message['role']}:\n\t\"{message['content']}\"")
        print(f"Load time: {duration:.4f} seconds")

    print(f"Conversation: '{conversation_id}'. Type 'exit' to quit.")

    while True:
        user_input = input("> ")
        if user_input.lower().strip() == 'exit' or user_input.lower().strip() == 'bye' or user_input.lower().strip() == 'goodbye':
            print("Goodbye!")
            break

        start_time = time.perf_counter()

        if not messages:
            messages = db_manager.get_conversation(conversation_id, thread_id)

        messages.append({"role": "user", "content": user_input})

        ai_response = f"Good afternoon, {user_id}"
        messages.append({"role": "assistant", "content": ai_response})

        relative_filepath = f"{conversation_id}.json"
        db_manager.save_conversation(conversation_id, relative_filepath, thread_id, messages)


        end_time = time.perf_counter()
        duration = end_time - start_time

        print(f"AI: {ai_response}")
        print(f"(Operation took {duration:.4f} seconds)")


if __name__ == "__main__":
    main()