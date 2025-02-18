from flask import Flask, render_template, request, jsonify
from chat_with_products import chat_with_products
import os
from dotenv import load_dotenv
import pandas as pd
import markdown

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')

def format_response(text: str) -> str:
    """Format the response text with better structure and styling"""
    html = markdown.markdown(text, extensions=['extra'])
    return html

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        chat_history = request.json.get('history', [])
        
        # Add user message to history
        chat_history.append({"role": "user", "content": user_message})
        
        # Get response from the model
        response = chat_with_products(messages=chat_history)
        assistant_message = response["message"].content
        
        # Format the response
        formatted_message = format_response(assistant_message)
        
        # Add assistant response to history
        chat_history.append({"role": "assistant", "content": assistant_message})
        
        return jsonify({
            "response": formatted_message,
            "history": chat_history
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)