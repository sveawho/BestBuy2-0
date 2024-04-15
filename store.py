from typing import List
from products import Product
from products import NonStockedProduct, LimitedProduct


class Store:
    """Represents a store containing products."""

    def __init__(self, products: List[Product]):
        """Initialize the store with a list of products."""
        self.products = products

    def add_product(self, product):
        """Add a product to the store."""
        self.products.append(product)

    def remove_product(self, product):
        """Remove a product from the store."""
        self.products.remove(product)

    def get_total_quantity(self):
        """Get the total quantity of items in the store."""
        total_quantity = 0
        for product in self.products:
            if not isinstance(product, (NonStockedProduct)):
                total_quantity += product.quantity
        return total_quantity

    def get_all_products(self) -> List[Product]:
        """Get all active products in the store."""
        active_products = [product for product in self.products if product.is_active]
        return active_products

    def order(self, shopping_list) -> float:
        """Make an order for products."""
        total_price = 0
        for product, quantity in shopping_list:
            if product.is_active:
                total_price += product.buy(quantity)
            else:
                raise ValueError("Invalid product in shopping list.")
        return total_price

    def __add__(self, other_store):
        """Combine two stores by adding their products."""
        combined_store = Store(self.products + other_store.products)
        return combined_store
