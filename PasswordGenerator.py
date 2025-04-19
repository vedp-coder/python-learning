import random
import string
import pyperclip  # For copying password to clipboard

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate_password(self, length=12, use_uppercase=True, use_digits=True, use_special=True):
        # Create character pool based on requirements
        char_pool = self.lowercase
        if use_uppercase:
            char_pool += self.uppercase
        if use_digits:
            char_pool += self.digits
        if use_special:
            char_pool += self.special_chars
            
        # Ensure minimum requirements are met
        password = []
        if use_uppercase:
            password.append(random.choice(self.uppercase))
        if use_digits:
            password.append(random.choice(self.digits))
        if use_special:
            password.append(random.choice(self.special_chars))
            
        # Fill remaining length with random characters
        remaining_length = length - len(password)
        password.extend(random.choice(char_pool) for _ in range(remaining_length))
        
        # Shuffle the password
        random.shuffle(password)
        return ''.join(password)
    
    def check_password_strength(self, password):
        score = 0
        checks = {
            'length': len(password) >= 12,
            'uppercase': any(c.isupper() for c in password),
            'lowercase': any(c.islower() for c in password),
            'digits': any(c.isdigit() for c in password),
            'special': any(c in self.special_chars for c in password)
        }
        
        return {
            'score': sum(checks.values()),
            'checks': checks
        }

def main():
    generator = PasswordGenerator()
    
    while True:
        print("\nPassword Generator Menu:")
        print("1. Generate Password")
        print("2. Check Password Strength")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            length = int(input("Enter password length (minimum 8): "))
            use_upper = input("Include uppercase letters? (y/n): ").lower() == 'y'
            use_digits = input("Include numbers? (y/n): ").lower() == 'y'
            use_special = input("Include special characters? (y/n): ").lower() == 'y'
            
            password = generator.generate_password(
                length=max(8, length),
                use_uppercase=use_upper,
                use_digits=use_digits,
                use_special=use_special
            )
            
            print(f"\nGenerated Password: {password}")
            pyperclip.copy(password)
            print("Password copied to clipboard!")
            
        elif choice == '2':
            password = input("Enter password to check: ")
            result = generator.check_password_strength(password)
            
            print(f"\nPassword Strength Score: {result['score']}/5")
            print("\nChecks:")
            for check, passed in result['checks'].items():
                print(f"{check}: {'✓' if passed else '✗'}")
                
        elif choice == '3':
            print("Thank you for using Password Generator!")
            break
            
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
