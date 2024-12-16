import tkinter as tk
from tkinter import simpledialog, messagebox
from ..models.class_box import ClassBox
from ..models.association_line import AssociationLine

class UMLApp:
    """Main application to manage the UML Diagram Editor."""

    def __init__(self, root):
        self.root = root
        self.root.title("Modern UML Diagram Editor")
        self.canvas = tk.Canvas(root, bg="white", width=900, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.class_boxes = []
        self.associations = []

        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.drag_data = {"item": None, "start_x": 0, "start_y": 0}
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface elements."""
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X)
        tk.Button(button_frame, text="Add Class", command=self.add_class).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Add Association", command=self.add_association).pack(side=tk.LEFT)
        tk.Button(button_frame, text="Quit", command=self.root.quit).pack(side=tk.RIGHT)

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

        box1 = self.select_box("Select the first class")
        box2 = self.select_box("Select the second class")

        if box1 and box2:
            line_type = simpledialog.askstring(
                "Line Type",
                "Enter line type (association, dependency, inheritance, composition, aggregation):"
            )
            if line_type in {"association", "dependency", "inheritance", "composition", "aggregation"}:
                line = AssociationLine(self.canvas, box1, box2, line_type)
                self.associations.append(line)
            else:
                messagebox.showerror("Error", "Invalid line type.")

    def select_box(self, prompt):
        """Prompt the user to select a class box."""
        options = [box.class_name for box in self.class_boxes]
        selected = simpledialog.askstring(prompt, f"Available classes: {', '.join(options)}")

        for box in self.class_boxes:
            if box.class_name == selected:
                return box
        messagebox.showerror("Error", "Class not found.")
        return None

    def on_drag(self, event):
        """Handle drag events for moving boxes."""
        if not self.drag_data["item"]:
            item = self.canvas.find_closest(event.x, event.y)[0]
            for box in self.class_boxes:
                if box.rect == item:
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
            for assoc in self.associations:
                assoc.update_line()

    def on_release(self, event):
        """Handle mouse release."""
        self.drag_data["item"] = None