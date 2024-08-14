from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CONVERTED_FOLDER'] = CONVERTED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return 'Server is running'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files or 'compression' not in request.form:
        return 'No file part or compression type'
    files = request.files.getlist('files')
    compression_type = request.form['compression']
    for file in files:
        if file.filename == '':
            return 'No selected file'
        if file and file.filename.lower().endswith(('png', 'jpg', 'jpeg')):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            convert_image(filepath, filename, compression_type)
    return 'Files successfully uploaded and converted'

def convert_image(filepath, filename, compression_type):
    image = Image.open(filepath)
    if compression_type == 'webp':
        converted_filename = os.path.splitext(filename)[0] + '.webp'
        converted_filepath = os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)
        image.save(converted_filepath, 'WEBP')
    elif compression_type == 'jpeg':
        converted_filename = os.path.splitext(filename)[0] + '.jpeg'
        converted_filepath = os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)
        image.save(converted_filepath, 'JPEG')
    elif compression_type == 'png':
        converted_filename = os.path.splitext(filename)[0] + '.png'
        converted_filepath = os.path.join(app.config['CONVERTED_FOLDER'], converted_filename)
        image.save(converted_filepath, 'PNG')
    print(f"Image {filename} successfully converted to {converted_filename}")

if __name__ == '__main__':
    app.run(debug=True)