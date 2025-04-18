import random

def play_game():
    choices = ['rock', 'paper', 'scissors']
    
    while True:
        print("\nRock, Paper, Scissors - Shoot!")
        
        # Get player's choice
        player_choice = input("Enter your choice (rock/paper/scissors) or 'quit' to exit: ").lower()
        if player_choice == 'quit':
            break
            
        if player_choice not in choices:
            print("Invalid choice! Please try again.")
            continue
            
        # Computer's choice
        computer_choice = random.choice(choices)
        print(f"\nYou chose: {player_choice}")
        print(f"Computer chose: {computer_choice}")
        
        # Determine winner
        if player_choice == computer_choice:
            print("It's a tie!")
        elif (player_choice == 'rock' and computer_choice == 'scissors') or \
             (player_choice == 'paper' and computer_choice == 'rock') or \
             (player_choice == 'scissors' and computer_choice == 'paper'):
            print("You win!")
        else:
            print("Computer wins!")

if __name__ == "__main__":
    play_game()
