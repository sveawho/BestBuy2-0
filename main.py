import products
import store
from products import LimitedProduct



def start(store_obj):
    """Start the user interface for interacting with the store."""
    while True:
        print("\n   Store Menu")
        print("   ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose a number: ")

        if choice == "1":
            print("------")
            display_all_products(store_obj)
            print("------")
        elif choice == "2":
            print("Total of", store_obj.get_total_quantity(), "items in store")
        elif choice == "3":
            make_order(store_obj)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number between 1 and 4.")


def display_all_products(store_obj):
    """Display all products in the store."""
    products = store_obj.get_all_products()
    for i, product in enumerate(products, 1):
        print(f"{i}. {product}")  # Use __str__ method to display product info
    return products  # Return products list

def make_order(store_obj):
    """Make an order for products."""
    print("------")
    products = display_all_products(store_obj)  # Access products list from display_all_products
    print("------")
    shopping_list = []
    while True:
        product_num = input("When you want to finish order, enter empty text.\n"
                            "Which product # do you want? ")
        if not product_num:
            break
        try:
            product_num = int(product_num)
            if product_num < 1 or product_num > len(products):
                print("Invalid product number.")
                continue
        except ValueError:
            print("Invalid input.")
            continue
        product = products[product_num - 1]
        try:
            amount = int(input("What amount do you want? "))
            if amount <= 0:
                print("Invalid amount.")
                continue
            if isinstance(product, LimitedProduct) and amount > product.maximum:
                print(f"Error: Quantity exceeds maximum allowed ({product.maximum}).")
                continue
        except ValueError:
            print("Invalid input.")
            continue
        shopping_list.append((product, amount))
        print("Product added to list!")
    try:
        total_price = store_obj.order(shopping_list)
        print("********")
        print("Order made! Total payment:", total_price)
    except ValueError as error_message:
        print("Error while making order!", error_message)


if __name__ == "__main__":
    # setup initial stock of inventory
    mac = products.Product("MacBook Air M2", price=1450, quantity=100)
    bose = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    pixel = products.Product("Google Pixel 7", price=500, quantity=250)
    windows_license = products.NonStockedProduct("Windows License", price=125)
    shipping = products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)


    # Define promotions
    mac.promotion = products.SecondItemHalfPrice("Second Half price!")
    bose.promotion = products.Buy2Get1Free("Third One Free!")
    windows_license.promotion = products.PercentageDiscount("30% off!", 30)

    best_buy = store.Store([mac, bose, pixel, windows_license, shipping])

    # Start the user interface
    start(best_buy)

