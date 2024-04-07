import os

class Tester:
    def __init__(self, client, model, use_cache=False):
        self.client = client
        self.model = model

        self.use_cache = use_cache

        self.system_prompt = """
        Task Description:
        We migrate some project to a new technology. You are a Tester tasked with designing a integration tests for the new solution. 
        They have to be written in new technology but have to preserve the given API.  
        """

        self.max_tokens = 1500
        self.tests_destination_dir = "./migration_tests"

        self.tests_cached = """
        Test Filenames and Content:

        1. test\_config\_Java:
        ```java
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;

        public class test_config_Java {
            @Test
            public void testConfig() {
                // Assuming config is a public static final field in Config class
                assertEquals("expectedDBConfig", Config.config);
            }
        }
        ```
        2. test\_controller\_Java:
        ```java
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;

        public class test_controller_Java {
            @Test
            public void testCheckUser() {
                // Assuming Controller class and checkUser method
                assertEquals(true, Controller.checkUser("testUser"));
            }

            // Add more tests for other methods in controller.py
        }
        ```
        3. test\_mainWindow\_Java:
        ```java
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;

        public class test_mainWindow_Java {
            @Test
            public void testMainWindow() {
                // Assuming MainWindow class and methods
                MainWindow mainWindow = new MainWindow();
                assertEquals("expectedTitle", mainWindow.getTitle());
            }
        }
        ```
        4. test\_dashboard\_Java:
        ```java
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;

        public class test_dashboard_Java {
            @Test
            public void testDashboard() {
                // Assuming Dashboard class and methods
                Dashboard dashboard = new Dashboard();
                assertEquals("expectedDashboardTitle", dashboard.getTitle());
            }
        }
        ```
        5. test\_reservations\_Java:
        ```java
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;

        public class test_reservations_Java {
            @Test
            public void testReservations() {
                // Assuming Reservations class and methods
                Reservations reservations = new Reservations();
                assertEquals("expectedReservationsTitle", reservations.getTitle());
            }
        }
        ```
        6. test\_addReservations\_Java:
        ```java
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;

        public class test_addReservations_Java {
            @Test
            public void testAddReservations() {
                // Assuming AddReservations class and methods
                AddReservations addReservations = new AddReservations();
                assertEquals("expectedAddReservationsTitle", addReservations.getTitle());
            }
        }
        ```
        7. test\_viewReservations\_Java:
        ```java
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;

        public class test_viewReservations_Java {
            @Test
            public void testViewReservations() {
                // Assuming ViewReservations class and methods
                ViewReservations viewReservations = new ViewReservations();
                assertEquals("expectedViewReservationsTitle", viewReservations.getTitle());
            }
        }
        ```
        8. test\_updateReservation\_Java:
        ```java
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;

        public class test_updateReservation_Java {
            @Test
            public void testUpdateReservation() {
                // Assuming UpdateReservations class and methods
                UpdateReservations updateReservations = new UpdateReservations();
                assertEquals("expectedUpdateReservationsTitle", updateReservations.getTitle());
            }
        }
        ```
        9. test\_rooms\_Java:
        ```java
        import org.junit.Test;
        import static org.junit.Assert.assertEquals;

        public class test_rooms_Java {
            @Test
            public void testRooms() {
                // Assuming Rooms class and methods
                Rooms rooms = new Rooms();
                assertEquals("expectedRoomsTitle", rooms.getTitle());
            }
        }
        ```
        """

    def generate_integration_tests(self, docs, general_plan, stack):
        input_data = f"""
        You are tasked with generating integration tests for our system that has recently been migrated to a new technology stack.
        The new technology is {general_plan}.
        Specifically, stack is {stack}.

        The tests should validate the interaction between different components of the system, ensuring that they work together as expected in the new environment. 
        The integration tests should be based on the provided programmer documentation, covering critical functionalities and interactions within the system.

        The programmers documentation:
        {docs}
        """
        
        expected_output = f"""
        Expected Integration Tests Format:
        Each test should be documented as follows:

            Name of the New Test File: (e.g., GuestController.java)
            Content of the Test File: (The Java/Spring Boot equivalent of the original Python module, considering Spring Boot's conventions and the application's architectural requirements.)

        Guidelines for Test Creation:
            Use descriptive test names that clearly indicate what each test aims to verify.
            Include setup and teardown methods as necessary to prepare for and clean up after tests, especially for database interactions.
            Employ mocking to isolate tests from external dependencies, focusing on the interaction between system components.
            Assert both expected outcomes and error handling paths to ensure robustness.

        DO NOT INCLUDE ANYTHING BUT REQUIRED FORMAT OF (test_filename : [content of the test file]). DO NOT ADD ANY COMMENTS!
        Note that you have only {self.max_tokens} tokens to output.
        Ensure that filenames include extensions corresponding to their programming language. For example, if you write tests for C#, generate files with .cs extension. 
        """

        prompt = f"{input_data}\n\n{expected_output}"

        if self.use_cache:
            print("Using cached...")
            return self.tests_cached
        
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

    def modificate_tests(self, tests):
        return tests

    def save_test_files(self, model_output_tests):
        files = self.parse_files(model_output_tests)

        if not os.path.exists(self.tests_destination_dir):
            os.makedirs(self.tests_destination_dir)
        
        for filename, content in files.items():
            # Construct the full path where the file will be saved
            file_path = os.path.join(self.tests_destination_dir, filename)
            
            # Write the content to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

    def parse_files(self, message):
        lines = message.split('\n')
        test_files = {}
        current_filename = ""
        for line in lines:
            if line and line.strip().startswith('Test File Name'):
                current_filename = line.strip().split(':')[1].strip().replace('\\', '')
                test_files[current_filename] = ""
            else:
                if current_filename:
                    if line.strip().startswith("```") or line.strip().startswith("Content"):
                        continue
                    test_files[current_filename] += line + "\n"
        
        return test_files
        
        return test_files
    
if __name__ == "__main__":
    test_tester = Tester(None, None)
    res = test_tester.save_test_files(None)
    for item in res.items():
        print(f"Filename: {item[0]} : \nContent:{item[1]}")