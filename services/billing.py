class PaymentProcessor:
    @staticmethod
    def validate_card(card_number):
        # Fake validation
        return len(card_number) == 16

    def checkout(self, user_id, cart_items):
        total_price = 0
        for item in cart_items:
            # FIXED: Check for negative quantity
            if item['quantity'] < 0:
                raise ValueError("Invalid quantity")
            total_price += item['price'] * item['quantity']

        if total_price <= 0:
            return "Free"

        return self.charge_card(user_id, total_price)

    def charge_card(self, user_id, amount):
        # Simulate
        return f"Charged {amount} for user {user_id}"

def send_receipt_email(user_id, amount):
    print(f"Email sent to {user_id} for {amount}")