from flask import Flask, request, render_template, url_for
from werkzeug.utils import secure_filename
from flashpdf import process_pdf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        pdf = request.files['pdf']
        number_of_terms = request.form['number_of_terms']
        
        if not pdf or not number_of_terms:
            return 'Missing pdf or number of terms', 400

        filename = secure_filename(pdf.filename)
        pdf.save("/home/troutmask/Desktop/flashpdf/uploads/" + filename)

        flashcards = process_pdf("/home/troutmask/Desktop/flashpdf/uploads/" + filename, int(number_of_terms))

        return render_template('results.html', flashcards=flashcards)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)