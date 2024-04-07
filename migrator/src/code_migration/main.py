import os
from openai import OpenAI
from dotenv import load_dotenv
import project_utils as ProjectUtils
from solution_architect import SolutionArchitect 
from software_engineer import SoftwareEngineer
from tester import Tester

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
base_url = os.getenv('OPENAI_API_BASE')
model_name = os.getenv('OPENAI_MODEL_NAME')

os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_MODEL_NAME"] = model_name
os.environ["OPENAI_API_BASE"] = base_url

PROJECT_PATH = '/home/timothy/hackaton/code-migration/sample_project/'

class Pipeline:
    def __init__(self, project_path):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.project_path = project_path

        # Agents:
        self.solution_architect = SolutionArchitect(self.client, model_name)
        self.tester = Tester(self.client, model_name)
        self.programmer = SoftwareEngineer(self.client, model_name)

    def run_cycle_iterative(self):
        # build a dependency graph
        dependency_tree = ProjectUtils.find_file_dependencies(self.project_path)

        # generate documentation for the project
        project_structure = ProjectUtils.get_project_structure(project_path=self.project_path)
        files_contents = ProjectUtils.get_project_files_contents(project_path=self.project_path)
        programmer_docs = self.solution_architect.generate_docs(project_structure, files_contents)
        print(programmer_docs)

        # ask a user what he wants
        general_migration_prompt = input("[MIGRATION SPECS] Type a general migration plan: ")
        migration_stack = input("[MIGRATION SPECS] Specify a new stack: ")

        # feed all that to the Solution Architect
        migration_plan = self.solution_architect.build_solution(general_migration_prompt, migration_stack, programmer_docs)
        
        print("-"*50+f"\nMigration plan:\n{migration_plan}\n"+"-"*50)
        answer = input("[CONFIRMATION] Do you confirm the migration plan? If no, specify your modifications. ")
        while answer != "Yes":
            migration_plan = self.solution_architect.modificate_plan(migration_plan, answer)
            print("-"*50+f"\nMigration plan:\n{migration_plan}\n"+"-"*50)
            answer = input("[CONFIRMATION] Do you confirm the migration plan? If no, specify your modifications. ")

        # Generate Integration Tests
        tests = self.tester.generate_ixntegration_tests(programmer_docs, general_migration_prompt, migration_stack)
        answer = input("[CONFIRMATION] Do you confirm the tests? If no, specify your modifications. ")
        while answer != "Yes":
            tests = self.tester.modificate_tests(tests, answer)
            answer = input("[CONFIRMATION] Do you confirm the tests? If no, specify your modifications. ")

        
        print("-"*50+f"\nIntegration tests:\n{tests}\n"+"-"*50)
        answer = input("[CONFIRMATION] Do you confirm the tests? If no, specify your modifications. ")

        self.tester.save_test_files(tests)
        
        # feed it to the Programmer
        migrated_files = self.programmer.generate_migrated_code(migration_plan, tests, project_structure, files_contents)
        self.programmer.save_migrated_files(migrated_files)

    def run_cycle(self):
        # build a dependency graph
        dependency_tree = ProjectUtils.find_file_dependencies(self.project_path)

        # generate documentation for the project
        project_structure = ProjectUtils.get_project_structure(project_path=self.project_path)
        files_contents = ProjectUtils.get_project_files_contents(project_path=self.project_path)
        programmer_docs = self.solution_architect.generate_docs(project_structure, files_contents)
        print(programmer_docs)

        # ask a user what he wants
        general_migration_prompt = input("[MIGRATION] General migration plan: ")
        migration_stack = input("[MIGRATION] Specify a new stack: ")

        # feed all that to the Solution Architect
        migration_plan = self.solution_architect.build_solution(general_migration_prompt, migration_stack, programmer_docs)

        print("-"*50+f"\nMigration plan:\n{migration_plan}\n"+"-"*50)
        input("[CONFIRMATION] Do you confitm the migration plan?")

        # Generate Integration Tests
        tests = self.tester.generate_integration_tests(programmer_docs, general_migration_prompt, migration_stack)
        self.tester.save_test_files(tests)
        print(tests)
        
        # feed it to the Programmer
        migrated_files = self.programmer.generate_migrated_code(migration_plan, tests, project_structure, files_contents)
        print(migrated_files)
        self.programmer.save_migrated_files(migrated_files)

if __name__ == "__main__":
    pipeline = Pipeline(PROJECT_PATH)
    pipeline.run_cycle_iterative()