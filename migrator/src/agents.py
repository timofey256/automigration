import os
from openai import OpenAI
from dotenv import load_dotenv
import code_migration.project_utils as ProjectUtils
from code_migration.solution_architect import SolutionArchitect 
from code_migration.software_engineer import SoftwareEngineer
from code_migration.tester import Tester

class Agents:
    def __init__(self):
        load_dotenv()

        api_key = os.getenv('OPENAI_API_KEY')
        base_url = os.getenv('OPENAI_API_BASE')
        model_name = os.getenv('OPENAI_MODEL_NAME')

        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_MODEL_NAME"] = model_name
        os.environ["OPENAI_API_BASE"] = base_url

        self.client = OpenAI(api_key=api_key, base_url=base_url)
        
        # Agents:
        self.solution_architect = SolutionArchitect(self.client, model_name)
        self.tester = Tester(self.client, model_name)
        self.programmer = SoftwareEngineer(self.client, model_name)

        self.technical_documentation = None

    def generate_technical_documentation(self, files):
        # Used in console app:
        # project_structure = ProjectUtils.get_project_structure(project_path=self.project_path)
        # files_contents = ProjectUtils.get_project_files_contents(project_path=self.project_path)

        project_structure = ""
        files_contents = {}
        for filename, content in files.items():
            project_structure += f"{filename}\n"
            files_contents[filename] = content
        
        self.technical_documentation = self.solution_architect.generate_docs(project_structure, files_contents)

        return self.technical_documentation