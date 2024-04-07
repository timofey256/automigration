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
        code_model_name = os.getenv('CODE_MODEL_NAME')
        text_model_name = os.getenv('TEXT_MODEL_NAME')

        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["CODE_MODEL_NAME"] = code_model_name
        os.environ["TEXT_MODEL_NAME"] = text_model_name
        os.environ["OPENAI_API_BASE"] = base_url

        self.client = OpenAI(api_key=api_key, base_url=base_url)
        
        # Agents:
        self.solution_architect = SolutionArchitect(self.client, text_model_name)
        self.tester = Tester(self.client, code_model_name)
        self.programmer = SoftwareEngineer(self.client, code_model_name)

        self.technical_documentation = None
        self.migration_plan = None
        self.tests = None

        self.contents = None
        self.project_structure = None

        self.general_plan = None
        self.tech_stack = None

    def generate_tech_docs(self, structure, contents):
        self.contents = contents
        self.project_structure = structure
        self.technical_documentation = self.solution_architect.generate_docs(structure, contents)
        return self.technical_documentation
    
    def generate_migration_plan(self):
        self.migration_plan = self.solution_architect.build_solution(self.general_plan, self.tech_stack, self.technical_documentation)
        return self.migration_plan
    
    def regenerate_migration_plan(self, modifications):
        self.migration_plan = self.solution_architect.modificate_plan(self.migration_plan, modifications)
        return self.migration_plan
    
    def generate_tests(self):
        self.tests = self.tester.generate_integration_tests(self.technical_documentation, self.general_plan, self.tech_stack)
        return self.tests
    
    def generate_migrated_code(self):
        self.migrated_code = self.programmer.generate_migrated_code(self.migration_plan, self.tests, self.project_structure, self.contents)
        return self.migrated_code
    
    def regenerate_migrated_code(self, prompt):
        self.migrated_code = self.programmer.modify_code(self.migrated_code, prompt)
        print("="*30)
        print("="*30)
        print("="*30)
        print(self.migrated_code)
        return self.migrated_code