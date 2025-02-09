from datetime import datetime
from models import Receipt
import math

def calculate_points(receipt: Receipt) -> int:
    points = 0

    # One point for every alphanumeric character in the retailer name
    points += sum(c.isalnum() for c in receipt.retailer)

    # 50 points if the total is a round dollar amount with no cents
    if receipt.total.endswith('.00'):
        points += 50

    # 25 points if the total is a multiple of 0.25
    total_float = float(receipt.total)
    if total_float % 0.25 == 0:
        points += 25

    # 5 points for every two items on the receipt
    points += (len(receipt.items) // 2) * 5

    # Item-specific points calculations
    for item in receipt.items:
        description_length = len(item.shortDescription.strip())
        if description_length % 3 == 0:
            item_price = float(item.price)
            points_from_price = item_price * 0.2
            points += math.ceil(points_from_price)  # Correct rounding up

    # Date and time rules
    purchase_date = datetime.strptime(receipt.purchaseDate, '%Y-%m-%d')
    purchase_time = datetime.strptime(receipt.purchaseTime, '%H:%M')

    # 6 points if the day is odd
    if purchase_date.day % 2 != 0:
        points += 6

    # No points for time as it is not between 2:00 PM and 4:00 PM
    if 14 <= purchase_time.hour < 16:
        points += 10

    return points