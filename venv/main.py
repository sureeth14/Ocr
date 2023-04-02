import os
import datetime
import easyocr
import docx
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

reader = easyocr.Reader(['en'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file uploaded', 400

    file = request.files['file']

    if file.filename == '':
        return 'No file selected', 400

    if not allowed_file(file.filename):
        return 'Invalid file type (only .jpg, .jpeg, .png allowed)', 400

    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    result = reader.readtext(os.path.join(app.config['UPLOAD_FOLDER'], filename), paragraph=True)

    doc = docx.Document()
    for i in range(len(result)):
        doc.add_paragraph(result[i][1])

    doc_filename = f"output_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.docx"
    doc.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), doc_filename))

    return send_from_directory(directory=os.path.dirname(os.path.abspath(__file__)), filename=doc_filename,
                               as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
