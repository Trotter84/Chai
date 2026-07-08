import os
import json
import shutil
from typing import List


class FlatFileManager:
    """
    Manages storing and retrieving chat conversations in flat JSON files.
    """
    def __init__(self, storage_dir="data"):
        """
        Initializes the FlatFileManager for a specific user.

        Args:
            storage_dir (str): The unique identifier for the user.
        """
        self.storage_dir = storage_dir
        self._ensure_storage_exists()
        self.conversations_index = {} # Key: conversation_id => Value: Filepath
        self._init_index()

    def _ensure_storage_exists(self) -> None:
        os.makedirs(self.storage_dir, exist_ok=True)


    def _init_index(self) -> None:
        index_file = os.path.join(self.storage_dir, "conversations.json")
        if not os.path.exists(index_file):
            self.save_index()
        with open(index_file, "r") as file:
            self.conversations_index = json.load(file)

    def save_index(self) -> None:
        index_file = os.path.join(self.storage_dir, "conversations.json")
        with open(index_file, "w") as file:
            json.dump(self.conversations_index, file, indent=2)


    def get_conversation(self, conversation_id: str) -> List[any]:
        relative_filepath = self.conversations_index.get(conversation_id)
        if not relative_filepath:
            return []
        
        filepath = os.path.join(self.storage_dir, relative_filepath)

        try:
            with open(filepath, "r") as file:
                return json.load(file)
        except:
            print("There was an error loading conversation.")
            return []


    def save_conversation(self, conversation_id: str, relative_filepath: str, messages: List[any]) -> None:
        self.conversations_index[conversation_id] = relative_filepath
        self.save_index()
        
        filepath = os.path.join(self.storage_dir, relative_filepath)
        with open(filepath, "w") as file:
            json.dump(messages, file, indent=2)


    def run_tests(self):
        print("Testing FlatFileManager._ensure_storage_exists()")
        # manually check that file exists
        if not os.path.isdir(self.storage_dir):
            print("Failed to create directory!")
            return

        print("Testing FlatFileManager.save_conversation()")
        messages = [{"role": "user", "content": "hello world"}]
        conversation_id = "test_user"
        relative_filepath = "test_user.json"

        self.save_conversation(conversation_id, relative_filepath, messages)
        filepath = os.path.join(manager.storage_dir, relative_filepath)
        if not os.path.exists(filepath):
            print("Failed to save conversation!")
            return
        print("Successfully saved conversation!")

        print("Testing FlatFileManager.get_conversation()")
        read_messages = self.get_conversation(conversation_id)
        if not read_messages:
            print("Failed to get conversation!")
            return
        print("Successfully retrieved conversation!")

        try:
            shutil.rmtree(self.storage_dir)
            print("Deleted storage directory")
        except OSError as e:
            print(f"Failed to delete storage directory: {e}")

        print("All tests passed!")

if __name__ == "__main__":
    print("Testing FlatFileManager")
    manager = FlatFileManager(storage_dir="data_test")
    manager.run_tests()