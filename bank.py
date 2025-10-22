def show_balance():
    print(f"Your money in balance is : ${balance:.2f}")
def deposit():
    amount=float(input("Enter an amount to be deposits:"))
    if amount<0:
        print("That`s not a valid amount")
        return 0
    else:
        return amount
def withdraw():
    amount=float(input("Input your money to withdraw:"))
    if amount>balance:
        print("your money is not enough")
    elif amount<0:
        print("Amout must be greater than 0")
    else:
        return amount
balance=0
is_running=True
while is_running:
    print("----------------Banking Program-----------")
    print("1.Show balance")
    print("2.Deposit")
    print("3.Withdraw")
    print("4.Exit")

    op=input("Please inout your choice (1 to 4):")
    if op=='1':
        show_balance()
    elif op=='2':
        balance+=deposit()
    elif op=='3':
        balance-=withdraw()
    elif op=='4':
        is_running=False
    else:
        print("Please Input again ...!")


    