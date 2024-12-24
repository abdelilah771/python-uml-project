class AssociationLine:
    """Represents an association line with different UML relationship types."""

    def __init__(self, canvas, box1, box2, line_type="association"):
        """
        Initialize an AssociationLine instance.

        Parameters:
        - canvas (tk.Canvas): The Tkinter canvas where the line will be drawn.
        - box1 (ClassBox): The first UML class box connected by the association.
        - box2 (ClassBox): The second UML class box connected by the association.
        - line_type (str): The type of UML relationship (e.g., "association", "dependency").
                           Defaults to "association".
        """
        self.canvas = canvas            # Reference to the Tkinter canvas
        self.box1 = box1                # First class box
        self.box2 = box2                # Second class box
        self.line_type = line_type      # Type of association
        self.line = None                # Canvas line ID
        self.arrow = None               # Canvas arrow or symbol ID
        self.create_line()              # Create the initial line upon initialization

    def create_line(self):
        """Creates the initial association line by calling update_line."""
        self.update_line()

    def update_line(self):
        """
        Updates the line's position and style based on the connected class boxes.

        This method recalculates the line's endpoints, styles it according to the
        association type, and redraws any arrows or symbols to represent the relationship.
        """
        if self.line:
            self.canvas.delete(self.line)  # Remove the existing line from the canvas
        if self.arrow:
            self.canvas.delete(self.arrow)  # Remove the existing arrow/symbol from the canvas

        # Calculate the closest edge points between the two class boxes for the line endpoints
        x1, y1 = self.get_closest_edge(self.box1, self.box2)
        x2, y2 = self.get_closest_edge(self.box2, self.box1)

        # Determine the dash pattern based on the relationship type
        dash_pattern = None
        if self.line_type == "dependency":
            dash_pattern = (6, 2)  # Dashed line for dependency

        # Draw the main association line on the canvas
        self.line = self.canvas.create_line(
            x1, y1, x2, y2,
            width=1,                 # Line width
            dash=dash_pattern,       # Dash pattern (if any)
            fill="black"             # Line color
        )

        # Calculate the direction vector for the arrow/symbol
        dx = x2 - x1
        dy = y2 - y1
        length = (dx * dx + dy * dy) ** 0.5  # Euclidean distance between points
        if length == 0:
            return  # Avoid division by zero if both points are identical
        udx, udy = dx / length, dy / length  # Unit direction vector

        # Draw the appropriate arrow or symbol based on the relationship type
        if self.line_type == "inheritance":
            self.draw_inheritance_arrow(x2, y2, udx, udy)
        elif self.line_type == "composition":
            self.draw_diamond(x2, y2, udx, udy, filled=True)
        elif self.line_type == "aggregation":
            self.draw_diamond(x2, y2, udx, udy, filled=False)
        elif self.line_type == "association":
            self.draw_association_arrow(x2, y2, udx, udy)

    def get_closest_edge(self, box_from, box_to):
        """
        Calculate the closest edge point between two class boxes.

        Parameters:
        - box_from (ClassBox): The class box from which the line originates.
        - box_to (ClassBox): The class box to which the line points.

        Returns:
        - tuple: (x, y) coordinates of the closest edge point on box_from towards box_to.
        """
        # Calculate the center coordinates of box_from
        x_center = box_from.x + box_from.width / 2
        y_center = box_from.y + box_from.height / 2

        # Calculate the center coordinates of box_to
        to_x = box_to.x + box_to.width / 2
        to_y = box_to.y + box_to.height / 2

        # Calculate the difference in coordinates
        dx = to_x - x_center
        dy = to_y - y_center

        # Determine the closest edge based on the dominant direction
        if abs(dx) > abs(dy):
            if dx > 0:
                return box_from.x + box_from.width, y_center  # Right edge
            else:
                return box_from.x, y_center                     # Left edge
        else:
            if dy > 0:
                return x_center, box_from.y + box_from.height  # Bottom edge
            else:
                return x_center, box_from.y                     # Top edge

    def draw_inheritance_arrow(self, x, y, udx, udy):
        """
        Draw a hollow triangle to represent inheritance.

        Parameters:
        - x (float): X-coordinate of the arrow's base point.
        - y (float): Y-coordinate of the arrow's base point.
        - udx (float): Unit direction vector component in the X-axis.
        - udy (float): Unit direction vector component in the Y-axis.
        """
        size = 12  # Size of the inheritance arrow
        # Calculate the three points of the triangle
        points = [
            (x, y),  # Tip of the arrow
            (x - size * udx + size * udy, y - size * udy - size * udx),
            (x - size * udx - size * udy, y - size * udy + size * udx)
        ]
        # Draw the hollow triangle on the canvas
        self.arrow = self.canvas.create_polygon(
            points, fill="white", outline="black"
        )

    def draw_association_arrow(self, x, y, udx, udy):
        """
        Draw a simple arrow to represent an association.

        Parameters:
        - x (float): X-coordinate of the arrow's base point.
        - y (float): Y-coordinate of the arrow's base point.
        - udx (float): Unit direction vector component in the X-axis.
        - udy (float): Unit direction vector component in the Y-axis.
        """
        size = 10  # Size of the association arrow
        # Draw a V-shaped arrowhead
        self.arrow = self.canvas.create_line(
            x, y,
            x - size * udx + size/2 * udy, y - size * udy - size/2 * udx,
            x - size * udx - size/2 * udy, y - size * udy + size/2 * udx,
            fill="black"
        )

    def draw_diamond(self, x, y, udx, udy, filled=False):
        """
        Draw a diamond shape to represent aggregation or composition.

        Parameters:
        - x (float): X-coordinate of the diamond's base point.
        - y (float): Y-coordinate of the diamond's base point.
        - udx (float): Unit direction vector component in the X-axis.
        - udy (float): Unit direction vector component in the Y-axis.
        - filled (bool): Whether the diamond is filled (True for composition, False for aggregation).
        """
        size = 10  # Size of the diamond
        # Calculate the four points of the diamond
        points = [
            (x, y),  # Right point
            (x - size * udx + size * udy, y - size * udy - size * udx),  # Top point
            (x - 2 * size * udx, y - 2 * size * udy),  # Left point
            (x - size * udx - size * udy, y - size * udy + size * udx)   # Bottom point
        ]
        # Draw the diamond on the canvas
        self.arrow = self.canvas.create_polygon(
            points,
            fill="black" if filled else "white",  # Filled for composition, hollow for aggregation
            outline="black"
        )
