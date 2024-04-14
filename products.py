class Product:
    """Represents a product available in the store."""

    def __init__(self, name, price, quantity):
        """Initialize the product with name, price, and quantity."""
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid input for product initialization.")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self):
        """Get the quantity of the product."""
        return self.quantity

    def set_quantity(self, quantity):
        """Set the quantity of the product."""
        self.quantity = quantity
        if self.quantity <= 0:
            self.deactivate()

    def is_active(self):
        """Check if the product is active."""
        return self.active

    def activate(self):
        """Activate the product."""
        self.active = True

    def deactivate(self):
        """Deactivate the product."""
        self.active = False

    def show(self):
        """Display information about the product."""
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity):
        """Buy a certain quantity of the product."""
        if quantity <= 0 or quantity > self.quantity:
            raise ValueError("Invalid quantity for purchase.")

        total_price = quantity * self.price
        self.quantity -= quantity
        if self.quantity <= 0:
            self.deactivate()
        return total_price
