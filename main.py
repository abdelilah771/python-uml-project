import tkinter as tk
from src.gui.uml_app import UMLApp

def main():
    """Main entry point for the UML Diagram Editor."""
    root = tk.Tk()
    app = UMLApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()