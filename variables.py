from re import compile

### Game Settings ###
board_size = 10
ship_count = (1,4), (2,3), (3,2) #number, length

# Characters used in the grid: [D]efault, [S]hip, [H]it and [W]ater
D, S, H, W = list('.SXw') 

# Other reused variables
columns = [ chr(n) for n in range(ord('A'), ord('A')+board_size) ]

### Regular expressions to parse user input
digit, letter = r'(\d{1,2})', f'([A-{columns[-1]}])'
shoot_regex =  compile(f'{digit}{letter}')
boot_regex = compile(f'{digit}{letter}-{digit}{letter}')
