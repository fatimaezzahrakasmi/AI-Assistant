# ChatBot

A simple Flask‑based conversational AI application that leverages the **Groq** API for chat completions, stores exchanged messages in a local SQLite database, and provides a web interface for real‑time interaction.

---

## 🚀 Features

- **Conversational AI** using Groq's `llama-3.3-70b-versatile` model
- Message persistence with **SQLite** (`chatbot.db`)
- History retrieval and clearing via REST endpoints
- Web interface built with Flask, HTML templates, and CSS
- Environment variable support with `python-dotenv`

## 🗂 Project Structure

```
AI-Assistant/
├── app.py               # main Flask application
├── chatbot.db           # SQLite database (created at runtime)
├── README.md            # this file
├── templates/
│   └── index.html       # chat UI
└── static/
    └── style.css        # styles for the UI
```

## 📦 Requirements

- Python 3.10+
- Packages listed in `requirements.txt` 

> 📌 Note: The `groq-python` package provides the `Groq` client used in `app.py`.

## 🛠 Setup

1. **Clone the repository** (or navigate to your workspace):
   ```bash
   cd c:\Users\hp\OneDrive\Desktop\chatBot_project
   ```

2. **Create and activate a virtual environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```
   *(alternatively install manually: `pip install flask groq-python python-dotenv`)*

4. **Environment variables**
   - Create a `.env` file in the project root and add your Groq API key:
     ```env
     GROQ_API_KEY=your_api_key_here
     ```

5. **Run the app**:
   ```powershell
   python app.py
   ```
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## 🧪 Endpoints

| Route           | Method | Description                         |
|----------------|--------|-------------------------------------|
| `/`            | GET    | Render chat UI                      |
| `/chat`        | POST   | Send message; return AI response    |
| `/history`     | GET    | Retrieve stored conversation log    |
| `/clear_history`| POST  | Reset both in‑memory and database history |

Send a JSON payload to `/chat`:
```json
{ "message": "Hello!" }
```

## 🧠 Conversation Flow

- Messages are kept in `conversation_history` to provide context.
- Typing `clear` in the chat resets the in‑memory context.
- Every exchange is saved to SQLite for persistence; use `/history` to view all entries.

## 📝 Notes & Improvements

- The database is created automatically when the app starts (`init_db()` in `app.py`).
- The chat model, temperature, and other parameters are configurable in `groq_chat_with_history`.
- Feel free to add logging, user authentication, or deploy to a platform (Heroku, Azure, etc.).

---

Happy chatting! 🤖
