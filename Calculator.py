# Calculator Application
def calculator():
    print("Simple Calculator")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    
    try:
        operation = int(input("Select operation (1-4): "))
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        
        if operation == 1:
            print(f"Result: {num1 + num2}")
        elif operation == 2:
            print(f"Result: {num1 - num2}")
        elif operation == 3:
            print(f"Result: {num1 * num2}")
        elif operation == 4:
            if num2 != 0:
                print(f"Result: {num1 / num2}")
            else:
                print("Error: Cannot divide by zero")
        else:
            print("Invalid operation")
    except ValueError:
        print("Please enter valid numbers")


# Run either application
if __name__ == "__main__":
    
    
    
