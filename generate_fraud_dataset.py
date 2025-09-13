import pandas as pd
import random

payment_types = ["cash on delivery", "credit card", "paytm", "paypal"]

def generate_user_id():
    return str(random.randint(10000, 99999))

def generate_typing_speed(is_fraud):
    if is_fraud:
        return random.randint(120, 300)  # Suspiciously fast
    return random.randint(20, 90)        # Normal human

def generate_time_on_page(is_fraud):
    if is_fraud:
        return random.randint(5, 30)     # Very short
    return random.randint(45, 600)       # Normal

def generate_payment_type(is_fraud):
    # Assume fraudsters prefer credit card or paypal
    if is_fraud:
        return random.choices(["credit card", "paypal"], k=1)[0]
    return random.choice(payment_types)

rows = []
for i in range(500):
    is_fraud = random.choices([0, 1], weights=[0.9, 0.1])[0]  # 10% fraud
    typing_speed = generate_typing_speed(is_fraud)
    time_on_page = generate_time_on_page(is_fraud)
    payment_type = generate_payment_type(is_fraud)
    user_id = generate_user_id()
    rows.append([typing_speed, time_on_page, payment_type, user_id, is_fraud])

df = pd.DataFrame(rows, columns=[
    "typing_speed", "time_on_page", "payment_type", "user_id", "is_fraud"
])

df.to_csv("ai_orders_training.csv", index=False)
print("Generated dataset saved as ai_orders_training.csv")