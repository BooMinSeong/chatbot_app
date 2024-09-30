import os
import glob
from datetime import datetime

class ChatLogHandle:
    def __init__(self):
        """
        Initializes the ChatLogHandle object by setting the save path and preparing to handle chat history.
        """
        self.save_path = _get_save_path()
        self.max_cached_files = 10  # Maximum number of cached files allowed to retain
        self.filename = f'cached_chatlog_{datetime.now().strftime("%Y-%m-%d_%H-%M")}.jsonl'

        # cleaning cached file
        self.cleanup_cached_files()

    def _get_save_path(self):
        path = os.getenv('CACHE_PATH')
        if not path:
            raise EnvironmentError("SAVE_PATH environment variable not set.")
        if not os.path.isdir(self.save_path):  # Ensure the path exists and is a directory
            raise FileNotFoundError(f"Cache directory '{self.save_path}' does not exist.")
        return path
        
    def _del_cached_chatlog(self):
        """
        Deletes the cached chat log file if it exists.
        """
        if self.save_path:
            cached_file = os.path.join(self.save_path, self.filename)  # Define path to cached file
            try:
                if os.path.exists(cached_file):  # Check if file exists before attempting to delete
                    os.remove(cached_file)
                    print_info("Cached chat log deleted.")
                else:
                    print_info("No cached chat log found.")
            except Exception as e:
                print_error(f"Failed to delete cached chat log: {e}")

    def load_cached_chatlog(self, prefix='cached_chatlog'):
        """
        Loads the latest cached chat log based on the provided prefix.
        """
        if self.save_path:
            cached_files = glob.glob(os.path.join(self.save_path, f'{prefix}*.md'))  # Get matching files
            if cached_files:
                latest_file = max(cached_files, key=os.path.getctime)  # Find the latest file by creation time
                try:
                    with open(latest_file, 'r') as file:  # Read contents of the latest chat log
                        chat_history = [json.loads(line) for line in file] # jsonl 파일 로딩 방식 확인하기
                    print_info(f"Loaded history from {latest_file}.")
                except Exception as e:
                    print_error(f"Failed to load cached chat log: {e}")
            else:
                print_info("No cached chat log found.")

        return chat_history

    def save_chatlog(self,chat_history):
        """
        Saves the current chat history to a new file with a timestamped filename.
        """

        # Create a filename with the current timestamp
        file_path = os.path.join(self.save_path, self.filename)
        
        self._del_cached_chatlog()

        try:
            with open(file_path, 'w') as file:  # Write the chat history to the new file
                for message in chat_history:
                    file.write(json.dumps(message)+"\n") # jsonl 파일 제대로 저장되는지 확인

            print_info(f"Chat log saved to {file_path}.")
            self.cleanup_cached_files()  # Clean up old cached files

        except Exception as e:
            print_error(f"Failed to save chat log: {e}")

    def cleanup_cached_files(self):
        """
        Deletes the oldest cached files if the total number exceeds the limit.
        """
        # Get a sorted list of cached files, sorted by modification time
        cached_files = sorted(glob.glob(os.path.join(self.save_path, 'cached_chatlog_*.jsonl')),
                              key=os.path.getmtime)

        # If the number of cached files exceeds the allowed limit, delete the oldest
        while len(cached_files) > self.max_cached_files:
            try:
                os.remove(cached_files[0])  # Remove the oldest file
                print_info(f"Deleted oldest cached file: {cached_files[0]}")
                cached_files.pop(0)  # Remove the filename from the list
            except Exception as e:
                print_error(f"Failed to delete cached file: {e}")


