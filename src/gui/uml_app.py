import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import json
from ..models.class_box import ClassBox
from ..models.association_line import AssociationLine
from ..models.code_generator import generate_code_from_diagram

# Define the main application class for the UML Diagram Editor
class UMLApp:
    """Main application to manage the UML Diagram Editor."""

    def __init__(self, root):
        """
        Initialize the UMLApp with the main Tkinter window.

        Parameters:
        - root: The root Tkinter window.
        """
        self.root = root
        self.root.title("Modern UML Diagram Editor")  # Set the window title

        # Create a canvas widget where UML elements will be drawn
        self.canvas = tk.Canvas(root, bg="white", width=900, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Make the canvas expandable

        self.class_boxes = []     # List to store all UML class boxes
        self.associations = []    # List to store all associations between classes

        # Dictionary to manage dragging state
        self.drag_data = {"item": None, "start_x": 0, "start_y": 0}

        # Bind mouse events to their respective handlers
        self.canvas.bind("<B1-Motion>", self.on_drag)          # Left mouse button drag
        self.canvas.bind("<ButtonRelease-1>", self.on_release) # Left mouse button release
        self.canvas.bind("<Button-3>", self.delete_item)       # Right mouse button click for deletion

        # Set up the user interface components like menus
        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface with a menu bar."""
        menu_bar = tk.Menu(self.root)  # Create a menu bar

        # File Menu
        file_menu = tk.Menu(menu_bar, tearoff=0)  # Create a submenu for 'File'
        file_menu.add_command(label="Generate Code", command=self.generate_code)  # Add 'Generate Code' option
        file_menu.add_command(label="Save Diagram", command=self.save_diagram)      # Add 'Save Diagram' option
        file_menu.add_command(label="Load Diagram", command=self.load_diagram)      # Add 'Load Diagram' option
        file_menu.add_command(label="Quit", command=self.root.quit)                 # Add 'Quit' option
        menu_bar.add_cascade(label="File", menu=file_menu)                        # Add 'File' menu to the menu bar

        # Edit Menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)  # Create a submenu for 'Edit'
        edit_menu.add_command(label="Add Class", command=self.add_class)           # Add 'Add Class' option
        edit_menu.add_command(label="Add Association", command=self.add_association) # Add 'Add Association' option
        menu_bar.add_cascade(label="Edit", menu=edit_menu)                        # Add 'Edit' menu to the menu bar

        self.root.config(menu=menu_bar)  # Configure the root window to display the menu bar

    def add_class(self):
        """Add a new class box to the canvas."""
        # Prompt the user to enter the class name
        class_name = simpledialog.askstring("Class Name", "Enter the class name:")
        # Prompt the user to enter class attributes, separated by commas
        attributes = simpledialog.askstring("Attributes", "Enter attributes (comma-separated):")
        # Prompt the user to enter class methods, separated by commas
        methods = simpledialog.askstring("Methods", "Enter methods (comma-separated):")

        if class_name:
            # Split the attributes string into a list, stripping any extra whitespace
            attr_list = [attr.strip() for attr in attributes.split(",")] if attributes else []
            # Split the methods string into a list, stripping any extra whitespace
            method_list = [method.strip() for method in methods.split(",")] if methods else []
            # Create a new ClassBox instance at position (100, 100) with the provided details
            box = ClassBox(self.canvas, 100, 100, class_name, attr_list, method_list)
            # Add the new class box to the list of class boxes
            self.class_boxes.append(box)

    def add_association(self):
        """Add an association line between two existing classes."""
        # Ensure there are at least two classes to create an association
        if len(self.class_boxes) < 2:
            messagebox.showerror("Error", "You need at least two classes to create an association.")
            return

        # Retrieve the names of all existing classes
        box_names = [box.class_name for box in self.class_boxes]
        # Prompt the user to select the first class for association
        box1_name = simpledialog.askstring("Class Selection", f"Select the first class:\n{', '.join(box_names)}")
        # Prompt the user to select the second class for association
        box2_name = simpledialog.askstring("Class Selection", f"Select the second class:\n{', '.join(box_names)}")

        # Find the ClassBox instances corresponding to the selected class names
        box1 = next((box for box in self.class_boxes if box.class_name == box1_name), None)
        box2 = next((box for box in self.class_boxes if box.class_name == box2_name), None)

        if box1 and box2:
            # Prompt the user to enter the type of association
            line_type = simpledialog.askstring(
                "Line Type",
                "Enter line type (association, dependency, inheritance, composition, aggregation):"
            )
            # Validate the entered association type
            if line_type in {"association", "dependency", "inheritance", "composition", "aggregation"}:
                # Create a new AssociationLine between the two classes with the specified type
                line = AssociationLine(self.canvas, box1, box2, line_type)
                # Add the new association to the list of associations
                self.associations.append((line, line_type, box1.class_name, box2.class_name))
            else:
                messagebox.showerror("Error", "Invalid line type.")  # Show error for invalid type
        else:
            messagebox.showerror("Error", "Class not found.")  # Show error if class names are invalid

    def generate_code(self):
        """Generate and display code for all classes in the selected programming language."""
        # Prompt the user to enter the target programming language
        language = simpledialog.askstring(
            "Code Generation", "Enter target language (python, java, php):"
        )
        # Validate the entered language
        if language not in {"python", "java", "php"}:
            messagebox.showerror("Error", "Invalid language. Choose python, java, or php.")
            return

        # Create a summary of all associations in the diagram
        association_summary = "\n".join([
            f"{assoc[2]} -> {assoc[3]} ({assoc[1]})"
            for assoc in self.associations
        ])
        # Display the associations summary to the user
        messagebox.showinfo("Associations", f"Generated Associations:\n{association_summary}")

        code_output = ""  # Initialize a string to hold the generated code
        # Iterate over each class box to generate code based on the selected language
        for box in self.class_boxes:
            if language == "python":
                code_output += box.generate_python_code() + "\n\n"
            elif language == "java":
                code_output += box.generate_java_code() + "\n\n"
            elif language == "php":
                code_output += box.generate_php_code() + "\n\n"

        # Display the generated code in a new window
        self.display_code_in_window(code_output, language)

    def display_code_in_window(self, code, language):
        """Display the generated code in a new Tkinter window."""
        # Create a new top-level window for displaying the code
        code_window = tk.Toplevel(self.root)
        code_window.title(f"Generated Code ({language})")  # Set the window title

        # Create a text widget to display the code
        text_widget = tk.Text(code_window, wrap=tk.WORD)
        text_widget.insert(tk.END, code)             # Insert the generated code
        text_widget.configure(state=tk.DISABLED)      # Make the text widget read-only
        text_widget.pack(fill=tk.BOTH, expand=True)   # Make the text widget expandable

        # Create a button to save the generated code to a file
        save_button = tk.Button(code_window, text="Save Code", command=lambda: self.save_code_to_file(code, language))
        save_button.pack(pady=5)  # Add some padding around the button

    def save_code_to_file(self, code, language):
        """Save the generated code to a file with the appropriate extension."""
        # Open a file save dialog with the correct file extension based on the language
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{language}",
            filetypes=[(f"{language.capitalize()} Files", f"*.{language}")],
            title="Save Generated Code"
        )
        if file_path:
            # Write the generated code to the selected file
            with open(file_path, "w") as file:
                file.write(code)
            # Notify the user of the successful save operation
            messagebox.showinfo("Success", f"Code successfully saved to {file_path}")

    def save_diagram(self):
        """Save the current UML diagram to a JSON file."""
        # Open a file save dialog for JSON files
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Diagram"
        )
        if file_path:
            # Prepare the data structure to serialize the diagram
            data = {
                "classes": [
                    {
                        "name": box.class_name,
                        "attributes": box.attributes,
                        "methods": box.methods,
                        "position": self.canvas.coords(box.box_id)  # Get the position of the class box
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
            # Write the serialized data to the selected JSON file
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)  # Use indentation for readability
            # Notify the user of the successful save operation
            messagebox.showinfo("Success", f"Diagram successfully saved to {file_path}")

    def load_diagram(self):
        """Load a UML diagram from a JSON file."""
        # Open a file open dialog for JSON files
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Load Diagram"
        )
        if file_path:
            # Read and parse the JSON file
            with open(file_path, "r") as file:
                data = json.load(file)

            # Delete all existing class boxes from the canvas
            for box in self.class_boxes:
                box.delete()
            self.class_boxes.clear()  # Clear the class_boxes list

            # Delete all existing associations from the canvas
            for assoc, _, _, _ in self.associations:
                assoc.delete()
            self.associations.clear()  # Clear the associations list

            # Recreate class boxes from the loaded data
            for cls in data["classes"]:
                box = ClassBox(
                    self.canvas,
                    cls["position"][0],          # X-coordinate
                    cls["position"][1],          # Y-coordinate
                    cls["name"],                  # Class name
                    cls["attributes"],            # Class attributes
                    cls["methods"]                # Class methods
                )
                self.class_boxes.append(box)  # Add the recreated box to the list

            # Recreate associations from the loaded data
            for assoc in data["associations"]:
                # Find the source and target ClassBox instances based on their names
                box1 = next((box for box in self.class_boxes if box.class_name == assoc["from"]), None)
                box2 = next((box for box in self.class_boxes if box.class_name == assoc["to"]), None)
                if box1 and box2:
                    # Create a new AssociationLine with the specified type
                    line = AssociationLine(self.canvas, box1, box2, assoc["type"])
                    # Add the new association to the list
                    self.associations.append((line, assoc["type"], assoc["from"], assoc["to"]))

            # Notify the user of the successful load operation
            messagebox.showinfo("Success", "Diagram successfully loaded.")

    def delete_item(self, event):
        """Delete the selected class box or association line based on a right-click event."""
        # Find the closest canvas item to the mouse click position
        item = self.canvas.find_closest(event.x, event.y)[0]
        # Iterate through all class boxes to check if the clicked item is part of any class box
        for box in self.class_boxes:
            if box.box_id == item or item in box.box_parts:
                box.delete()              # Delete the class box from the canvas
                self.class_boxes.remove(box)  # Remove the box from the list
                return  # Exit after deletion

        # Iterate through all associations to check if the clicked item is a line
        for assoc, _, _, _ in self.associations:
            if assoc.line_id == item:
                assoc.delete()             # Delete the association line from the canvas
                self.associations.remove(assoc)  # Remove the association from the list
                return  # Exit after deletion

    def on_drag(self, event):
        """Handle drag events for moving class boxes around the canvas."""
        if not self.drag_data["item"]:
            # If no item is currently being dragged, identify the item under the cursor
            item = self.canvas.find_closest(event.x, event.y)[0]
            # Check if the identified item is part of any class box
            for box in self.class_boxes:
                if box.box_id == item or item in box.box_parts:
                    self.drag_data["item"] = box          # Set the current item being dragged
                    self.drag_data["start_x"] = event.x    # Record the starting X position
                    self.drag_data["start_y"] = event.y    # Record the starting Y position
                    break
        else:
            # Calculate the movement delta
            dx = event.x - self.drag_data["start_x"]
            dy = event.y - self.drag_data["start_y"]
            # Move the class box by the calculated delta
            self.drag_data["item"].move(dx, dy)
            # Update the starting positions for continuous dragging
            self.drag_data["start_x"] = event.x
            self.drag_data["start_y"] = event.y
            # Update all association lines connected to the moved class box
            for assoc, _, _, _ in self.associations:
                assoc.update_line()

    def on_release(self, event):
        """Handle mouse release event to stop dragging."""
        self.drag_data["item"] = None  # Reset the drag data to indicate no item is being dragged
