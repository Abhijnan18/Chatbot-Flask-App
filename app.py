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
    global conversation_count
    if conversation_count == message_limit:
        return render_template('index.html', conversation=conversation_history, show_form=False, message_limit=message_limit)
    return render_template('index.html', conversation=conversation_history, show_form=True, message_limit=message_limit)


@app.route('/ask', methods=['POST'])
def ask():
    global conversation_count

    user_message = request.form['user_message']
    conversation_history.append(f'You: {user_message}')

    # Construct the prompt for Lyra
    prompt = f'''You are Lyra, an AI healthcare chatbot created by Abhijnan. Your primary purpose is to offer accurate and concise information in response to health-related queries. Maintain a friendly and empathetic tone throughout the conversation.

    1. **General Instruction**: You are strictly programmed to respond only to health-related queries. If a question is unrelated to health, gently refuse to answer and guide the user back to health-related inquiries. It is crucial to adhere to this instruction consistently.

    2. **Response Structure**: Ensure your responses are clear and informative. If context from previous messages is required, refer to the earlier conversation history provided.

    3. **User Engagement**: Interact with users in a helpful manner. Your duty is to provide valuable health information and guide users towards better understanding.

    4. **Questioning**: You are allowed to ask questions related to health to gather more information and provide more accurate responses.

    Remember to embody the persona of a friendly and knowledgeable healthcare assistant. Please refer to the conversation history for context as needed.

    {conversation_history}
    '''

    # Pass the history as context
    response = genai.chat(messages=[prompt])

    # Append user input and Lyra's response to the conversation history
    conversation_history.append(f'Lyra: {response.last}')
    conversation_count += 1

    if conversation_count == message_limit:
        return render_template('index.html', conversation=conversation_history, show_form=False, message_limit=message_limit)
    return render_template('index.html', conversation=conversation_history, show_form=True, message_limit=message_limit)


@app.route('/new_conversation', methods=['POST'])
def new_conversation():
    global conversation_history
    global conversation_count
    conversation_history = []
    conversation_count = 0
    return render_template('index.html', conversation=conversation_history, show_form=True, message_limit=message_limit)


if __name__ == '__main__':
    app.run(debug=True)
