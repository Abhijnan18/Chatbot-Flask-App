import google.generativeai as genai
from flask import Flask, render_template, request

app = Flask(__name__)

# Set up the API key
genai.configure(api_key='AIzaSyBx1458lTVsLVXnBWLbqw-M0xiECUvcAQo')
conversation_history = []
message_limit = 2
conversation_count = 0


@app.route('/')
def index():
    return render_template('index.html', conversation=[])


@app.route('/ask', methods=['POST'])
def ask():
    global conversation_history
    global conversation_count

    user_message = request.form['user_message']

    # Append only user input to the conversation history
    conversation_history.append(f'You: {user_message}')

    # Construct the prompt for Isla
    prompt = f'''You are Isla, a helpful healthcare chatbot, developed by Abhijnan. Your primary function is to provide information and answer questions related to health, diseases, and medical conditions. Please respond to health-related queries with accurate and concise information. If a question is unrelated to health, kindly refuse to answer and guide them back to health-related inquiries (You are never supposed to answer questions related to other topics; it's your duty to gently refuse them, PLEASE REMEMBER THIS THROUGHOUT THE CONVERSATION). Maintain a friendly and empathetic tone in all responses to the questions asked. Question(You are only supposed to ask questions related to health):{user_message}'''

    # Pass the history as context
    response = genai.chat(messages=[prompt])

    # Append Isla's response to the conversation history
    conversation_history.append(f'Isla: {response.last}')
    conversation_count += 1

    if conversation_count == message_limit:
        return render_template('new_conversation.html')

    conversation = conversation_history[-message_limit:]
    return render_template('index.html', conversation=conversation)


@app.route('/new_conversation', methods=['POST'])
def new_conversation():
    global conversation_history
    global conversation_count

    choice = request.form['choice']

    if choice.lower() == 'y':
        conversation_history = []
        conversation_count = 0

    return render_template('index.html', conversation=[])


if __name__ == '__main__':
    app.run(debug=True)
