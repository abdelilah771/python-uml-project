import json

def generate_code_from_diagram(file_path, language):
    """Generate code based on a saved UML diagram JSON file."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except Exception as e:
        raise ValueError(f"Error reading file: {e}")

    classes = {cls["name"]: cls for cls in data.get("classes", [])}
    associations = data.get("associations", [])

    code_output = ""
    for cls_name, cls_data in classes.items():
        class_name = cls_data["name"]
        attributes = cls_data["attributes"]
        methods = cls_data["methods"]

        # Check associations for inheritance
        parents = [assoc["from"] for assoc in associations if assoc["to"] == class_name and assoc["type"] == "inheritance"]
        parent_class = parents[0] if parents else None

        # Generate code for the class
        if language == "python":
            code_output += generate_python_code(class_name, attributes, methods, parent_class) + "\n\n"
        elif language == "java":
            code_output += generate_java_code(class_name, attributes, methods, parent_class) + "\n\n"
        elif language == "php":
            code_output += generate_php_code(class_name, attributes, methods, parent_class) + "\n\n"
        else:
            raise ValueError("Unsupported language. Choose python, java, or php.")

        # Generate code for composition and aggregation
        related_classes = [
            assoc for assoc in associations if assoc["from"] == class_name and assoc["type"] in {"composition", "aggregation"}
        ]
        for assoc in related_classes:
            code_output += generate_relationship_code(language, assoc, classes) + "\n"

    return code_output


def generate_python_code(class_name, attributes, methods, parent_class):
    inheritance = f"({parent_class})" if parent_class else ""
    attr_lines = [f"    {attr} = None" for attr in attributes]
    method_lines = [f"    def {method}(self):\n        pass" for method in methods]

    return f"class {class_name}{inheritance}:\n" + "\n".join(attr_lines + method_lines)


def generate_java_code(class_name, attributes, methods, parent_class):
    inheritance = f" extends {parent_class}" if parent_class else ""
    attr_lines = [f"    private Object {attr};" for attr in attributes]
    method_lines = [f"    public void {method}() {{}}\n" for method in methods]

    return f"public class {class_name}{inheritance} {{\n" + "\n".join(attr_lines + method_lines) + "\n}"


def generate_php_code(class_name, attributes, methods, parent_class):
    inheritance = f" extends {parent_class}" if parent_class else ""
    attr_lines = [f"    public ${attr};" for attr in attributes]
    method_lines = [f"    public function {method}() {{}}\n" for method in methods]

    return f"class {class_name}{inheritance} {{\n" + "\n".join(attr_lines + method_lines) + "\n}"


def generate_relationship_code(language, assoc, classes):
    """Generate code for composition and aggregation relationships."""
    from_class = assoc["from"]
    to_class = assoc["to"]
    assoc_type = assoc["type"]

    if language == "python":
        if assoc_type == "composition":
            return f"    self.{to_class.lower()} = {to_class}()  # Composition relationship in {from_class}"
        elif assoc_type == "aggregation":
            return f"    self.{to_class.lower()} = None  # Aggregation relationship in {from_class}"
    elif language == "java":
        if assoc_type == "composition":
            return f"    private {to_class} {to_class.lower()};  // Composition relationship in {from_class}"
        elif assoc_type == "aggregation":
            return f"    private {to_class} {to_class.lower()};  // Aggregation relationship in {from_class}"
    elif language == "php":
        if assoc_type == "composition":
            return f"    private ${to_class.lower()};  // Composition relationship in {from_class}"
        elif assoc_type == "aggregation":
            return f"    private ${to_class.lower()};  // Aggregation relationship in {from_class}"

    return ""  # Fallback for unsupported relationships
