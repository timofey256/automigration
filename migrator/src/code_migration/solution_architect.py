class SolutionArchitect:
    def __init__(self, client, model, use_cache=False):
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
        self.use_cache = use_cache

        self.docs_cached = """
        Codebase Overview:

        The project is a hotel management system (HMS) that allows users to manage guests, rooms, and reservations. It has a modular structure, with different modules for handling different aspects of the system. The main components of the project are:

        1. config.py: Contains configurations and globals used throughout the project.
        2. controller.py: Contains functions for interacting with the database, such as adding, updating, and deleting records.
        3. gui/: Contains the graphical user interface (GUI) components of the project. It has a main_window package that contains the main application window and its components, and a login package that contains the login window.

        Component Documentation:

        config.py:

        Component Overview:
        This file contains configurations and globals used throughout the project.

        API Documentation:

        * `config`: A dictionary containing configurations for the database connection.

        controller.py:

        Component Overview:
        This file contains functions for interacting with the database, such as adding, updating, and deleting records.

        API Documentation:

        * `checkUser(username, password=None)`: Checks if a user exists in the database with the given username and password.
        * `human_format(num)`: Formats a number as a string with a suffix indicating its magnitude (e.g., "1K" for 1000).
        * `updatePassword(username, sec_ans, sec_que, password)`: Updates a user's password in the database.
        * `updateUsername(oldusername, password, newusername)`: Updates a user's username in the database.
        * `find_g_id(name)`: Finds a guest's ID in the database given their name.
        * `checkin(g_id)`: Checks a guest in for a reservation in the database.
        * `checkout(id)`: Checks a guest out of a reservation in the database.
        * `acceptable(*args, acceptables)`: Checks if all the characters in the given strings are in the given set of acceptable characters.
        * `get_guests()`: Retrieves all guests from the database.
        * `add_guest(name, address, email_id, phone)`: Adds a new guest to the database.
        * `add_room(room_no, price, room_type)`: Adds a new room to the database.
        * `get_rooms()`: Retrieves all rooms from the database.
        * `get_reservations()`: Retrieves all reservations from the database.
        * `add_reservation(g_id, meal, r_id, check_in="now")`: Adds a new reservation to the database.
        * `get_total_rooms()`: Retrieves the total number of rooms in the database.
        * `booked()`: Retrieves the number of booked rooms in the database.
        * `vacant()`: Retrieves the number of vacant rooms in the database.
        * `bookings()`: Retrieves the number of bookings for each room type in the database.
        * `get_total_hotel_value()`: Retrieves the total value of all rooms in the database.
        * `delete_reservation(id)`: Deletes a reservation from the database.
        * `delete_room(id)`: Deletes a room from the database.
        * `delete_guest(id)`: Deletes a guest from the database.
        * `update_rooms(id, room_no, room_type, price)`: Updates a room in the database.
        * `update_guests(name, address, id, phone)`: Updates a guest in the database.
        * `update_reservations(g_id, check_in, room_id, reservation_date, check_out, meal, type, id)`: Updates a reservation in the database.
        * `meals()`: Retrieves the total number of meals booked in the database.
        * `update_reservation(id, g_id, check_in, room_id, check_out, meal)`: Updates a reservation in the database.

        gui/main\_window/\_\_init\_\_.py:

        Component Overview:
        This file is an empty package initialization file.

        gui/main\_window/main.py:

        Component Overview:
        This file contains the main application window for the HMS.

        API Documentation:

        * `MainWindow`: A class representing the main application window.

        gui/main\_window/dashboard/gui.py:

        Component Overview:
        This file contains the dashboard window for the HMS.

        API Documentation:

        * `Dashboard`: A class representing the dashboard window.

        gui/main\_window/reservations/\_\_init\_\_.py:

        Component Overview:
        This file is an empty package initialization file.

        gui/main\_window/reservations/main.py:

        Component Overview:
        This file contains the reservations window for the HMS.

        API Documentation:

        * `Reservations`: A class representing the reservations window.

        gui/main\_window/reservations/add\_reservations/gui.py:

        Component Overview:
        This file contains the add reservations window for the HMS.

        API Documentation:

        * `AddReservations`: A class representing the add reservations window.

        gui/main\_window/reservations/view\_reservations/main.py:

        Component Overview:
        This file contains the view reservations window for the HMS.

        API Documentation:

        * `ViewReservations`: A class representing the view reservations window.

        gui/main\_window/reservations/update\_reservation/main.py:

        Component Overview:
        This file contains the update reservation window for the HMS.

        API Documentation:

        * `UpdateReservations`: A class representing the update reservation window.

        gui/main\_window/rooms/\_\_init\_\_.py:

        Component Overview:
        This file is an empty package initialization file.

        gui/main\_window/rooms/main.py:

        Component Overview:
        This file contains the rooms window for the HMS.

        API Documentation:

        * `Rooms`: A class representing the rooms window.

        gui

        """
        
        self.migration_solution_cached = """
        Technology Stack Selection:

        For the hotel management system, we will migrate from Python to Java, utilizing the Spring Boot framework for a robust and modular backend. Specific technologies and tools within the target stack include:

        1. Java 11: As the primary programming language, Java offers a mature ecosystem, excellent tooling, and strong community support.
        2. Spring Boot: A production-grade framework that provides rapid application development and deployment capabilities, along with built-in support for security, transactions, and data access.
        3. Spring Data: A module within the Spring ecosystem that simplifies data access and provides integration with various databases, including relational and NoSQL databases.
        4. Hibernate: A popular Object-Relational Mapping (ORM) tool for Java that simplifies database interactions and mapping between Java objects and relational database tables.
        5. Thymeleaf: A modern server-side templating engine for creating rich and dynamic web pages, integrated with Spring Boot.

        Architecture and Design Patterns:

        1. Microservices Architecture: To take advantage of Java's modularity and scalability, we will adopt a microservices architecture, where each core functionality (e.g., guests, rooms, reservations) is a separate service.
        2. Repository Pattern: Implement the Repository pattern for data access, which abstracts the underlying data store and provides a consistent interface for data manipulation.
        3. Domain-Driven Design (DDD): Utilize DDD principles to define rich domain models, ensuring a clear separation of concerns and improved maintainability.

        Component-by-Component Migration Strategy:

        1. config.py:
                * Map to: A Java configuration class annotated with `@Configuration` that initializes and manages global variables and configurations.
                * Adjustments: Replace Python dictionaries with Java Maps or Java classes for storing configurations.
        2. controller.py:
                * Map to: Spring Data repositories and Spring service classes for managing data access and business logic.
                * Adjustments: Replace direct database access with Hibernate and Spring Data methods.
        3. gui/:
                * Map to: Thymeleaf templates and Spring MVC controllers for creating the user interface.
                * Adjustments: Replace Python GUI components with Thymeleaf templates and Spring MVC controllers.

        Data Migration Plan:

        1. Export the existing data from the SQLite database to a format compatible with the target database (e.g., CSV, JSON).
        2. Write a Java utility to import the data into the new database, using Hibernate and Spring Data to map the data to Java objects.
        3. Ensure data consistency and integrity by comparing the data in the old and new databases before decommissioning the old system.

        Implementation Roadmap:

        1. Set up the Java and Spring Boot development environment.
        2. Create the initial project structure, including packages for each microservice and the data access layer.
        3. Implement the data access layer using Spring Data repositories and Hibernate.
        4. Implement the business logic layer using Spring service classes.
        5. Implement the user interface using Thymeleaf templates and Spring MVC controllers.
        6. Migrate the data from the SQLite database to the target database.
        7. Test and validate the new system, ensuring feature parity with the old system.
        8. Gradually deploy the new microservices, retiring the old system in phases to minimize disruption.
        """
        
        self.max_tokens = 1500

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
        
        Expected Output:

        Your output should be a meticulously structured document with the following sections:

        Codebase Overview: A succinct introduction to the project, outlining its purpose, scope, and overarching design principles. Highlight the main features and the intended user or system interactions.

        Component Documentation: For each file or module detailed in the input:
            Component Overview: Summarize the component's purpose and its contribution to the project's functionality.
            API Documentation: Detail the public interfaces, classes, methods, and functions defined in the component. For each entity, describe:
                Its purpose and functionality.
                Input parameters and expected output.
                Any exceptions it might raise.
                Dependencies on other project components or external libraries.
            Internal Implementation Details: Optionally, delve into significant implementation specifics that could aid in understanding complex logic or performance considerations.
        """

        prompt = f"Task :\n{task}\nProject tree structure :\n{project_structure}\n"
        for filename, content in files.items():
            prompt += f"Content of {filename} : \n{content}\n"

        if self.use_cache:
            print("Using cache...")
            return self.docs_cached
        
        return self.send_request(prompt)

    def build_solution(self, general_plan, new_stack, docs) -> str:
        task = f"You are tasked with {general_plan}\n\nUser-Specified Target Technology Stack:\n{new_stack}\n\nProject documentation:\n{docs}\n\n"
        expected_output = """
        Expected Migration Plan Output:

        Technology Stack Selection:
            Describe the rationale for choosing specific technologies and tools within the target stack, considering the functionalities and requirements outlined in the existing system's documentation.

        Architecture and Design Patterns:
            Suggest any architectural changes or introductions of design patterns that could benefit the system in the context of the target technology stack, ensuring alignment with best practices and idiomatic usage.

        Component-by-Component Migration Strategy:
            For each main component or module identified in the existing system, outline a strategy for its migration. This should include:
                Mapping to equivalent structures in the target stack (files, classes, services, etc.).
                Library or API substitutions for replacing specific functionalities.
                Adjustments in logic or architecture necessitated by differences between the source and target stacks.

        Data Migration Plan:
            If the system involves persistent data storage, provide guidelines for migrating this data to the new structure or technology, including any necessary transformations or adaptations.
        
        Implementation Roadmap:
            Present a phased or step-by-step approach for executing the migration, suggesting a logical order for component migrations to manage dependencies and minimize disruption.
        """

        prompt = task + expected_output

        if self.use_cache:
            print("Using cache...")
            return self.migration_solution_cached
        return self.send_request(prompt)

    def modificate_plan(self, migration_plan, modifications) -> str:
        task = f"""
        Modificate the Migration Plan below according to the these modifications: \"{modifications}\"
        
        Here is the Migration Plan: 
        {migration_plan}
        """

        expected_output = """
        Expected Modified Migration Plan Output:

        Technology Stack Selection:
            Describe the rationale for choosing specific technologies and tools within the target stack, considering the functionalities and requirements outlined in the existing system's documentation.

        Architecture and Design Patterns:
            Suggest any architectural changes or introductions of design patterns that could benefit the system in the context of the target technology stack, ensuring alignment with best practices and idiomatic usage.

        Component-by-Component Migration Strategy:
            For each main component or module identified in the existing system, outline a strategy for its migration. This should include:
                Mapping to equivalent structures in the target stack (files, classes, services, etc.).
                Library or API substitutions for replacing specific functionalities.
                Adjustments in logic or architecture necessitated by differences between the source and target stacks.

        Data Migration Plan:
            If the system involves persistent data storage, provide guidelines for migrating this data to the new structure or technology, including any necessary transformations or adaptations.
        
        Implementation Roadmap:
            Present a phased or step-by-step approach for executing the migration, suggesting a logical order for component migrations to manage dependencies and minimize disruption.
        """

        prompt = f"{task}\n\n{expected_output}"
        
        return self.send_request(prompt)

    def send_request(self, prompt):
        print("Sending request...")
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
            max_tokens=self.max_tokens
        )

        return chat_completion.choices[0].message.content