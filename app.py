import sys
import os

from flask import Flask, flash, redirect, render_template, request, session
import pytesseract
from PIL import Image

from datetime import datetime
from uuid import uuid4

# Configure application
app = Flask(__name__)

app.config['SECRET_KEY'] = "supersecretkey"
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'files')

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = os.path.join(os.getcwd(), 'tesseract', 'tesseract')

@app.route("/", methods=['GET', 'POST'])
def index():
    """Home Page"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        img = request.files['file']
        if img.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if img:
            img_name = datetime.now().strftime('%Y-%m-%d:%H-%M-%S:') + str(uuid4()) + '.png'
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            img.save(img_path)

            output = pytesseract.image_to_string(Image.open(img))
            print(output)
            
            return render_template("index.html", output=output, img_path=img_path)

        return render_template("index.html", output='Upload Failed')
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)