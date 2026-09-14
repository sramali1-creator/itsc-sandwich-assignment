class SandwichMaker:
    """A ham sandwich vending machine."""

    # Sets up the machine with starting resources
    def __init__(self, machine_resources):
        self.resources = machine_resources

    # Verifies enough ingredients are available before proceeding
    def check_resources(self, ingredients):
        """Returns True if there are enough resources to make the sandwich, False otherwise."""
        for item in ingredients:
            if ingredients[item] > self.resources[item]:
                print(f"Sorry there is not enough {item}.")
                return False
        return True
it
    # Collects coin input and returns the total dollar amount
    def process_coins(self):
        """Prompts the user for coins and returns the total monetary value inserted."""
        print("Please insert coins.")
        large_dollars = int(input("how many large dollars?: "))
        half_dollars = int(input("how many half dollars?: "))
        quarters = int(input("how many quarters?: "))
        nickels = int(input("how many nickels?: "))

        total = (large_dollars * 1) + (half_dollars * 0.5) + (quarters * 0.25) + (nickels * 0.05)
        return total

    # Checks if the coins inserted cover the cost, and gives change if needed
    def transaction_result(self, coins, cost):
        """Returns True if payment covers the cost (and gives change), False otherwise."""
        if coins < cost:
            print("Sorry that's not enough money. Money refunded.")
            return False
        else:
            change = round(coins - cost, 2)
            print(f"Here is ${change} in change.")
            return True


    # Updates resources and confirms the sandwich is ready
    def make_sandwich(self, sandwich_size, order_ingredients):
        """Deducts the sandwich's ingredients from the machine's resources."""
        for item in order_ingredients:
            self.resources[item] -= order_ingredients[item]
        print(f"{sandwich_size} sandwich is ready. Bon appetit!")

    # Displays the current remaining resources
    def report(self):
        print(f"Bread: {self.resources['bread']} slice(s)")
        print(f"Ham: {self.resources['ham']} slice(s)")
        print(f"Cheese: {self.resources['cheese']} pound(s)")


# Recipes dictionary: defines ingredients and cost for each sandwich size
recipes = {
    "small": {
        "ingredients": {"bread": 2, "ham": 4, "cheese": 4},
        "cost": 1.75,
    },
    "medium": {
        "ingredients": {"bread": 4, "ham": 6, "cheese": 8},
        "cost": 3.25,
    },
    "large": {
        "ingredients": {"bread": 6, "ham": 8, "cheese": 12},
        "cost": 5.5,
    },
}

# Starting resources for the machine
resources = {
    "bread": 12,
    "ham": 18,
    "cheese": 24,
}


# Main program loop that runs the sandwich machine
def main():
    machine = SandwichMaker(resources)
    is_on = True

    while is_on:
        choice = input("What would you like? (small/ medium/ large/ off/ report): ").lower()

        if choice == "off":
            is_on = False
        elif choice == "report":
            machine.report()
        elif choice in recipes:
            order = recipes[choice]
            if machine.check_resources(order["ingredients"]):
                payment = machine.process_coins()
                if machine.transaction_result(payment, order["cost"]):
                    machine.make_sandwich(choice, order["ingredients"])
        else:
            print("Please choose small, medium, large, off, or report.")


if __name__ == "__main__":
    main()
