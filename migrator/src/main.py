# import subprocess
# import json
# from concurrent.futures import ThreadPoolExecutor
# import concurrent.futures

# class Models:
#     def call_ollama_model_via_curl(self, prompt):
#         # Escape newlines in the prompt for JSON compatibility
#         json_payload = json.dumps({"model": "llama2", "prompt": prompt, "stream": False})
#         command = f'curl http://localhost:11434/api/generate -d \'{json_payload}\''
#         process = subprocess.run(command, shell=True, capture_output=True, text=True)
#         print("TEST")
#         if process.returncode == 0:
#             print("TESTTT")
#             try:
#                 response_data = json.loads(process.stdout)
#                 return response_data.get("response")
#             except json.JSONDecodeError:
#                 return "Error: Failed to parse JSON response"
#         else:
#             return f"Error: Command failed with status {process.returncode} and error message {process.stderr}"

#     def call_another_model(self, prompt):
#         return {"response": "Simulated response for " + prompt}
    
# # class Parser():
# #     def parseCSharp(self, code):
# #         return code.replace("\\n", "\n")
    
        
# class ProgrammerAgent:
#     # Will be responsible for communicating with the models asynchrounously and return the responses
#     # def __init__(self):
#     #     self.promot = None

#     def write_code(self, prompt, models_instance):
#         responses = {}
#         with ThreadPoolExecutor() as executor:
#             future_to_model = {executor.submit(model, prompt): name for name, model in models_instance.items()}
#             for future in concurrent.futures.as_completed(future_to_model):
#                 model_name = future_to_model[future]
#                 try:
#                     responses[model_name] = future.result()
#                 except Exception as exc:
#                     print(f'{model_name} generated an exception: {exc}')
#         return responses
    
#     def satisfied(self, some_bool):
#         if some_bool:
#             return True
#         else:
#             return False
    

# def main():
#     model_instances = Models()
#     agent = ProgrammerAgent()
#     prompt = """Please convert the following C# code into Python code and only give me the code without any explanation. namespace PRACTICE {

#     abstract class Program {

#         public static void Main(string[] args) {
#             List<int> intList = new List<int>();
#             intList.Add(1); // No casting needed
#             intList.Add(2);
#             List<string> stringList = new List<string>();
#             stringList.Add("Hello");
#             stringList.Add("World");
#             // Accessing elements does not require casting
#             int firstNumber = intList[0];
#             string firstString = stringList[0];
#         }
#     }
# }
# """
#     prompt.replace("\\\n", "\n")
#     model_methods = {
#         "ollama": model_instances.call_ollama_model_via_curl,
#         "another_model": model_instances.call_another_model
#     }
#     responses = agent.write_code(prompt, model_methods)
#     for model_name, response in responses.items():
#         print(response)

# if __name__ == "__main__":
#     main()



# def main():
#     server.app.run(debug=True)

# if __name__ == "__main__":
#     main()