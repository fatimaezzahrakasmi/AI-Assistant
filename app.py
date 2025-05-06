from flask import Flask, render_template, request, jsonify
from groq import Groq
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize database and create table if not exists
def init_db():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Call it once when app starts
init_db()

def save_message(sender, message):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (sender, message)
        VALUES (?, ?)
    ''', (sender, message))
    conn.commit()
    conn.close()



app = Flask(__name__)

#initialize Groq Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are a knowledgeable and friendly AI assistant."}
]

def groq_chat_with_history(user_message, model="llama-3.3-70b-versatile"):
    global conversation_history
    # Add user message to history
    conversation_history.append({"role": "user", "content": user_message})
    
    try:
        chat_completion = client.chat.completions.create(
            messages=conversation_history,
            model=model,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        
        # Get AI response and add to history
        ai_response = chat_completion.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": ai_response})
        
        return ai_response
    except Exception as e:
        return f"An error occurred: {str(e)}"
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"response": "No message received."})

    if user_message.lower() == 'clear':
        global conversation_history
        conversation_history = [
            {"role": "system", "content": "You are a knowledgeable and friendly AI assistant."}
        ]
        return jsonify({"response": "Conversation history cleared."})

    # Get AI response
    ai_response = groq_chat_with_history(user_message)

    # Save user and bot messages into the database
    save_message('user', user_message)
    save_message('bot', ai_response)

    return jsonify({"response": ai_response})

@app.route("/history", methods=["GET"])
def history():
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sender, message, timestamp FROM conversations ORDER BY timestamp ASC")
    rows = cursor.fetchall()
    conn.close()

    # Format history
    history = [{"sender": row[0], "message": row[1], "timestamp": row[2]} for row in rows]

    return jsonify(history)

@app.route('/clear_history', methods=['POST'])
def clear_history():
    global conversation_history
    conversation_history = [
        {"role": "system", "content": "You are a knowledgeable and friendly AI assistant."}
    ]

    # Also clear from database if you want
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM conversations')
    conn.commit()
    conn.close()

    return jsonify({"message": "Conversation history cleared."})



if __name__=="__main__":
    app.run(debug=True)