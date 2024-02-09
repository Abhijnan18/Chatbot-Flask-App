# Flask app
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from IPython.display import Markdown
import markdown


app = Flask(__name__)

# Set up the API key
genai.configure(api_key='AIzaSyBx1458lTVsLVXnBWLbqw-M0xiECUvcAQo')
conversation_history = []
message_limit = 50
conversation_count = 0


@app.route('/')
def index():
    global conversation_count
    if conversation_count == message_limit:
        return render_template('index.html', conversation=conversation_history, show_form=False, message_limit=message_limit, conversation_count=conversation_count)
    return render_template('index.html', conversation=conversation_history, show_form=True, message_limit=message_limit, conversation_count=conversation_count)


@app.route('/ask', methods=['POST'])
def ask():
    global conversation_count

    user_message = request.form['user_message']
    conversation_history.append(f'You::: {user_message}')

    # Construct the prompt for Lyra
    prompt = f'''
    You are Lyra, a knowledgeable AI healthcare chatbot developed by Abhijnan. Your primary mission is to provide accurate and concise information solely in response to health-related queries, maintaining a friendly and empathetic tone throughout the conversation.

    1. **General Instruction**: Your programming strictly confines responses to health-related queries. If a user poses a question unrelated to health, gently refuse to answer and redirect them to health-related topics. Consistency in adhering to this instruction is vital.

    2. **Response Structure**: Create responses that are clear, informative, and relevant to the user's health inquiries. If context from previous messages is necessary, refer to the earlier conversation history provided for a more tailored response.

    3. **User Engagement**: Interact with users in a helpful and supportive manner. Your duty is not only to provide information but also to guide users toward a better understanding of their health concerns. Ensure your communication reflects a positive and caring demeanor.

    4. **Questioning**: You are empowered to ask questions related to health to gather additional information, allowing you to provide more accurate and personalized responses. This enhances the user experience by tailoring information to their specific needs.
    
    Remember, your expertise lies in the health domain. Consistently follow these instructions to create a seamless and positive user experience. Refer to the conversation history for context as needed.

    The text delimited by single quotes is the conversation history please refer this to have context, and to avoid redundancy, reffering this make sure your conversations isn't reptational :'{conversation_history}'
    
    This is the current user message you are supposed to reply by reffering to the converstaion history if needed, and also please provide the answer in markdown format it is esstential for the users: {user_message}
    
    '''
    # All the Text elements of all the outputs you provide must be enclosed in suitable html tags, please dont forget to do this.
    # def to_markdown(text):
    #     text = text.replace('•', '  *')
    #     return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

    # Pass the history as context
    response = genai.chat(messages=[prompt])
    md_text = response.last
    
    # Convert markdown to html using the markdown function
    html = markdown.markdown(md_text)
    

    # Append user input and Lyra's response to the conversation history
    conversation_history.append(f'Lyra::: { html }')
    conversation_count += 1

    # Return JSON response
    return jsonify({'user_message': f'You::: {user_message}', 'lyra_message': f'Lyra::: {html}'})


@app.route('/new_conversation', methods=['POST'])
def new_conversation():
    global conversation_history
    global conversation_count
    conversation_history = []
    conversation_count = 0
    return render_template('index.html', conversation=conversation_history, show_form=True, message_limit=message_limit, conversation_count=conversation_count)

if __name__ == '__main__':
    app.run(debug=True)