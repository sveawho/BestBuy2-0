import pytest
from products import Product

def test_create_normal_product():
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active == True


def test_create_product_with_invalid_details_empty_name():
    with pytest.raises(ValueError):
        Product("", price=1450, quantity=100)

def test_create_product_with_invalid_details_negative_price():
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-10, quantity=100)

def test_product_quantity_reaches_zero_becomes_inactive():
    product = Product("Test Product", price=10, quantity=1)
    assert product.is_active == True
    product.buy(1)
    assert product.quantity == 0  # Ensure quantity is zero
    assert product.is_active == False  # Ensure product is inactive after quantity becomes zero


def test_product_purchase_modifies_quantity_and_returns_right_output():
    product = Product("Test Product", price=10, quantity=5)
    total_price = product.buy(3)
    assert total_price == 30
    assert product.quantity == 2

def test_buying_larger_quantity_than_exists_invokes_exception():
    product = Product("Test Product", price=10, quantity=5)
    with pytest.raises(ValueError):
        product.buy(10)
