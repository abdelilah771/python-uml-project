import json

def generate_code_from_diagram(diagram, language):
    """Generate code from the UML diagram data."""
    classes = {cls["name"]: cls for cls in diagram["classes"]}
    associations = diagram["associations"]

    code_output = []

    # Helper to format class definition
    def format_class(cls_name, attributes, methods, parent_class=None):
        if language == "python":
            inheritance = f"({parent_class})" if parent_class else ""
            attr_lines = [f"    self.{attr} = None" for attr in attributes]
            method_lines = [f"    def {method}(self):\n        pass" for method in methods]
            return (
                f"class {cls_name}{inheritance}:\n"
                f"    def __init__(self):\n"
                + "\n".join(attr_lines) + "\n"
                + "\n".join(method_lines) + "\n"
            )
        elif language == "java":
            inheritance = f" extends {parent_class}" if parent_class else ""
            attr_lines = [f"    private String {attr};" for attr in attributes]
            method_lines = [f"    public void {method}() {{}}\n" for method in methods]
            return (
                f"public class {cls_name}{inheritance} {{\n"
                + "\n".join(attr_lines) + "\n"
                + "\n".join(method_lines) + "\n}\n"
            )
        elif language == "php":
            inheritance = f" extends {parent_class}" if parent_class else ""
            attr_lines = [f"    private ${attr};" for attr in attributes]
            method_lines = [f"    public function {method}() {{}}\n" for method in methods]
            return (
                f"<?php\nclass {cls_name}{inheritance} {{\n"
                + "\n".join(attr_lines) + "\n"
                + "\n".join(method_lines) + "\n}\n?>\n"
            )
        else:
            raise ValueError("Unsupported language")

    # Process each class
    for cls_name, cls_data in classes.items():
        parent_class = None

        # Check for inheritance
        for assoc in associations:
            if assoc["type"] == "inheritance" and assoc["to"] == cls_name:
                parent_class = assoc["from"]

        # Generate class definition
        code_output.append(format_class(cls_name, cls_data["attributes"], cls_data["methods"], parent_class))

    # Handle aggregation and dependencies
    for assoc in associations:
        if assoc["type"] == "aggregation":
            # Add an attribute for aggregation
            code_output.append(
                f"# Aggregation: {assoc['from']} aggregates {assoc['to']}\n"
            )
        elif assoc["type"] == "dependency":
            # Add a method parameter for dependency
            code_output.append(
                f"# Dependency: {assoc['from']} depends on {assoc['to']}\n"
            )

    return "\n".join(code_output)


# Example Usage
uml_diagram = {
    "classes": [
        {
            "name": "a",
            "attributes": ["a"],
            "methods": ["a"],
            "position": [20.0, 100.0, 220.0, 220.0],
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
