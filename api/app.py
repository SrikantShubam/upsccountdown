import sys
import os

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Append the 'api' directory to the Python search path
sys.path.append(current_directory)

from flask import Flask, render_template, send_from_directory, redirect,url_for,request,jsonify
import csv
import datetime
import re

from fuzzywuzzy import fuzz
from send_mail import add_exam_request
from urllib.parse import quote_plus
from flask_cors import CORS



app = Flask(__name__)
CORS(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True
csv_file = os.path.join(app.root_path, 'static', 'assets', 'dates.csv')


@app.route('/')
def index():
    exams = load_sorted_exams_from_csv(csv_file)
    for exam in exams:
        exam['countdown'] = countdown_to_date(exam['Date of Commencement of Exam'])
    return render_template('index.html', exams=exams)


def generate_slug(name):
    # Convert to lowercase
    name = name.lower()
    # Replace special characters and spaces with hyphens
    name = re.sub(r'[^a-z0-9]+', '-', name)
    # Remove leading and trailing hyphens
    name = name.strip('-')
    return name

def category_sort_order(exam):
    if exam.get('Category') == 'Popular':
        return 1
    elif exam.get('Category') == 'Upcoming':
        return 2
    else:
        return 3

def load_sorted_exams_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        exams = [row for row in csv_reader]
        for exam in exams:
            exam['url_exam_name'] = generate_slug(exam['Name of Examination'])
            # Check if the countdown is less than 45 days
            countdown = countdown_to_date(exam['Date of Commencement of Exam'])
            if countdown < 45 and not exam.get('Category'): 
                exam['Category'] = 'Upcoming'
    exams.sort(key=lambda x: (category_sort_order(x), datetime.datetime.strptime(x['Date of Commencement of Exam'], '%d.%m.%Y')))
    return exams



def countdown_to_date(date_str):
    exam_date = datetime.datetime.strptime(date_str, '%d.%m.%Y')
    current_date = datetime.datetime.now()
    delta = exam_date - current_date
    return delta.days


@app.route('/exam-detail/<exam_name>-<year>')
def old_exam_detail(exam_name, year):
    new_url = url_for('exam_detail', exam_name=exam_name, year=year)
    # Generate the new URL

    print("New URL:", new_url)
    return redirect(new_url, code=301)




@app.route('/<exam_name>')
def exam_detail(exam_name):
    exams = load_sorted_exams_from_csv(csv_file)


    exam = next((e for e in exams if e['url_exam_name'] == exam_name), None)

    print("Looking for:", exam_name.replace('-', ' ').title())
    if exam:
        exam['countdown'] = countdown_to_date(exam['Date of Commencement of Exam'])
        return render_template('exam_details.html', exam=exam, meta_description=exam['Keywords'], exam_name=exam['Name of Examination'])
    else:
        return "Exam not found", 404

@app.route('/search', methods=['GET'])
def search():
    
    query = request.args.get('query', '').lower()
    print("query is loaded",query)
  
    exams = load_sorted_exams_from_csv(csv_file)

    # Filter exams based on fuzzy matching
    threshold = 75  # Define a threshold for fuzzy matching (you can adjust this)
    matching_exams = [
        exam for exam in exams if fuzz.token_set_ratio(query, exam['Name of Examination'].lower()) > threshold
    ]

    # Limit the number of results
    max_results = 5
    matching_exams = matching_exams[:max_results]

    return jsonify(matching_exams)


@app.route('/request-exam', methods=['POST'])
def request_exam():
  
    exam_name = request.form.get('exam_name')
    # Process this information. For now, we just print it.
    print(f"User has requested the addition of: {exam_name}")
    add_exam_request(exam_name)
    return jsonify({"message": "Request received!"})



@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml')
if __name__ == "__main__":
    app.run(debug=True)
