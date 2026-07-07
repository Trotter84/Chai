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

    # --- TODO 1: Instantiate the Database Wrapper ---
    # Create an instance of the FlatFileManager, passing the user_id to it.
    # This object will handle all our file reading and writing.
    # Specify the storage directory as "data"
    db_manager = None # fixme!

    # --- TODO 6 (do this last): Create a way for a user_id to have multiple conversation threads
    # Requirements:
    #   - If user already exists, then have the user select which thread (conversation_id) they want to use
    #       - Give the option to use a new thread
    #   - Proceed to run_chat() with the correct conversation_id
    #   Hint: This is not a "clean" addition, you may need to restructure how data is stored and indexed
    #         There are many ways to do this. Devise a plan and implement your own solution.

    conversation_id = f"{user_id}_conversation"
    run_chat(db_manager, conversation_id)

def run_chat(db_manager: FlatFileManager, conversation_id: str) -> None:
    # --- TODO 2: Check if conversation already exists, printout conversation if so ---
    #   - Add a timer that times how long it took to use get_conversation and print the results after
    start_time = None # fixme!
    messages = None # fixme!
    end_time = None # fixme!
    duration = None # fixme!
    if messages:
        for message in messages:
            print(message)
        print(f"Load time: {duration:.4f} seconds")

    print(f"Conversation: '{conversation_id}'. Type 'exit' to quit.")

    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # --- TODO 3: Start the performance timer ---
        # Record the start time before performing the database operations.
        # Use time.perf_counter() for high precision.
        start_time = None # fixme!

        # --- TODO 4: Implement the Read-Append-Write Cycle ---
        # 1. Get the entire conversation history from the file.
        if not messages:
            messages = None # fixme!

        # 2. Append the new user message to the list of messages using messages.append()
        #    Each message should be a dictionary, e.g., {"role": "user", "content": user_input}
        messages.append() # fixme!

        # 3. Create a mock AI response and append it to the list.
        #    The AI response should also be a dictionary using format: {"role": "assistant", "content": ai_response}
        ai_response = "This is a mock response from the AI."
        messages.append() # fixme!

        # 4. Save the *entire*, updated list of messages back to the file.
        #    Call your db_manager's save method.
        relative_filepath = f"{conversation_id}.json"
        # fixme! use db manager save method here

        # ----------------------------------------------------

        # --- TODO 5: Stop the timer and calculate duration ---
        # Record the end time and calculate the difference to see how long the
        # entire read-append-write cycle took.
        end_time = None # fixme!
        duration = None # fixme!
        # ---------------------------------------------------

        print(f"AI: {ai_response}")
        print(f"(Operation took {duration:.4f} seconds)")


if __name__ == "__main__":
    main()