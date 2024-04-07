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
    print(files)
    agents_singleton.general_plan = request.form.get('general_plan', '')
    agents_singleton.tech_stack = request.form.get('tech_stack', '')
    print(agents_singleton.general_plan)
    print(agents_singleton.tech_stack)    

    if not files or files[0].filename == '':
        # print(files)
        return jsonify({'error': 'No files selected.'})

    files_content_dict = {}
    project_structure = []

    for file in files:
        filename = secure_filename(file.filename)
        content = file.read().decode('utf-8')

        files_content_dict[filename] = content
        project_structure.append(filename)

    agents_singleton.generate_tech_docs(project_structure, files_content_dict)

    return jsonify({'message': f'{len(files)} files uploaded successfully', 
                    'general_plan': agents_singleton.general_plan, 
                    'tech_stack': agents_singleton.tech_stack})

@app.route('/success')
def upload_success():
    tech_docs_markdown = markdown(agents_singleton.technical_documentation)
    print(tech_docs_markdown)
    return render_template('second.html', content1=tech_docs_markdown)

@app.route('/regenerate-migration-plan', methods=['POST'])
def regenerate_migration_plan():
    data = request.get_json()
    prompt = data.get('prompt', 'Default prompt')
    # Assuming regenerate_migration_plan returns a Markdown string
    migration_plan_markdown = markdown(agents_singleton.regenerate_migration_plan(prompt))
    return jsonify({'content': migration_plan_markdown})

@app.route('/regenerate-migrated-code', methods=['POST'])
def regenerate_migrated_code():
    data = request.get_json()
    prompt = data.get('prompt', 'Default prompt')
    migration_plan_markdown = agents_singleton.regenerate_migrated_code(prompt)
    return render_template('fifth.html', files_dict=migration_plan_markdown)

@app.route('/generate_tests')
def generate_tests():
    tests = agents_singleton.generate_tests()
    print(tests) 
    return render_template('fourth.html', files_dict=tests)

@app.route('/generate_migrated_code')
def generate_migrated_code():
    print("hello!")
    migrated_code = agents_singleton.generate_migrated_code()
    print(migrated_code) 
    return render_template('fifth.html', files_dict=migrated_code)

@app.route('/to-migration-plan')
def to_migration_plan():
    migration_plan_markdown = markdown(agents_singleton.generate_migration_plan())
    return render_template('third.html', content1=migration_plan_markdown)

if __name__ == '__main__':
    app.run(debug=True)