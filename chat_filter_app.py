import tkinter as tk
from tkinter import filedialog, Text, ttk
import os
import re
import json

class ChatFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Chat Log Filter")
        self.root.geometry("600x500")

        # Load previous settings
        self.settings_file = "settings.json"
        self.load_settings()

        # Button to select file
        self.file_button = tk.Button(root, text="Select a .txt file", command=self.select_file)
        self.file_button.pack(pady=10)

        # Text box for usernames input
        self.username_entry_label = tk.Label(root, text="Enter usernames to keep (space-separated):")
        self.username_entry_label.pack()
        self.username_entry = tk.Entry(root, width=50)
        self.username_entry.pack()
        self.username_entry.insert(0, self.settings.get("usernames", ""))  # Pre-fill with previous usernames

        # Frame for radio buttons
        self.reduce_frame = tk.Frame(root)
        self.reduce_frame.pack(pady=5)

        # Radio buttons for reducing content
        self.reduce_var = tk.StringVar(value=self.settings.get("reduce_option", "none"))
        self.reduce_recent_radio = tk.Radiobutton(self.reduce_frame, text="Keep most recent messages", variable=self.reduce_var, value="recent")
        self.reduce_oldest_radio = tk.Radiobutton(self.reduce_frame, text="Keep oldest messages", variable=self.reduce_var, value="oldest")
        self.reduce_recent_radio.pack(side=tk.LEFT, padx=5)
        self.reduce_oldest_radio.pack(side=tk.LEFT, padx=5)

        # Checkbox for removing excess whitespace
        self.remove_whitespace_var = tk.BooleanVar(value=self.settings.get("remove_whitespace", False))
        self.remove_whitespace_checkbox = tk.Checkbutton(root, text="Remove excess whitespace", variable=self.remove_whitespace_var)
        self.remove_whitespace_checkbox.pack(pady=5)

        # Checkbox for excluding date stamps
        self.exclude_dates_var = tk.BooleanVar(value=self.settings.get("exclude_dates", False))
        self.exclude_dates_checkbox = tk.Checkbutton(root, text="Exclude date stamps", variable=self.exclude_dates_var)
        self.exclude_dates_checkbox.pack(pady=5)

        # Button to process file
        self.process_button = tk.Button(root, text="Process File", command=self.process_file)
        self.process_button.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=400)
        self.progress.pack(pady=10)

        # Result display box
        self.result_text = Text(root, height=8, width=70, state="disabled")
        self.result_text.pack(pady=10)

        self.file_path = None

    def select_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.file_path:
            self.file_button.config(text=f"File selected: {self.file_path.split('/')[-1]}")

    def process_file(self):
        if not self.file_path:
            self.show_message("No file selected!")
            return

        usernames = self.username_entry.get().strip().split()
        if not usernames:
            self.show_message("No usernames entered!")
            return

        try:
            # Save settings
            self.save_settings(usernames)

            # Create output directory if it doesn't exist
            os.makedirs("output", exist_ok=True)

            with open(self.file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Read header and store to add back later
            header = []
            for i, line in enumerate(lines):
                if line.strip() == "":
                    header = lines[:i + 1]
                    lines = lines[i + 1:]
                    break

            # Set progress bar max value to the number of lines
            self.progress["maximum"] = len(lines)

            # Filter the chat log
            filtered_lines = self.filter_chat(lines, usernames)

            # Truncate content based on user selection
            if self.reduce_var.get() == "recent":
                filtered_lines = self.truncate_to_keep_recent(header + filtered_lines)
            elif self.reduce_var.get() == "oldest":
                filtered_lines = self.truncate_to_keep_oldest(header + filtered_lines)

            # Remove excess whitespace if the checkbox is selected
            if self.remove_whitespace_var.get():
                filtered_lines = self.remove_excess_whitespace(header + filtered_lines)

            # Exclude date stamps if the checkbox is selected
            if self.exclude_dates_var.get():
                filtered_lines = self.exclude_date_stamps(header + filtered_lines)

            # Combine header and filtered lines into the result text
            result_text = ''.join(filtered_lines)

            # Save the result to a new file in the output folder
            output_file_path = os.path.join("output", "filtered_chat_log.txt")
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result_text)

            # Reset progress bar and display completion message in result box
            self.progress["value"] = 0
            self.show_message(f"File saved to: {output_file_path}")

        except Exception as e:
            self.show_message(f"Error processing file: {str(e)}")

    def filter_chat(self, lines, usernames):
        user_pattern = re.compile(r"\[.*?\] (\S+)")
        filtered_lines = []
        current_message_block = []

        for line in lines:
            match = user_pattern.match(line)
            if match:
                if current_message_block:
                    filtered_lines.append('\n'.join(current_message_block) + '\n')  # Separate messages by new lines
                    current_message_block = []
                username = match.group(1)
                if username in usernames:
                    message = line.split(']', 1)[-1].strip()  # Get the message content without the date
                    current_message_block.append(message)
            elif current_message_block:
                current_message_block.append(line.strip())  # Add message contents

            # Update the progress bar with each line processed
            self.progress.step(1)
            self.root.update_idletasks()

        if current_message_block:
            filtered_lines.append('\n'.join(current_message_block) + '\n')  # Add the last message block

        return filtered_lines

    def truncate_to_keep_recent(self, content_lines):
        """Remove content to keep within 16,000 characters for ChatGPT's context window."""
        max_characters = 16000
        content = ''.join(content_lines)
        if len(content) > max_characters:
            return [content[-max_characters:]]  # Keep the most recent messages
        return content_lines

    def truncate_to_keep_oldest(self, content_lines):
        """Remove content to keep within 16,000 characters for ChatGPT's context window."""
        max_characters = 16000
        content = ''.join(content_lines)
        if len(content) > max_characters:
            return [content[:max_characters]]  # Keep the oldest messages
        return content_lines

    def remove_excess_whitespace(self, content_lines):
        """Remove empty lines and reduce multiple spaces to a single space."""
        content = ''.join(content_lines)
        content = re.sub(r'\n\s*\n', '\n', content)  # Remove empty lines
        content = re.sub(r'\s+', ' ', content)  # Replace multiple spaces with a single space
        return [content]

    def exclude_date_stamps(self, content_lines):
        """Remove date stamps from messages while keeping them distinct."""
        user_pattern = re.compile(r"\[.*?\]")
        filtered_lines = []

        for line in content_lines:
            if user_pattern.match(line):
                message = line.split(']', 1)[-1].strip()  # Get the message content without the date
                filtered_lines.append(message + '\n')  # Append message without date
            else:
                filtered_lines.append(line)  # Non-matching lines (like header)

        return filtered_lines

    def load_settings(self):
        """Load previous settings from a JSON file."""
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.settings = json.load(f)
        else:
            self.settings = {}

    def save_settings(self, usernames):
        """Save current settings to a JSON file."""
        settings = {
            "usernames": ' '.join(usernames),
            "reduce_option": self.reduce_var.get(),
            "remove_whitespace": self.remove_whitespace_var.get(),
            "exclude_dates": self.exclude_dates_var.get(),
        }
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f)

    def show_message(self, message):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
        self.result_text.config(state="disabled")

# Run the application
root = tk.Tk()
app = ChatFilterApp(root)
root.mainloop()
