from flask import Flask, render_template, request, session, jsonify
import json
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load questions from JSON file
try:
    with open('questions.json', encoding='utf-8') as f:
        all_questions = json.load(f)
except FileNotFoundError:
    all_questions = []
    print("Error: 'questions.json' file not found. Ensure it exists in the project directory.")
except json.JSONDecodeError:
    all_questions = []
    print("Error: Failed to parse 'questions.json'. Check the JSON file for formatting issues.")
except Exception as e:
    all_questions = []
    print(f"Error: {str(e)}")

@app.route('/')
def home():
    return render_template('home.html', title="Quiz Game")

@app.route('/quiz')
def quiz():
    category = request.args.get('category')

    categories = {
        "jee": ["physics", "chemistry", "math"],
        "neet": ["physics", "chemistry", "biology"],
        "physics": ["physics"],
        "chemistry": ["chemistry"],
        "maths": ["math"],
        "biology": ["biology"]
    }

    if category not in categories:
        return jsonify({'error': 'Invalid category!'}), 400

    selected_subjects = categories[category]
    selected_questions = [
        question for question in all_questions if question.get("category") in selected_subjects
    ]

    if not selected_questions:
        return jsonify({'error': 'No questions available for the selected category.'}), 404

    # Set the number of questions based on the category
    num_questions = 20 if category in ["jee", "neet"] else 10

    if len(selected_questions) >= num_questions:
        selected_questions = random.sample(selected_questions, num_questions)

    session['questions'] = selected_questions
    session['current_question'] = 0
    session['score'] = 0

    return render_template('index.html', category=category)

@app.route('/get_question', methods=['GET'])
def get_question():
    current_index = session.get('current_question', 0)
    selected_questions = session.get('questions', [])

    if not selected_questions:
        return jsonify({'error': 'No questions available.'}), 400

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

    if not selected_questions:
        return jsonify({'error': 'No active questions.'}), 400

    if current_index < len(selected_questions):
        question = selected_questions[current_index]

        if question['id'] == question_id:
            correct_answer = question['correct_answer']

            if user_answer == correct_answer:
                session['score'] += 1

            session['current_question'] += 1

            return jsonify({
                'correct': user_answer == correct_answer,
                'is_complete': session['current_question'] >= len(selected_questions),
                'score': session['score']
            })
        else:
            return jsonify({'error': 'Question ID mismatch.'}), 400
    else:
        return jsonify({'error': 'Invalid question ID or no active question.'}), 400

@app.route('/get_final_score', methods=['GET'])
def get_final_score():
    score = session.get('score', 0)
    return jsonify({'score': score})
if __name__ == '__main__':
    app.run(debug=True)


