from flask import Flask, render_template, request, session, jsonify
import json
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

try:
    with open('questions.json') as f:
        all_questions = json.load(f)
except FileNotFoundError:
    all_questions = []

@app.route('/')
def index():
    if len(all_questions) >= 5:
        selected_questions = random.sample(all_questions, 5)
    else:
        selected_questions = all_questions.copy() 

    session['questions'] = selected_questions  
    session['current_question'] = 0
    session['score'] = 0
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    current_index = session.get('current_question', 0)
    selected_questions = session.get('questions', [])

    if current_index < len(selected_questions):
        question = selected_questions[current_index]
        return jsonify({
            'question_id': question['id'],
            'question_text': question['question'],
            'options': question['options']
        })
    else:
        return jsonify({'quiz_complete': True, 'score': session.get('score', 0)})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    question_id = data.get('question_id')
    user_answer = data.get('answer')

    current_index = session.get('current_question', 0)
    selected_questions = session.get('questions', [])

    if current_index < len(selected_questions) and selected_questions[current_index]['id'] == question_id:
        correct_answer = selected_questions[current_index]['correct_answer']

        # Update score if the answer is correct
        if user_answer == correct_answer:
            session['score'] += 1

        # Move to the next question
        session['current_question'] += 1

        return jsonify({
            'correct': user_answer == correct_answer,
            'is_complete': session['current_question'] >= len(selected_questions),
            'score': session['score']
        })
    else:
        return jsonify({'error': 'Invalid question ID or answer.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
