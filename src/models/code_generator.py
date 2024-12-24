import json  # Import the JSON module for handling JSON data

def generate_code_from_diagram(diagram, language):
    """
    Generate source code from the UML diagram data.

    Parameters:
    - diagram (dict): A dictionary representing the UML diagram, containing classes and associations.
    - language (str): The target programming language for code generation ('python', 'java', or 'php').

    Returns:
    - str: The generated source code as a single string.
    """
    # Create a dictionary mapping class names to their respective data for easy lookup
    classes = {cls["name"]: cls for cls in diagram["classes"]}
    associations = diagram["associations"]  # Extract associations from the diagram

    code_output = []  # Initialize a list to hold the generated code snippets

    def format_class(cls_name, attributes, methods, parent_class=None):
        """
        Helper function to format the class definition based on the target language.

        Parameters:
        - cls_name (str): The name of the class.
        - attributes (list): A list of attribute names.
        - methods (list): A list of method names.
        - parent_class (str, optional): The name of the parent class if inheritance is used.

        Returns:
        - str: The formatted class definition as a string.
        """
        if language == "python":
            # Handle inheritance in Python
            inheritance = f"({parent_class})" if parent_class else ""
            # Define attributes with default value None
            attr_lines = [f"    self.{attr} = None" for attr in attributes]
            # Define methods with a pass statement
            method_lines = [f"    def {method}(self):\n        pass" for method in methods]
            # Construct the complete class definition
            return (
                f"class {cls_name}{inheritance}:\n"
                f"    def __init__(self):\n"
                + "\n".join(attr_lines) + "\n"
                + "\n".join(method_lines) + "\n"
            )
        elif language == "java":
            # Handle inheritance in Java
            inheritance = f" extends {parent_class}" if parent_class else ""
            # Define attributes as private strings
            attr_lines = [f"    private String {attr};" for attr in attributes]
            # Define methods as public void methods with empty bodies
            method_lines = [f"    public void {method}() {{}}\n" for method in methods]
            # Construct the complete class definition
            return (
                f"public class {cls_name}{inheritance} {{\n"
                + "\n".join(attr_lines) + "\n"
                + "\n".join(method_lines) + "\n}\n"
            )
        elif language == "php":
            # Handle inheritance in PHP
            inheritance = f" extends {parent_class}" if parent_class else ""
            # Define attributes as private variables
            attr_lines = [f"    private ${attr};" for attr in attributes]
            # Define methods as public functions with empty bodies
            method_lines = [f"    public function {method}() {{}}\n" for method in methods]
            # Construct the complete class definition with PHP tags
            return (
                f"<?php\nclass {cls_name}{inheritance} {{\n"
                + "\n".join(attr_lines) + "\n"
                + "\n".join(method_lines) + "\n}\n?>\n"
            )
        else:
            # Raise an error if an unsupported language is specified
            raise ValueError("Unsupported language")

    # Iterate over each class in the diagram to generate its definition
    for cls_name, cls_data in classes.items():
        parent_class = None  # Initialize parent_class to None for inheritance

        # Check if the current class inherits from another class
        for assoc in associations:
            if assoc["type"] == "inheritance" and assoc["to"] == cls_name:
                parent_class = assoc["from"]  # Set the parent class name

        # Generate the class definition using the helper function
        class_def = format_class(
            cls_name,
            cls_data["attributes"],
            cls_data["methods"],
            parent_class
        )
        code_output.append(class_def)  # Add the class definition to the output list

    # Handle additional association types like aggregation and dependency
    for assoc in associations:
        if assoc["type"] == "aggregation":
            # Add a comment indicating aggregation relationship
            code_output.append(
                f"# Aggregation: {assoc['from']} aggregates {assoc['to']}\n"
            )
            # Depending on the language, you might want to implement aggregation-specific code here
        elif assoc["type"] == "dependency":
            # Add a comment indicating dependency relationship
            code_output.append(
                f"# Dependency: {assoc['from']} depends on {assoc['to']}\n"
            )
            # Depending on the language, you might want to implement dependency-specific code here

    # Join all code snippets into a single string separated by newlines
    return "\n".join(code_output)


# Example Usage
if __name__ == "__main__":
    # Define a sample UML diagram with classes and associations
    uml_diagram = {
        "classes": [
            {
                "name": "a",
                "attributes": ["a"],
                "methods": ["a"],
                "position": [20.0, 100.0, 220.0, 220.0],  # Position on the canvas (not used here)
            },
            {
                "name": "b",
                "attributes": ["b"],
                "methods": ["b"],
                "position": [467.0, 118.0, 667.0, 238.0],
            },
        ],
        "associations": [
            {"type": "inheritance", "from": "a", "to": "b"},
            {"type": "aggregation", "from": "a", "to": "b"},
            {"type": "dependency", "from": "b", "to": "a"},
        ],
    }

    # Generate Python Code
    print("Python Code:")
    print(generate_code_from_diagram(uml_diagram, "python"))

    # Generate Java Code
    print("\nJava Code:")
    print(generate_code_from_diagram(uml_diagram, "java"))

    # Generate PHP Code
    print("\nPHP Code:")
    print(generate_code_from_diagram(uml_diagram, "php"))
