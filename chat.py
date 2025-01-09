from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API key directly in the code
API_KEY = "Your_gemini_api_key"
genai.configure(api_key=API_KEY)

@app.route('/start-chat', methods=['POST'])
def start_chat():
    data = request.json
    place_name = data.get('place_name', 'India')
    # Use a session-like mechanism or alternative to store place_name
    return jsonify({'status': 'success'})

@app.route('/chat')
def chat():
    # Retrieve place_name from an alternative storage if needed
    place_name = 'India'  # Default value if not using session
    return render_template('chat.html', place_name=place_name)

@app.route('/ask-question', methods=['POST'])
def ask_question():
    user_question = request.json.get('question', '')
    place_name = request.json.get('place_name', 'India')  # Adjust as necessary

    if user_question.strip() != "":
        place_specific_question = f"Tell me about {place_name}. {user_question}"

        # Generate response using Google Gemini AI
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(place_specific_question)
            return jsonify({'response': response.text})
        except Exception as e:
            return jsonify({'response': f'Error: {str(e)}'})

    return jsonify({'response': 'Error: Question cannot be empty'})

if __name__ == '__main__':
    app.run(debug=True)
