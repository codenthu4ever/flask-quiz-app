from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Sample quiz questions
quiz_questions = [
    {
        'question': 'What is the main focus of ISO 9001?',
        'options': ['Environmental Management', 'Occupational Health and Safety', 'Quality Management', 'Information Security'],
        'correct_answer': 'Quality Management'
    },
    {
        'question': 'Which of the following is NOT one of the ISO 9001 quality management principles?',
        'options': ['Customer Focus', 'Continual Improvement', 'Risk Management', 'Process Approach'],
        'correct_answer': 'Risk Management'
    },
    {
        'question': 'What is the purpose of the Plan-Do-Check-Act (PDCA) cycle in ISO 9001?',
        'options': ['To ensure compliance with legal requirements', 'To establish environmental objectives and targets', 'To monitor and improve processes', 'To assess workplace safety hazards'],
        'correct_answer': 'To monitor and improve processes'
    },
    {
        'question': 'Which ISO 9001 clause addresses the requirement for documenting the organization\'s quality management system?',
        'options': ['Clause 5 - Leadership', 'Clause 7 - Support', 'Clause 8 - Operation', 'Clause 9 - Performance Evaluation'],
        'correct_answer': 'Clause 7 - Support'
    },
    {
        'question': 'What is the primary objective of conducting internal audits in ISO 9001?',
        'options': ['To identify and address nonconformities', 'To monitor customer satisfaction', 'To reduce environmental impact', 'To develop product design specifications'],
        'correct_answer': 'To identify and address nonconformities'
    },
    {
        'question': 'What is the purpose of the "Context of the Organization" clause in ISO 9001?',
        'options': ['To determine the scope of the quality management system', 'To establish quality objectives', 'To conduct internal audits', 'To monitor customer feedback'],
        'correct_answer': 'To determine the scope of the quality management system'
    },
    {
        'question': 'Which ISO 9001 clause focuses on the control of nonconforming products or services?',
        'options': ['Clause 6 - Planning', 'Clause 7 - Support', 'Clause 8 - Operation', 'Clause 9 - Performance Evaluation'],
        'correct_answer': 'Clause 9 - Performance Evaluation'
    },
    {
        'question': 'What is the difference between ISO 9001:2015 and previous versions of the standard?',
        'options': ['ISO 9001:2015 emphasizes risk-based thinking and leadership engagement', 'ISO 9001:2015 includes requirements for product design', 'ISO 9001:2015 does not require internal audits', 'ISO 9001:2015 focuses solely on customer satisfaction'],
        'correct_answer': 'ISO 9001:2015 emphasizes risk-based thinking and leadership engagement'
    },
    {
        'question': 'What is the purpose of the "Interested Parties" clause in ISO 9001?',
        'options': ['To identify stakeholders affected by the quality management system', 'To define product specifications', 'To conduct market research', 'To establish quality control procedures'],
        'correct_answer': 'To identify stakeholders affected by the quality management system'
    },
    {
        'question': 'What is the key objective of ISO 14001?',
        'options': ['Quality Management', 'Environmental Management', 'Occupational Health and Safety', 'Information Security'],
        'correct_answer': 'Environmental Management'
    },
    {
        'question': 'Which of the following is a core element of ISO 14001?',
        'options': ['Risk Management', 'Supply Chain Management', 'Life Cycle Assessment', 'Project Management'],
        'correct_answer': 'Life Cycle Assessment'
    },
    {
        'question': 'What is the purpose of conducting an environmental aspect assessment in ISO 14001?',
        'options': ['To identify significant environmental aspects', 'To establish quality objectives', 'To monitor energy consumption', 'To assess employee competencies'],
        'correct_answer': 'To identify significant environmental aspects'
    },
    {
        'question': 'Which ISO 14001 clause addresses the requirement for establishing and maintaining documented procedures?',
        'options': ['Clause 5 - Leadership', 'Clause 6 - Planning', 'Clause 7 - Support', 'Clause 8 - Operation'],
        'correct_answer': 'Clause 7 - Support'
    },
    {
        'question': 'What is the primary goal of ISO 14001 certification?',
        'options': ['Achieving cost savings', 'Enhancing product quality', 'Demonstrating environmental commitment', 'Expanding market share'],
        'correct_answer': 'Demonstrating environmental commitment'
    },
    {
        'question': 'Which ISO 14001 clause addresses the requirement for monitoring and measurement of environmental performance?',
        'options': ['Clause 6 - Planning', 'Clause 7 - Support', 'Clause 8 - Operation', 'Clause 9 - Performance Evaluation'],
        'correct_answer': 'Clause 9 - Performance Evaluation'
    },
    {
        'question': 'What is the role of the "Environmental Policy" in ISO 14001?',
        'options': ['To establish environmental objectives and targets', 'To communicate the organization\'s commitment to environmental management', 'To conduct environmental audits', 'To assess compliance with legal requirements'],
        'correct_answer': 'To communicate the organization\'s commitment to environmental management'
    },
    {
        'question': 'Which ISO 14001 clause requires organizations to establish procedures for emergency preparedness and response?',
        'options': ['Clause 6 - Planning', 'Clause 7 - Support', 'Clause 8 - Operation', 'Clause 9 - Performance Evaluation'],
        'correct_answer': 'Clause 6 - Planning'
    },
    {
        'question': 'What is the purpose of the "Life Cycle Perspective" in ISO 14001?',
        'options': ['To assess employee competencies', 'To identify significant environmental aspects', 'To evaluate product sustainability throughout its life cycle', 'To monitor energy consumption and waste generation'],
        'correct_answer': 'To evaluate product sustainability throughout its life cycle'
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

        # Store quiz results in Excel
        date_time = datetime.now()
        data = {
            'Username': [username],
            'Score': [score],
            'Date': [date_time.date()],
            'Time': [date_time.time()]
        }
        df = pd.DataFrame(data)
        try:
            existing_data = pd.read_excel('quiz_results.xlsx')
            df = pd.concat([existing_data, df], ignore_index=True)
        except FileNotFoundError:
            pass
        df.to_excel('quiz_results.xlsx', index=False)

        return redirect(url_for('display_leaderboard'))
    return render_template('quiz.html', questions=quiz_questions)


@app.route('/leaderboard')
def display_leaderboard():
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]['score'], reverse=True)
    return render_template('leaderboard.html', leaderboard=sorted_leaderboard)


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=True)

