import tkinter as tk

class ClassBox:
    """Represents a UML class box with a PlantUML-like design."""

    def __init__(self, canvas, x, y, class_name, attributes, methods):
        self.canvas = canvas
        self.class_name = class_name
        self.attributes = attributes
        self.methods = methods
        self.width = 240
        self.x = x
        self.y = y

        # Dynamically calculate height based on attributes and methods
        self.height = max(80 + 20 * len(attributes) + 20 * len(methods), 130)

        self.rect = None
        self.text_ids = []
        self.lines = []
        self.create_box()

    def create_box(self):
        """Draws the UML class box with a clear tabular structure."""
        # Main Rectangle for Class Box
        self.rect = self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + self.height, fill="white", outline="black"
        )

        # Class Name Section
        self.canvas.create_rectangle(
            self.x, self.y, self.x + self.width, self.y + 30, fill="#5dade2", outline="black"
        )
        self.text_ids.append(
            self.canvas.create_text(
                self.x + self.width / 2, self.y + 15, text=self.class_name, font=("Arial", 12, "bold"), fill="white"
            )
        )

        # Attributes Section
        y_offset = self.y + 30
        self.canvas.create_line(self.x, y_offset, self.x + self.width, y_offset, fill="black")
        y_offset += 5
        for attr in self.attributes:
            self.text_ids.append(
                self.canvas.create_text(
                    self.x + 10, y_offset, text=f"- {attr}", anchor="w", font=("Arial", 10)
                )
            )
            y_offset += 20

        # Methods Section
        self.canvas.create_line(self.x, y_offset, self.x + self.width, y_offset, fill="black")
        y_offset += 5
        for method in self.methods:
            self.text_ids.append(
                self.canvas.create_text(
                    self.x + 10, y_offset, text=f"+ {method}()", anchor="w", font=("Arial", 10)
                )
            )
            y_offset += 20

    def move(self, dx, dy):
        """Move the class box and its elements."""
        self.canvas.move(self.rect, dx, dy)
        for text_id in self.text_ids:
            self.canvas.move(text_id, dx, dy)
        self.x += dx
        self.y += dy