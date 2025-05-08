from time import sleep
from numpy import full
from numpy.random import choice, randint, seed
from variables import board_size, D, S, H, W, columns, shoot_regex, boot_regex

class Player:
    
    def __init__(self, ship_count):
        self.ship_count = ship_count
        self.board = self.create_board()
        self.populate_board()
    
    def __repr__(self):
        return '\n'.join(
            [f'Player: {self.name}'] +
            [ ' '.join(l) for l in self.board ] + ['']
        )
    
    def create_board(self):
        return full((board_size, board_size), D)
    
    def pretty_board(self, title, board):
        line_length = board_size*2 + 2
        lines = [title.center(line_length)] + [' '.join(
            ['  '] + columns )]
        lines += [ ' '.join(
            [f'{i+1:>2}']+list(l)) for i,l in enumerate(board) ]
        
        return lines

    def full_disclosure_board(self):
        return self.pretty_board('Your board:', self.board)

    def guess_board(self):
        kk = self.board.copy()
        kk[kk == S] = D
        return self.pretty_board('Opponent:', kk)
    
    def place_ship(self, ship):
        if (self.board[max(ship[0][0]-1, 0):ship[0][1]+1,
                       max(ship[1][0]-1, 0):ship[1][1]+1] != D).any():
            
            if isinstance(self, HumanPlayer):
                print('Please choose a new ship positon, leaving at least one square between previously placed ships.')
            return False

        self.board[ship[0][0]:ship[0][1],
                   ship[1][0]:ship[1][1]] = S
        
        return True

    def _populate_board(self):
        for number, size in self.ship_count:
            for kk in range(number):
                
                placed = False
                while not placed:
                    ship = self.create_ship(size)
                    placed = self.place_ship(ship)
                
                if isinstance(self, HumanPlayer):
                    print('\n'.join(['']+self.full_disclosure_board()))

    def check_fire(self, square):
        hit = self.board[square] == S
        self.board[square] = H if hit else W
        return hit


class MachinePlayer(Player):
    
    def __init__(self, ship_count):
        Player.__init__(self, ship_count)
        self.name = 'Computer'

    def populate_board(self):
        self._populate_board()
    
    def create_ship(self, size):
        vertical = choice([True, False])
        ship = [
            [randint(
                board_size - (size if vertical else 0)
            )],
            [randint(
                board_size - (0 if vertical else size)
            )]
        ]

        if vertical:
            ship[0] += [ship[0][0]+size]
            ship[1] += [ship[1][0]+1]
        else:
            ship[0] += [ship[0][0]+1]
            ship[1] += [ship[1][0]+size]
    
        return ship

    def choose_target(self):
        return (randint(board_size),
                randint(board_size))


class HumanPlayer(Player):

    def __init__(self, name, ship_count):
        Player.__init__(self, ship_count)
        self.name = name

    def populate_board(self):
        print('\n'.join( self.full_disclosure_board() ), end='\n\n')
        print('Using the row numbers and column letters, tell me',
              'where you want to place each of your ships.\n'
              'For intance, to place a ship of size 4 horizontaly',
              'on the top left corner, type: 1A-1D\n')

        self._populate_board()
    
    def create_ship(self, size):
        while True:
            ans = input(f'Ship of size {size}: ')
            m = boot_regex.match(ans)
            if not m:
                print('Please use the required format. Ex: 1A-4A')
                continue
            
            r1,c1,r2,c2 = m.groups()
            r1, r2 = int(r1)-1, int(r2)-1
            c1, c2 = columns.index(c1), columns.index(c2)
            if not (0<=r1<=9 and 0<=r2<=9):
                print('Please choose a row between 1 and 10.')
                continue
            if not (c1==c2) != (r1==r2):
                print('Your ship must have size > 1 and be placed horizontally or vertically')
                continue
            
            r1, r2 = sorted([r1, r2])
            c1, c2 = sorted([c1, c2])
            r2 += 1
            c2 += 1

            if not ((c2-c1)==size or (r2-r1)==size):
                print(f'This ship should have size {size}.')
                continue

            return [[r1,r2], [c1,c2]]
    
    def choose_target(self):
        while True:
            ans = input('Where would you like to shoot?\n'+
                        '(Provide the row number and the column letter. Ex: 1A): ')
            m = shoot_regex.match(ans)
            if not m:
                print('Please use the required format. Ex: 10B')
                continue

            r, c = m.groups()
            r = int(r)-1
            c = columns.index(c)
            if not 0<=r<=9:
                print('Please choose a row between 1 and 10.')
                continue

            return (r, c)


class Battleship:
    
    def __init__(self, short_demo, apagon, ship_count):
        self.short_demo = short_demo
        self.apagon = apagon
        self.ship_count = ship_count
        
        self.print_header()
        self.set_players()
        self.choose_first_player()
        self.print_boards()
        self.run_game()

    def print_header(self):
        sleep(2)
        title = '# # #  THE AMAZING BATTLESHIP GAME  # # #'
        l = len(title)
        h_border = '# '*((len(title)+1)//2)
        v_border = '# # #'+' '*(l-10)+'# # #'
        print('', h_border, v_border,
              title,
              v_border, h_border, '', sep='\n' )
    
        if self.short_demo or self.apagon:
            print('# # NOTE: You are in demo mode. # #\n'.center(l))
            seed(6)

        print('\tLoading', end=' ')
        for kk in range(6):
            sleep(2)
            print('.', end=' ')
        print('\r'+' '*18+'DONE!'+' '*18+'\n\n')
        sleep(1)
        
    def set_players(self):
        self.computer = MachinePlayer(self.ship_count)

        if self.apagon:
            self.human = MachinePlayer(self.ship_count)
            self.human.name = 'Fake Human'
        else:
            name = input('What should I call you? ')
            print(f'\n\tHi {name}!\n')
            self.human = HumanPlayer(name, self.ship_count)

    def choose_first_player(self):
        if self.apagon:
            self.human_first = choice([True, False])
        else:
            ans = input(f'\n{self.human.name} would you like to go first? [y/n]: ')
            self.human_first = ans in 'yY1'
            if not self.human_first:
                print(self.computer.name +
                      ', will go first since you did not type "y".\n')
            else:
                print()

    def print_boards(self):
        player = self.human.full_disclosure_board()
        other = self.computer.guess_board()

        for pair in zip(player, other):
            print('    '.join(pair))
        print()

    def run_game(self):
        player, opponent = (
            self.human, self.computer
        ) if self.human_first else (
            self.computer, self.human
        )
        game_over = False
        while not game_over:
            while True:
                
                target = player.choose_target()
                if opponent.board[target] in (H,W):
                    continue
                
                hit = opponent.check_fire(target)
                if not self.apagon and isinstance(player, MachinePlayer):
                    sleep(1)
                print(f'\n{player.name} shot at {target[0]+1}{columns[target[1]]}: {"HIT" if hit else "Miss"}')
                self.print_boards()
                
                if not hit:
                    player, opponent = opponent, player
                    break
                if (opponent.board == S).sum() < 1:
                    if isinstance(player, HumanPlayer):
                        print(f'\tCongratulations {player.name}! You won!')
                    else:
                        print(f'\tSorry {player.name}, {opponent.name} won this time.')
                    game_over = True
                    break
