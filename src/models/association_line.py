class AssociationLine:
    """Represents an association line with different UML relationship types."""

    def __init__(self, canvas, box1, box2, line_type="association"):
        self.canvas = canvas
        self.box1 = box1
        self.box2 = box2
        self.line_type = line_type
        self.line = None
        self.arrow = None
        self.create_line()

    def create_line(self):
        """Creates the initial line."""
        self.update_line()

    def update_line(self):
        """Updates the line position and style."""
        if self.line:
            self.canvas.delete(self.line)
        if self.arrow:
            self.canvas.delete(self.arrow)

        # Calculate line endpoints
        x1, y1 = self.get_closest_edge(self.box1, self.box2)
        x2, y2 = self.get_closest_edge(self.box2, self.box1)

        # Set line style based on relationship type
        dash_pattern = None
        if self.line_type == "dependency":
            dash_pattern = (6, 2)

        # Draw the main line
        self.line = self.canvas.create_line(
            x1, y1, x2, y2,
            width=1,
            dash=dash_pattern,
            fill="black"
        )

        # Calculate arrow direction
        dx = x2 - x1
        dy = y2 - y1
        length = (dx * dx + dy * dy) ** 0.5
        if length == 0:
            return
        udx, udy = dx / length, dy / length

        # Draw appropriate arrow/symbol based on relationship type
        if self.line_type == "inheritance":
            self.draw_inheritance_arrow(x2, y2, udx, udy)
        elif self.line_type == "composition":
            self.draw_diamond(x2, y2, udx, udy, filled=True)
        elif self.line_type == "aggregation":
            self.draw_diamond(x2, y2, udx, udy, filled=False)
        elif self.line_type == "association":
            self.draw_association_arrow(x2, y2, udx, udy)

    def get_closest_edge(self, box_from, box_to):
        """Calculate the closest edge point between two boxes."""
        x_center = box_from.x + box_from.width / 2
        y_center = box_from.y + box_from.height / 2

        to_x = box_to.x + box_to.width / 2
        to_y = box_to.y + box_to.height / 2

        dx = to_x - x_center
        dy = to_y - y_center

        if abs(dx) > abs(dy):
            if dx > 0:
                return box_from.x + box_from.width, y_center
            else:
                return box_from.x, y_center
        else:
            if dy > 0:
                return x_center, box_from.y + box_from.height
            else:
                return x_center, box_from.y

    def draw_inheritance_arrow(self, x, y, udx, udy):
        """Draw a hollow triangle for inheritance."""
        size = 12
        points = [
            (x, y),
            (x - size * udx + size * udy, y - size * udy - size * udx),
            (x - size * udx - size * udy, y - size * udy + size * udx)
        ]
        self.arrow = self.canvas.create_polygon(
            points, fill="white", outline="black"
        )

    def draw_association_arrow(self, x, y, udx, udy):
        """Draw a simple arrow for association."""
        size = 10
        self.arrow = self.canvas.create_line(
            x, y,
            x - size * udx + size/2 * udy, y - size * udy - size/2 * udx,
            x - size * udx - size/2 * udy, y - size * udy + size/2 * udx,
            fill="black"
        )

    def draw_diamond(self, x, y, udx, udy, filled=False):
        """Draw a diamond for aggregation/composition."""
        size = 10
        points = [
            (x, y),
            (x - size * udx + size * udy, y - size * udy - size * udx),
            (x - 2 * size * udx, y - 2 * size * udy),
            (x - size * udx - size * udy, y - size * udy + size * udx)
        ]
        self.arrow = self.canvas.create_polygon(
            points,
            fill="black" if filled else "white",
            outline="black"
        )
