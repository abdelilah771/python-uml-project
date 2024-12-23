import tkinter as tk
from tkinter import simpledialog

class ClassBox:
    def __init__(self, canvas, x, y, class_name, attributes=None, methods=None, relationships=None):
        """
        Initialize a UML class box.
        :param canvas: Canvas on which the box is drawn.
        :param x, y: Top-left coordinates.
        :param class_name: Name of the class.
        :param attributes: List of class attributes.
        :param methods: List of class methods.
        :param relationships: Dict of relationships (composition, aggregation, dependency).
        """
        self.canvas = canvas
        self.class_name = class_name
        self.attributes = attributes or []
        self.methods = methods or []
        self.relationships = relationships or {"composition": [], "aggregation": [], "dependency": []}
        self.x, self.y = x, y
        self.width, self.height = 200, 120
        self.box_parts = []
        self.drag_data = {"x": 0, "y": 0}
        self.create_box()
        self.bind_events()

    def create_box(self):
        """Draws the UML class box."""
        # Draw main box and header
        self.box_id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height,
            outline="black", fill="#f0f8ff", width=2
        )
        header_id = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + 30,
            outline="black", fill="#87cefa", width=2
        )
        text_id = self.canvas.create_text(
            self.x + self.width / 2, self.y + 15, text=self.class_name,
            font=("Arial", 12, "bold"), anchor="center"
        )
        self.box_parts.extend([self.box_id, header_id, text_id])

        # Draw attributes
        attr_y = self.y + 35
        for attr in self.attributes:
            text_id = self.canvas.create_text(
                self.x + 10, attr_y, text=f"{attr}", font=("Arial", 10), anchor="nw"
            )
            self.box_parts.append(text_id)
            attr_y += 15

        # Draw methods
        method_y = attr_y + 5
        for method in self.methods:
            text_id = self.canvas.create_text(
                self.x + 10, method_y, text=f"{method}()", font=("Arial", 10), anchor="nw"
            )
            self.box_parts.append(text_id)
            method_y += 15

    def bind_events(self):
        """Binds drag and edit events."""
        for part_id in self.box_parts:
            self.canvas.tag_bind(part_id, "<ButtonPress-1>", self.on_drag_start)
            self.canvas.tag_bind(part_id, "<B1-Motion>", self.on_drag)
            self.canvas.tag_bind(part_id, "<Double-1>", self.edit_content)

    def on_drag_start(self, event):
        """Start dragging the box."""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag(self, event):
        """Handle dragging."""
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.move(dx, dy)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def move(self, dx, dy):
        """Move the box."""
        self.x += dx
        self.y += dy
        for part_id in self.box_parts:
            self.canvas.move(part_id, dx, dy)

    def edit_content(self, event):
        """Edit attributes, methods, and relationships."""
        attribute_string = ", ".join(self.attributes)
        method_string = ", ".join(self.methods)
        new_attributes = simpledialog.askstring("Edit Attributes", "Enter attributes (comma-separated):", initialvalue=attribute_string)
        new_methods = simpledialog.askstring("Edit Methods", "Enter methods (comma-separated):", initialvalue=method_string)
        if new_attributes is not None:
            self.attributes = [attr.strip() for attr in new_attributes.split(",")]
        if new_methods is not None:
            self.methods = [method.strip() for method in new_methods.split(",")]
        self.canvas.delete("all")
        self.create_box()

    def generate_python_code(self):
        """Generate Python code for the class."""
        code = f"class {self.class_name}:\n"
        code += "    def __init__(self):\n"

        # Add attributes
        for attr in self.attributes:
            code += f"        self.{attr} = None\n"

        # Add composition
        for comp_class in self.relationships["composition"]:
            code += f"        self.{comp_class.lower()} = {comp_class}()\n"

        # Add aggregation
        for agg_class in self.relationships["aggregation"]:
            code += f"        self.{agg_class.lower()} = None  # Aggregation\n"

        # Add dependency
        for dep_class in self.relationships["dependency"]:
            code += f"# Dependency: Uses {dep_class}\n"

        # Add methods
        for method in self.methods:
            code += f"\n    def {method}(self):\n        pass\n"

        return code

    def generate_java_code(self):
        """Generate Java code for the class."""
        code = f"public class {self.class_name} {{\n"

        # Add attributes
        for attr in self.attributes:
            code += f"    private String {attr};\n"

        # Add constructor
        code += "\n    public " + self.class_name + "() {\n"
        for comp_class in self.relationships["composition"]:
            code += f"        this.{comp_class.lower()} = new {comp_class}();\n"
        code += "    }\n"

        # Add aggregation
        for agg_class in self.relationships["aggregation"]:
            code += f"    private {agg_class} {agg_class.lower()}; // Aggregation\n"

        # Add dependency comments
        for dep_class in self.relationships["dependency"]:
            code += f"// Dependency: Uses {dep_class}\n"

        code += "}\n"
        return code

    def generate_php_code(self):
        """Generate PHP code for the class."""
        code = f"<?php\nclass {self.class_name} {{\n"

        # Add attributes
        for attr in self.attributes:
            code += f"    private ${attr};\n"

        # Add constructor
        code += "\n    public function __construct() {\n"
        for comp_class in self.relationships["composition"]:
            code += f"        $this->{comp_class.lower()} = new {comp_class}();\n"
        code += "    }\n"

        # Add aggregation
        for agg_class in self.relationships["aggregation"]:
            code += f"    private ${agg_class.lower()}; // Aggregation\n"

        # Add dependency comments
        for dep_class in self.relationships["dependency"]:
            code += f"// Dependency: Uses {dep_class}\n"

        code += "}\n?>"

    def delete(self):
         self.canvas.delete(self.box_id)


# The "return code" line was removed, because it's outside of a function
