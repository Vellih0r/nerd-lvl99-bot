emj = {'o': '⭕', 'x': '❌', 'n': '⬜'}

def get_gamefield(rows: int = 3, cols: int = 3) -> list[list[str]]:
    return [ [emj['n'] for _ in range(cols)] for _ in range(rows) ]

def gamefield_to_text(gamefield: list[list[str]]) -> str:
    str = ''
    for row in gamefield:
        for cell in row:
            str += cell
        str += '\n'
    return str

def take_turn(gamefield: list[list[str]], x: int, y: int, emj_name: str) -> list[list[str]]:
    if y > len(gamefield) or x > len(gamefield[0]):
        raise IndexError('Gamefield coords are out of bounds')
    
    if emj_name not in emj:
        raise TypeError('emj_name must by "x", "o", or "n"')
    
    gamefield[y][x] = emj[emj_name]
    return gamefield

def who_won(gamefield: list[list[str]]) -> int:
    row_streak = ''
    col_streak = [ True for _ in range(len(gamefield[0])) ]
    diagonal_streak = True
    back_diagonal_streak = True
    winner = {'⭕': False, '❌': False}
    for i, row in enumerate(gamefield):
        for j, cell in enumerate(row):
            # if cell == emj['n']:
            #     continue
            
            if j == 0:
                row_streak = True
            elif gamefield[i][0] != cell:
                row_streak = False

            if gamefield[0][j] != cell:
                col_streak[j] = False

            if i == len(gamefield)-1 and col_streak[j]:
                winner[cell] = True

            if i == j:
                if gamefield[0][0] != cell:
                    diagonal_streak = False
            if len(row)-i-1 == j:
                if gamefield[0][len(row)-1] != cell:
                    back_diagonal_streak = False


        if row_streak:
            winner[row_streak] = True

        if i == len(gamefield)-1:
            if diagonal_streak:
                winner[gamefield[0][0]] = True
            if back_diagonal_streak:
                winner[gamefield[0][len(row)-1]] = True
    
    if winner['❌'] and winner['⭕']:
        return 2
    elif winner['❌']:
        return 1
    elif winner['⭕']:
        return 0
    else:
        return 2
    
def result_to_text(result: int) -> str:
    match result:
        case 2:
            return 'tie!'
        case 1:
            return 'x won!'
        case 0:
            return 'o won!'

def tic_tac_toe():
    gf = get_gamefield()
    gf = take_turn(gf, 2, 0, 'x')
    gf = take_turn(gf, 1, 1, 'x')
    gf = take_turn(gf, 0, 2, 'x')
    print(gamefield_to_text(gf))
    result = who_won(gf)
    print(result_to_text(result))


tic_tac_toe()