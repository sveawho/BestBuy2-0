from abc import ABC, abstractmethod


class Product:
    """Represents a product available in the store."""

    def __init__(self, name, price, quantity):
        """Initialize the product with name, price, and quantity."""
        if not name or price < 0 or quantity < 0:
            raise ValueError("Invalid input for product initialization.")

        self._name = name
        self._price = price
        self._quantity = quantity
        self._active = True
        self._promotion = None  # Initialize promotion to None

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        if self._quantity <= 0:
            self._quantity = 0
            self._active = False  # Set active to False when quantity becomes zero
        else:
            self._active = True  # Set active to True when quantity is non-zero


    @property
    def is_active(self):
        """Check if the product is active."""
        return self._active

    @property
    def promotion(self):
        """Get the promotion applied to the product."""
        return self._promotion

    @promotion.setter
    def promotion(self, value):
        """Set the promotion applied to the product."""
        self._promotion = value

    def activate(self):
        """Activate the product."""
        self._active = True

    def deactivate(self):
        """Deactivate the product."""
        self._active = False

    def buy(self, quantity):
        """Buy a certain quantity of the product."""
        if quantity <= 0 or quantity > self.quantity:
            raise ValueError("Invalid quantity for purchase.")

        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        self._quantity -= quantity
        if self._quantity == 0:
            self._active = False  # Set is_active to False when quantity becomes zero

        return total_price

    def __str__(self):
        """String representation of the product."""
        promotion_info = f", Promotion: {self.promotion.name}" if self.promotion else ", Promotion: None"
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}{promotion_info}"

    def __gt__(self, other):
        """Comparison: greater than."""
        return self.price > other.price

    def __lt__(self, other):
        """Comparison: less than."""
        return self.price < other.price

    def __eq__(self, other):
        """Comparison: equal."""
        return self.price == other.price

    def __contains__(self, store):
        """Check if the product exists in the store."""
        return self in store.products


class NonStockedProduct(Product):
    """Represents a non-stocked product."""

    def __init__(self, name, price):
        """Initialize the non-stocked product with name and price."""
        super().__init__(name, price, quantity=0)  # Quantity always set to zero for non-stocked products

    def buy(self, quantity):
        """Buy the non-stocked product."""
        if quantity <= 0:
            raise ValueError("Invalid quantity for purchase.")

        if self.promotion:
            total_price = self.promotion.apply_promotion(self, quantity)
        else:
            total_price = quantity * self.price

        return total_price

    def __str__(self):
        """String representation of the non-stocked product."""
        promotion_info = f"Promotion: {self.promotion.name}" if self.promotion else ""
        return f"{self.name}, Price: ${self.price}, Quantity: Unlimited, Promotion: {promotion_info}"


class LimitedProduct(Product):
    """Represents a limited product."""

    def __init__(self, name, price, quantity=None, maximum=None):
        """Initialize the limited product with name, price, quantity, and maximum quantity."""
        super().__init__(name, price, quantity)
        self._maximum = maximum

    @property
    def maximum(self):
        return self._maximum

    def __str__(self):
        """String representation of the limited product."""
        promotion_info = f"Promotion: {self.promotion.name}" if self.promotion else "Promotion: None"
        return f"{self.name}, Price: ${self.price}, Limited to 1 per order!, {promotion_info}"


class Promotion(ABC):
    """Abstract class representing a promotion."""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        """Apply the promotion to the product and return the discounted price."""
        pass


class PercentageDiscount(Promotion):
    """Represents a percentage discount promotion."""

    def __init__(self, name, discount_percentage):
        super().__init__(name)
        self.discount_percentage = discount_percentage

    def apply_promotion(self, product, quantity):
        """Apply the percentage discount promotion."""
        discounted_price = product.price * (1 - self.discount_percentage / 100)
        return discounted_price * quantity

class SecondItemHalfPrice(Promotion):
    """Represents a second item at half price promotion."""

    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity):
        """Apply the second item at half price promotion."""
        full_price_items = quantity // 2
        half_price_items = quantity - full_price_items
        total_price = (full_price_items * product.price) + (half_price_items * (product.price / 2))
        return total_price


class Buy2Get1Free(Promotion):
    """Represents a buy 2, get 1 free promotion."""

    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity):
        """Apply the buy 2, get 1 free promotion."""
        full_price_items = quantity // 3 * 2
        free_items = quantity // 3
        total_price = (full_price_items * product.price)
        return total_price
