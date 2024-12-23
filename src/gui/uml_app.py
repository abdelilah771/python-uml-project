import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
from ..models.class_box import ClassBox
from ..models.association_line import AssociationLine
from ..models.code_generator import generate_code_from_diagram

class UMLApp:
    """Main application to manage the UML Diagram Editor."""

    def __init__(self, root):
        self.root = root
        self.root.title("Modern UML Diagram Editor")

        # Canvas
        self.canvas = tk.Canvas(root, bg="white", width=900, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.class_boxes = []
        self.associations = []

        # Dragging data
        self.drag_data = {"item": None, "start_x": 0, "start_y": 0}

        # Event bindings
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.canvas.bind("<Button-3>", self.delete_item)  # Right-click to delete items

        # UI setup
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface with a menu bar."""
        menu_bar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Generate Code", command=self.generate_code)
        file_menu.add_command(label="Save Diagram", command=self.save_diagram)
        file_menu.add_command(label="Load Diagram", command=self.load_diagram)
        file_menu.add_command(label="Quit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Add Class", command=self.add_class)
        edit_menu.add_command(label="Add Association", command=self.add_association)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menu_bar)

    def add_class(self):
        """Add a new class box."""
        class_name = simpledialog.askstring("Class Name", "Enter the class name:")
        attributes = simpledialog.askstring("Attributes", "Enter attributes (comma-separated):")
        methods = simpledialog.askstring("Methods", "Enter methods (comma-separated):")

        if class_name:
            attr_list = [attr.strip() for attr in attributes.split(",")] if attributes else []
            method_list = [method.strip() for method in methods.split(",")] if methods else []
            box = ClassBox(self.canvas, 100, 100, class_name, attr_list, method_list)
            self.class_boxes.append(box)

    def add_association(self):
        """Add an association line between two classes."""
        if len(self.class_boxes) < 2:
            messagebox.showerror("Error", "You need at least two classes to create an association.")
            return

        box_names = [box.class_name for box in self.class_boxes]
        box1_name = simpledialog.askstring("Class Selection", f"Select the first class:\n{', '.join(box_names)}")
        box2_name = simpledialog.askstring("Class Selection", f"Select the second class:\n{', '.join(box_names)}")

        box1 = next((box for box in self.class_boxes if box.class_name == box1_name), None)
        box2 = next((box for box in self.class_boxes if box.class_name == box2_name), None)

        if box1 and box2:
            line_type = simpledialog.askstring(
                "Line Type",
                "Enter line type (association, dependency, inheritance, composition, aggregation):"
            )
            if line_type in {"association", "dependency", "inheritance", "composition", "aggregation"}:
                line = AssociationLine(self.canvas, box1, box2, line_type)
                self.associations.append((line, line_type, box1.class_name, box2.class_name))
            else:
                messagebox.showerror("Error", "Invalid line type.")
        else:
            messagebox.showerror("Error", "Class not found.")

    def generate_code(self):
        """Generate and display code for all classes."""
        language = simpledialog.askstring(
            "Code Generation", "Enter target language (python, java, php):"
        )
        if language not in {"python", "java", "php"}:
            messagebox.showerror("Error", "Invalid language. Choose python, java, or php.")
            return

        association_summary = "\n".join([
            f"{assoc[2]} -> {assoc[3]} ({assoc[1]})"
            for assoc in self.associations
        ])
        messagebox.showinfo("Associations", f"Generated Associations:\n{association_summary}")

        code_output = ""
        for box in self.class_boxes:
            if language == "python":
                code_output += box.generate_python_code() + "\n\n"
            elif language == "java":
                code_output += box.generate_java_code() + "\n\n"
            elif language == "php":
                code_output += box.generate_php_code() + "\n\n"

        self.display_code_in_window(code_output, language)

    def display_code_in_window(self, code, language):
        """Display the generated code in a new Tkinter window."""
        code_window = tk.Toplevel(self.root)
        code_window.title(f"Generated Code ({language})")

        text_widget = tk.Text(code_window, wrap=tk.WORD)
        text_widget.insert(tk.END, code)
        text_widget.configure(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)

        save_button = tk.Button(code_window, text="Save Code", command=lambda: self.save_code_to_file(code, language))
        save_button.pack(pady=5)

    def save_code_to_file(self, code, language):
        """Save the generated code to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{language}",
            filetypes=[(f"{language.capitalize()} Files", f"*.{language}")],
            title="Save Generated Code"
        )
        if file_path:
            with open(file_path, "w") as file:
                file.write(code)
            messagebox.showinfo("Success", f"Code successfully saved to {file_path}")

    def save_diagram(self):
        """Save the current diagram to a JSON file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Diagram"
        )
        if file_path:
            data = {
                "classes": [
                    {
                        "name": box.class_name,
                        "attributes": box.attributes,
                        "methods": box.methods,
                        "position": self.canvas.coords(box.box_id)
                    } for box in self.class_boxes
                ],
                "associations": [
                    {
                        "type": assoc[1],
                        "from": assoc[2],
                        "to": assoc[3]
                    } for assoc in self.associations
                ]
            }
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("Success", f"Diagram successfully saved to {file_path}")

    def load_diagram(self):
        """Load a diagram from a JSON file."""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Load Diagram"
        )
        if file_path:
            with open(file_path, "r") as file:
                data = json.load(file)

            for box in self.class_boxes:
                box.delete()
            self.class_boxes.clear()
            for assoc, _, _, _ in self.associations:
                assoc.delete()
            self.associations.clear()

            for cls in data["classes"]:
                box = ClassBox(
                    self.canvas,
                    cls["position"][0],
                    cls["position"][1],
                    cls["name"],
                    cls["attributes"],
                    cls["methods"]
                )
                self.class_boxes.append(box)

            for assoc in data["associations"]:
                box1 = next((box for box in self.class_boxes if box.class_name == assoc["from"]), None)
                box2 = next((box for box in self.class_boxes if box.class_name == assoc["to"]), None)
                if box1 and box2:
                    line = AssociationLine(self.canvas, box1, box2, assoc["type"])
                    self.associations.append((line, assoc["type"], assoc["from"], assoc["to"]))

            messagebox.showinfo("Success", "Diagram successfully loaded.")

    def delete_item(self, event):
        """Delete the selected class box or association line."""
        item = self.canvas.find_closest(event.x, event.y)[0]
        for box in self.class_boxes:
            if box.box_id == item or item in box.box_parts:
                box.delete()
                self.class_boxes.remove(box)
                return
        for assoc, _, _, _ in self.associations:
            if assoc.line_id == item:
                assoc.delete()
                self.associations.remove(assoc)
                return

    def on_drag(self, event):
        """Handle drag events for moving boxes."""
        if not self.drag_data["item"]:
            item = self.canvas.find_closest(event.x, event.y)[0]
            for box in self.class_boxes:
                if box.box_id == item or item in box.box_parts:
                    self.drag_data["item"] = box
                    self.drag_data["start_x"] = event.x
                    self.drag_data["start_y"] = event.y
                    break
        else:
            dx = event.x - self.drag_data["start_x"]
            dy = event.y - self.drag_data["start_y"]
            self.drag_data["item"].move(dx, dy)
            self.drag_data["start_x"] = event.x
            self.drag_data["start_y"] = event.y
            for assoc, _, _, _ in self.associations:
                assoc.update_line()

    def on_release(self, event):
        """Handle mouse release."""
        self.drag_data["item"] = None
