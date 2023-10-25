from flask import Flask, render_template
import csv
import datetime

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    exams = load_sorted_exams_from_csv('./static/assets/dates.csv')
    for exam in exams:
        exam['countdown'] = countdown_to_date(exam['Date of Commencement of Exam'])
   
    return render_template('index.html', exams=exams)


def load_sorted_exams_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        exams = [row for row in csv_reader]
    
    exams.sort(key=lambda x: datetime.datetime.strptime(x['Date of Commencement of Exam'], '%d.%m.%Y'), reverse=False)
    return exams


def countdown_to_date(date_str):
    exam_date = datetime.datetime.strptime(date_str, '%d.%m.%Y')
    current_date = datetime.datetime.now()
    delta = exam_date - current_date

    return delta.days


@app.route('/exam-detail/<exam_name>')
def exam_detail(exam_name):
    exams = load_sorted_exams_from_csv('./static/assets/dates.csv')
    exam = next((e for e in exams if e['Name of Examination'] == exam_name), None)
    
    if exam:
        exam['countdown'] = countdown_to_date(exam['Date of Commencement of Exam'])
        return render_template('exam_details.html', exam=exam)
    else:
        return "Exam not found", 404



if __name__ == "__main__":
    app.run(debug=True)
