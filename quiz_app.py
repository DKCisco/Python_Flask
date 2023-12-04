from flask import Flask, render_template, request
import csv

app = Flask(__name__)

def load_quiz(filename):
    questions = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row if present
        for row in reader:
            question = {
                'text': row[0],
                'options': row[1].split(' | ')  # Assuming options are separated by ' | '
            }
            questions.append(question)
    return {'id': 1, 'name': 'Cybersecurity Quiz', 'questions': questions}

def load_correct_answers(filename):
    correct_answers = {}
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        print('Reading correct answers.')
        next(reader, None)  # Skip the header row
        for row in reader:
            correct_answers[int(row[0])] = [answer.strip() for answer in row[1].split('|')]
    return correct_answers

@app.route('/submit_quiz/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    quiz = load_quiz('sec_plus_quiz.csv')
    answers = load_correct_answers('correct_answers.csv')
    total_questions = len(quiz['questions'])
    correct_count = 0

    for q_index, question in enumerate(quiz['questions']):
        selected_options = request.form.getlist(f'question{q_index}')
        correct_set = set([ans.lower().strip() for ans in answers.get(q_index + 1, [])])  # Normalize data
        selected_set = set([sel.lower().strip() for sel in selected_options])  # Normalize data

        # Debugging logs
        print(f"Question {q_index + 1}:")
        print(f"Selected: {selected_set}")
        print(f"Correct: {correct_set}")

        if selected_set == correct_set:
            correct_count += 1
            print('Test')
            print(correct_count)

    score_percentage = (correct_count / total_questions) * 100
    return f"You scored {score_percentage:.2f}%!"

@app.route('/')
def home():
    quiz = load_quiz('sec_plus_quiz.csv')  # Replace with your CSV file path
    return render_template('home.html', quiz=quiz)

@app.route('/quiz/<int:quiz_id>')
def quiz(quiz_id):
    quiz = load_quiz('sec_plus_quiz.csv')
    return render_template('quiz.html', quiz=quiz)


if __name__ == '__main__':
    app.run(debug=True)
