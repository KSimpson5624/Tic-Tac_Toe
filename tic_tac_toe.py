#!/usr/bin/env python3

import random

class TicTacToe():
    def __init__(self) -> None:
        self.user_char = 'X'
        self.comp_char = 'O'
        self.place_holder = '*'
        self.board = self.setup_board()
        self.move_log = set()
        self.game_over = False
        self.winning_char = None

    def run(self):
        self.display_board()
        while not self.game_over:
            user_pick = self.get_user_pick()
            self.update_board(user_pick, self.user_char)
            if len(self.move_log) == 9:
                self.display_board()
                break
            comp_pick = self.get_ai_comp_pick()
            self.update_board(comp_pick, self.comp_char)
            self.display_board()
            self.game_over = self.winner()
        if self.winning_char == 'X':
            print('You Win!')
        elif self.winning_char == 'O':
            print('You lose. Better luck next time.')
        elif len(self.move_log) == 9:
            if self.winner() and self.winning_char == 'X':
                print('You Win!')
            elif self.winner() and self.winning_char == 'O':
                print('You lose. Better luck next time.')
            else:
                print("It's a draw!")
        self.again()
        

    def setup_board(self):
        row1 = [self.place_holder, self.place_holder, self.place_holder]
        row2 = [self.place_holder, self.place_holder, self.place_holder]
        row3 = [self.place_holder, self.place_holder, self.place_holder]
        board = [
            row1,
            row2,
            row3
        ]
        return board

    def display_board(self):
        count = 0
        print('-'*25)
        for row in self.board:
            for item in row:
                if count < 2:
                    print(f'|   {item}   ',  end='')
                    count += 1
                else:
                    print(f'|   {item}   |')
                    count = 0
            print('-'*25)
    
    def get_user_pick(self):
        try:
            user_pick = int(input('Enter your choice on the grid (1-9): '))
            while user_pick < 1 or user_pick > 9:
                user_pick = int(input('Enter your choice on the grid (1-9): '))
            while user_pick in self.move_log:
                print('Invalid choice. This is already taken.')
                user_pick = int(input('Enter your choice on the grid (1-9): '))
            self.move_log.add(user_pick)
            return user_pick
        except ValueError:
            print('Invalid input. Enter a number between 1 and 9.')
            return self.get_user_pick()
    
    def get_ai_comp_pick(self):
        total_options = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        potential_picks = [pick for pick in total_options if pick not in self.move_log]

        #Pick random for first move
        if len(self.move_log) == 1 or self.allfull():
            comp_pick = random.randint(1, 9)
            while comp_pick in self.move_log:
                comp_pick = random.randint(1, 9)
            self.move_log.add(comp_pick)
            return comp_pick

        # Check if any moves will win game
        for pick1 in potential_picks:
            if self.check_pick(pick1, self.comp_char):
                return pick1
            
        # Block any winning moves for user
        for pick2 in potential_picks:
            if self.check_pick(pick2, self.user_char):
                return pick2

        #Move close to already placed pick    
        return self.move_close()
            
    def update_board(self, pick, char):
        # divmod takes two numbers. First argument is number, second is divisor. Returns tuple(quotient, remainder)
        row, col = divmod(pick - 1, 3)
        self.board[row][col] = char
    
    def again(self):
        play_again = input('Play again? Enter Y or N: ').upper()
        if play_again == 'Y':
           self.reset()
           self.run()
        elif play_again == 'N':
            print('Thanks for playing!')
        else:
            print('Invalid entry. Enter Y or N.')
            self.again()
            
    def reset(self):
        self.board = self.setup_board()
        self.game_over = False
        self.winning_char = None
        self.move_log.clear()

    def winner(self):
        row = []
        column = []
        diagonal1 = []
        diagonal2 = []
        # Check rows
        for x in range(3):
            row += self.board[x]
            match = self.matches(row)
            if match:
                self.winning_char = row[0]
                return True
            row.clear()

        # Check columns
        for col in range(3):
            for i in range(3):
                column.append(self.board[i][col])
            match = self.matches(column)
            if match:
                self.winning_char = column[0]
                return True
            column.clear()
        
        # Check diaganols
        diagonal1.extend([
            self.board[0][0],
            self.board[1][1],
            self.board[2][2]
        ])
        match = self.matches(diagonal1)
        if match:
            self.winning_char = diagonal1[0]
            return True
        diagonal2.extend([
            self.board[0][2],
            self.board[1][1],
            self.board[2][0]
        ])
        match = self.matches(diagonal2)
        if match:
            self.winning_char = diagonal2[0]
            return True
        # Check for tie
        if all(cell != self.place_holder for row in self.board for cell in row):
            return True
        return False
        
        
    def matches(self, array):
        return all(x == array[0] for x in array) and array[0] != self.place_holder
    
    def check_pick(self, pick, char):
        row, col = divmod(pick - 1, 3)
        self.board[row][col] = char
        if self.winner():
            self.board[row][col] = self.place_holder
            self.winning_char = None
            self.move_log.add(pick)
            return True
        self.board[row][col] = self.place_holder
        return False
    
    def move_close(self):
        columns = []
        diagonal1 = []
        diagonal2 = []
        counter = 0
        for row in self.board:
            if self.comp_char in row and self.user_char not in row:
                comp_char_index = self.get_char_location(row)
                if counter == 0:
                    if comp_char_index > 1:
                        options = [1, 2]
                        return random.choice(options)
                    else:
                        return 3
                if counter == 1:
                    if comp_char_index > 1:
                        options = [4, 5]
                        return random.choice(options)
                    else:
                        return 6
                if counter == 2:
                    if comp_char_index > 1:
                        options = [7, 8]
                        return random.choice(options)
                    else:
                        return 9
            counter += 1
            
        
        for rows in range(3):
            for col in range(3):
                columns.append(self.board[col][rows])
            if self.comp_char in columns and self.user_char not in columns:
                comp_char_index = self.get_char_location(columns)
                if rows == 0:
                    if comp_char_index > 1:
                        options = [1, 4]
                        return random.choice(options)
                    else:
                        return 7
                elif rows == 1:
                    if comp_char_index > 1:
                        options = [2, 5]
                        return random.choice(options)
                    else:
                        return 8
                elif rows == 2:
                    if comp_char_index > 1:
                        options = [3, 6]
                        return random.choice(options)
                    else:
                        return 9
            columns.clear()
        
        
        diagonal1.extend([
            self.board[0][0],
            self.board[1][1],
            self.board[2][2]
        ])
        if self.comp_char in diagonal1 and self.user_char not in diagonal1:
            comp_char_index = self.get_char_location(diagonal1)
            if comp_char_index > 1:
                options = [1, 5]
                return random.choice(options)
            if comp_char_index < 2:
                return 9

        diagonal2.extend([
            self.board[0][2],
            self.board[1][1],
            self.board[2][0]
        ])
        if self.comp_char in diagonal1 and self.user_char not in diagonal1:
            comp_char_index = self.get_char_location(diagonal1)
            if comp_char_index > 1:
                options = [3, 5]
                return random.choice(options)
            if comp_char_index < 2:
                return 7
                

    def get_char_location(self, array:list):
        return array.index(self.comp_char)
    
    def allfull(self):
        columns = []
        checks = 0
        for row in self.board:
            if self.user_char in row:
                checks += 1
        
        for row in range(3):
            for col in range(3):
                columns.append(self.board[col][row])
            if self.user_char in columns:
                checks += 1
            columns.clear()

        if checks == 6:
            return True




if __name__ == '__main__':
    try:
        T = TicTacToe()
        T.run()
    except Exception as e:
        print(f'An error occurred: {e}')