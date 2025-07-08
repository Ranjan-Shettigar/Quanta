import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# Initialize Gemini client
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

MODEL_NAME = "gemini-2.5-flash"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']

    # Build conversation history (simple: just last user message)
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_budget=0,
        ),
        response_mime_type="text/plain",
    )

    # Get response from Gemini
    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=MODEL_NAME,
        contents=contents,
        config=generate_content_config,
    ):
        if hasattr(chunk, "text"):
            response_text += chunk.text

    return jsonify({'response': response_text})

# if __name__ == '__main__':
#     app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
