class SolutionArchitect:
    def __init__(self, client, model):
        self.client = client
        self.model = model

        self.system_prompt = """
        Task Description:
        You are a Solution Architect tasked with designing a migration plan from one technology to another. 
        It could be something like rewrite program from C# to Java. Or use MongoDB database instead of SQLite.
        You have 2 tasks: 
        1) Generate programmers documentation for the existing code.
        2) Generate migration plan: which components to rewrite and how.
        """

    def generate_docs(self, project_structure, files) -> str:
        """
        project structure : tree representation of the project
        files : a dictionary of items (filename : content of the file)
        """
        task = """
        You are tasked with generating comprehensive documentation for a software project. 
        The documentation should serve as a guide for programmers new to the project, providing insights into the project structure, key components, and detailed descriptions of the functionality contained within each file or module.        
        You have to output a detailed documentation for this which you will later use for the specifying how migration solution. 
        
        Input structure:
        Project Tree Structure: A text representation of the project's directory and file structure. This will give an overview of how the project is organized at a high level.
        File Contents: For a selection of files within the project, their full contents will be provided. This should include not just the code, but also any existing comments, docstrings, and metadata that could aid in understanding the purpose and functionality of each file.
        """

        prompt = f"Task :\n{task}\nProject tree structure :\n{project_structure}\n"
        for filename, content in files.items():
            prompt += f"Content of {filename} : \n{content}\n"
        
        print(prompt)

        chat_completion = self.client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": self.system_prompt,
            },
            {
            "role": "user",
            "content": prompt,
            }
            ],
            model=self.model,
            max_tokens=1500
        )

        return chat_completion.choices[0].message.content


    def build_solution(self, prompt, project_structure):
        chat_completion = self.client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": self.system_prompt,
            },
            {
            "role": "user",
            "content": self.generate_prompt(prompt, project_structure),
            }
            ],
            model=self.model
        )

        print(chat_completion.choices[0].message.content)

    def generate_prompt(self, user_prompt, project_structure):
        return f"""
        Task: {user_prompt}

        Project structure:
        {project_structure}

        Expected Output:
        Your output should be a structured Migration Plan that includes:

            Overview: A summary of the migration goals and key challenges.
            Preparation Steps: Any preliminary steps needed before starting the migration. This might include environment setup, training for the team on new technologies, or initial data backup.
            Migration Strategy:
                Component-wise Migration Plan: Detailed steps for migrating each component or module, considering dependencies and minimizing disruption.
                Data Migration Plan: Strategy for migrating databases or data stores, including schema migration, data transformation, and validation.
                Refactoring Guidelines: Suggestions for code refactoring needed to adapt to the new stack, including any patterns or practices to follow.
            Testing Strategy: Approach for testing during and after the migration, including unit tests, integration tests, and acceptance testing to ensure the migrated application meets all requirements.
            Rollout Plan: Steps for deploying the migrated project, including any phased rollout, rollback plan, and monitoring strategy.
            Risk Assessment and Mitigation: Identify potential risks and challenges in the migration process and propose mitigation strategies.
        """