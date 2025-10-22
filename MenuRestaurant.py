menu={
    "pizza":3.00,
    "nachos":4.50,
    "popocorn":6.00,
    "fries":2.50,
    "pretzel":3.50,
    "soda":3.00,
    "lemonade":4.25
}
cart=[]
total=0
print("-------Menu---------")
for key,value in menu.items():
    print(f"{key}: ${value}")
print("--------------------")
while True:
    food=input("Select an item (q to quit):").lower()
    if food=="q":
        break
    elif menu.get(food) is not None:
        cart.append(food)
print("------Your order------")
for food in cart:

    total+=menu.get(food)
print(f"Total:${total:.2f}")