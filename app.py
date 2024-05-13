from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample quiz questions
quiz_questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Berlin', 'Rome'],
        'correct_answer': 'Paris'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Mars', 'Venus', 'Jupiter', 'Saturn'],
        'correct_answer': 'Mars'
    },
    {
        'question': 'Who wrote "To Kill a Mockingbird"?',
        'options': ['Harper Lee', 'J.K. Rowling', 'Stephen King', 'George Orwell'],
        'correct_answer': 'Harper Lee'
    }
]

# Leaderboard
leaderboard = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        score = 0
        question_results = []  # Store information about each question's correctness
        for question in quiz_questions:
            selected_option = request.form.get(question['question'])
            correct_option = question['correct_answer']
            if selected_option == correct_option:
                score += 1
                question_results.append({'question': question['question'], 'correct': True})
            else:
                question_results.append({'question': question['question'], 'correct': False, 'correct_option': correct_option})
        username = request.form.get('username')
        leaderboard[username] = {'score': score, 'question_results': question_results}
  # Store user's score and question results
        return redirect(url_for('display_leaderboard'))
    return render_template('quiz.html', questions=quiz_questions)


@app.route('/leaderboard')
def display_leaderboard():
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]['score'], reverse=True)
    return render_template('leaderboard.html', leaderboard=sorted_leaderboard)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)

