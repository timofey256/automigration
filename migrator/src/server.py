from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from flask import render_template
from flask_cors import CORS
from markdown2 import markdown

from agents import Agents

app = Flask(__name__)
CORS(app)

base_url = os.getenv('OPENAI_API_BASE')

print(base_url)

CORS(app, resources={r"/upload": {"origins": base_url}})

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

agents_singleton = Agents()

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('directory')
    prompt = request.form.get('prompt', '')

    if not files or files[0].filename == '':
        # print(files)
        return jsonify({'error': 'No files selected.'})

    files_content_dict = {}

    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        with open(file_path, 'r') as file_content:
            content = file_content.read()
            files_content_dict[filename] = content

    agents_singleton.generate_technical_documentation(files_content_dict)
    print(agents_singleton.technical_documentation)

    return jsonify({'message': f'{len(files)} files uploaded successfully', 'prompt': prompt})

def something():
    x = False
    if (x == True):
        return "# Title\n\nSome content."
    return "## Another Title\n\nMore content."
    
@app.route('/success')
def upload_success():
    markdown_content_1 = something()
    markdown_content_2 = something()
    html_content_1 = markdown(markdown_content_1)
    html_content_2 = markdown(markdown_content_2)
    return render_template('second.html', content1=html_content_1, content2=html_content_2)

@app.route('/regenerate-markdown')
def regenerate_markdown():
    window = request.args.get('window', type=int)
    new_markdown_content = '## Another Title\n\nMore content.\n## Another Title\n\nMore content.\n## Another Title\n\nMore content.'  # Raw markdown content
    return jsonify({'content': new_markdown_content})

if __name__ == '__main__':
    app.run(debug=True)