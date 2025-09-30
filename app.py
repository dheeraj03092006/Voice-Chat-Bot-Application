from flask import Flask, render_template, request, jsonify
import subprocess
import sys
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # Call Chat_Bot.py with the user message
    result = subprocess.run([
        sys.executable, 'Chat_Bot.py', user_message
    ], capture_output=True, text=True)
    response = result.stdout.strip()
    return jsonify({'response': response})

@app.route('/voice', methods=['POST'])
def voice():
    # Call Voice_Bot.py in API mode to get both user_text and ai_response
    import json
    result = subprocess.run([
        sys.executable, 'Voice_Bot.py', '--api'
    ], capture_output=True, text=True)
    # Find the last line that is valid JSON
    lines = result.stdout.strip().splitlines()
    json_line = None
    for line in reversed(lines):
        try:
            data = json.loads(line)
            json_line = data
            break
        except Exception:
            continue
    if json_line:
        return jsonify(json_line)
    else:
        return jsonify({'error': 'Could not parse voice bot output', 'raw': result.stdout.strip()})

if __name__ == '__main__':
    app.run(debug=True)
