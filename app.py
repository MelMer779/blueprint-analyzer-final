from flask import Flask, render_template, request
import os
import zipfile
import shutil
import json

from blueprint_parser import parse_blueprint_folder

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if not uploaded_file or not uploaded_file.filename.endswith('.zip'):
            return render_template('index.html', error="Please upload a valid ZIP file.")

        extract_path = os.path.join(UPLOAD_FOLDER, 'current')
        shutil.rmtree(extract_path, ignore_errors=True)
        os.makedirs(extract_path)

        zip_path = os.path.join(extract_path, 'blueprint.zip')
        uploaded_file.save(zip_path)

        try:
            #Extract the ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            #If JSON file inside, load and display it
            json_file = next((f for f in os.listdir(extract_path) if f.endswith('.json') and not f.startswith('._')), None)
            if json_file:
                json_path = os.path.join(extract_path, json_file)
                with open(json_path, 'r') as jf:
                    json_data = json.load(jf)
                return render_template('index.html', data=json_data)

            # 🧠 Otherwise, run full parsing logic
            data = parse_blueprint_folder(extract_path)
            return render_template('index.html', data=data)

        except Exception as e:
            return render_template('index.html', error=f"Failed to process file: {e}")

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)



