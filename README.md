# Simple File Transfer Chat

## Description
This is a simple Python-based command-line chat application that allows users to chat with each other and transfer files. It uses **sockets** and **threading** to establish connections and handle multiple tasks simultaneously.

## Requirements
- Python 3 and above

## Usage
1. Run the `chat_program.py` script in the terminal.
   ```sh
   python chat_program.py
   ```
2. Enter your name, which will be displayed in the chat.
3. The program will display the **port number** it is listening on. Make a note of this number.
4. Enter the **target port number** to connect to another user running the same script.
5. Start **chatting** and **transferring files**.

## Commands
| Command | Description |
|---------|-------------|
| `transfer <filename>` | Transfer a file to the connected user. Replace `<filename>` with the name of the file you want to transfer. The file should be located in the same directory as the script. |
| `exit` | Close the connection and exit the chat. |

## Functionality
- **`handle_write(sock, sender_name)`**: Handles sending messages and file transfers to the connected user.
- **`handle_read(sock)`**: Handles receiving messages and file transfers from the connected user.
- **`main()`**: The main function that initializes the sockets, establishes connections, and creates the reading and writing threads.

## Notes
1. The transferred file will be saved in the same directory as the script with the prefix **`new_`** added to the original filename.
2. The chat application works on **localhost** (same machine). To use it over a network, replace `"localhost"` with the **IP address** of the target machine.

---



