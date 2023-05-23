from flask import Flask, request, render_template
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

        # Make the filename safe, remove unsupported chars
        filename = secure_filename(pdf.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        pdf.save("/home/troutmask/Desktop/flashpdf/uploads/" + filename)

        # process the pdf
        flashcards = process_pdf("/home/troutmask/Desktop/flashpdf/uploads/" + filename, int(number_of_terms))

        return render_template('results.html', flashcards=flashcards)

    return '''
    <!doctype html>
    <title>Upload a PDF</title>
    <h1>Upload a PDF</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=pdf>
      <input type=text name=number_of_terms placeholder="Enter number of terms">
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)