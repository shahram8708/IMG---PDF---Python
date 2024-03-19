from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    if 'jpgs' not in request.files:
        return redirect(request.url)
    files = request.files.getlist('jpgs')
    images = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            images.append(file_path)
    if len(images) > 0:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.pdf')
        images_to_pdf(images, pdf_path)
        return redirect(url_for('uploaded_file', filename='output.pdf'))
    return 'No valid images uploaded.'

def images_to_pdf(image_paths, pdf_path):
    images = []
    for image_path in image_paths:
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        images.append(img)
    if images:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    port = 3000
    print(f'Server running at http://localhost:{port}/')
    app.run(debug=True, port=port)
