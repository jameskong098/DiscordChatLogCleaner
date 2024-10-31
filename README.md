# Discord Chat Filter GUI Application
James D. Kong

## Overview

This application is a GUI-based tool designed to streamline the process of extracting and filtering specific user messages from Discord chat logs for further analysis or fun simulations using AI tools like ChatGPT or Claude. By filtering messages from one or multiple users, you can reduce the text content to fit within the input constraints of these AI tools, enabling deeper insights or conversation simulations. 

## Purpose

By using this tool, you can:
- Extract only the messages of specific users, which allows for focused analysis or simulation.
- Optionally remove timestamps and extra spaces to maximize the content that fits into an AI’s context window.
- Control the volume of extracted messages by choosing to keep either the most recent or the earliest messages, which can be valuable for focusing on specific periods in a conversation.
- Quickly reapply your settings for streamlined processing using the saved configuration in a settings file.

## Requirements

- **[DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter)**: This application requires chat logs to be in `.txt` format, which you can obtain by exporting chats using DiscordChatExporter.
- **Python Environment**: Ensure that Python and the required packages are installed.
- **PyInstaller** (optional): To create an executable version of the application.

## Features

- **Drag-and-drop GUI**: Drag a Discord `.txt` file directly into the GUI.
- **User-Specific Filtering**: Input one or multiple usernames to filter messages exclusively from those users.
- **Output Settings**:
  - Remove timestamps (optional).
  - Remove extra spacing to save space in the AI context window.
  - Limit the messages to either the most recent or oldest messages based on your preference.
- **Saved Settings**: All configuration settings are saved automatically, making it easy to apply the same settings each time.

## How It Works

1. **Launch the Application**: Run the Python script or executable to open the GUI.
2. **Load a Discord Chat Log**: Drag and drop a `.txt` file (exported from DiscordChatExporter) into the application.
3. **Specify Usernames**: In the input box, enter the usernames whose messages you want to keep, separated by spaces.
4. **Adjust Filtering Options**:
   - Choose to remove timestamps.
   - Choose to remove extra line spacing.
   - Decide to keep the most recent or oldest messages.
5. **Process the File**: Press the "Filter Chat" button to start filtering. A progress bar will indicate processing status.
6. **View Output**: Once processing is complete, an output file will be created in the `output` folder. The exact location of the file will be displayed in the GUI’s results box.

## How to Run

Run the following command in your terminal:
```bash
python chat_filter_app.py
```

## Usage

1. Open the GUI.
2. Drag in a `.txt` chat log file.
3. Enter usernames, select options, and click "Filter Chat."
4. Use the generated filtered output with your preferred AI tool for insights or simulations!

## Notes
`settings.json`: The application automatically saves your selected options in a settings.json file located in the same directory as the script.
