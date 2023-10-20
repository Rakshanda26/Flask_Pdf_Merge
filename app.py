import os
from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import PyPDF2
import tempfile
import PyPDF2.errors

app = Flask(__name__)

# Function to merge PDF files in a directory and its subdirectories
def merge_pdfs(directory, output_pdf):
    pdf_merger = PyPDF2.PdfMerger()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".pdf"):
                try:
                    pdf_merger.append(open(os.path.join(root, file), 'rb'))
                except PyPDF2.errors.PdfReadError as e:
                    print(f"Skipping {file} due to PDFReadError: {e}")
                    continue
    with open(output_pdf, 'wb') as output_file:
        pdf_merger.write(output_file)

@app.route('/', methods=['GET', 'POST'])
def merge_pdf():
    message = ""  # Initialize an empty message
    if request.method == 'POST':
        directory = request.form['directory']
        output_pdf = 'static/Merged_PDF.pdf'  # Output PDF path
        merge_pdfs(directory, output_pdf)
        message = "PDF files merged successfully!"
        print(message)
    return render_template('index.html', message=message)

@app.route('/download')
def download():
    return send_from_directory('static', 'Merged_PDF.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
