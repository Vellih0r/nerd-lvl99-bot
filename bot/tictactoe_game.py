emj = {'o': '⭕', 'x': '❌', 'n': '⬜'}

def get_game_id():
    return 1

def get_gamefield(rows: int = 3, cols: int = 3) -> list[list[str]]:
    return [ [emj['n'] for _ in range(cols)] for _ in range(rows) ]

def gamefield_to_text(gamefield: list[list[str]]) -> str:
    str = ''
    str += '  '
    for j in range(len(gamefield[0])):
        str += f'{j} '
    str += '\n'
    for i, row in enumerate(gamefield):
        str += f'{i}'
        for cell in row:
            str += cell
        str += '\n'
    return str

def take_turn(gamefield: list[list[str]], x: int, y: int, emj_name: str) -> list[list[str]]:
    if y > len(gamefield) or x > len(gamefield[0]):
        raise IndexError('Gamefield coords are out of bounds')
    
    if emj_name not in emj:
        raise TypeError('emj_name must by "x", "o", or "n"')
    
    if gamefield[y][x] != '⬜':
        raise Exception('this cell already taken')
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
        return 3
    
def result_to_text(result: int) -> str:
    match result:
        case 3:
            return 'tie!'
        case 2:
            return 'tie!'
        case 1:
            return '❌ won!'
        case 0:
            return '⭕ won!'

def tictactoe(gamedata: dict = None, coords: str = None):
    '''gamedata - "x_turn": bool, "gamefield": list[list[str]] "result": int, "turns": int, "text": str'''
    if gamedata is None:
        gamedata = {'x_turn': True, 'gamefield': get_gamefield(), 'result': 3, 'turns': 0, 'text': ''}
        return gamedata

    if gamedata['turns'] >= 9:
        gamedata['result'] = 2
        return gamedata

    gamedata['text'] = ''
    gamedata['turns'] += 1
    
    if gamedata['x_turn']:
        e = 'x'
    else:
        e = 'o'

    try:
        coords = coords.split(',')
        x,y = coords
        x = int(x)
        y = int(y)
    except Exception as e:
        gamedata['text'] += ('Invalid coords format')
        gamedata['turns'] -= 1
        return gamedata

    try:
        gamedata['gamefield'] = take_turn(gamedata['gamefield'], x, y, e)
    except Exception as e:
        text += (f'Invalid coords or field already taken -> {e}')
        gamedata['turns'] -= 1
        return gamedata
    
    gamedata['x_turn'] = not gamedata['x_turn']
    gamedata['result'] = who_won(gamedata['gamefield'])

    gamedata['text'] += '\n'
    gamedata['text'] += (gamefield_to_text(gamedata['gamefield']))

    if gamedata['x_turn']:
        e = 'x'
    else:
        e = 'o'
    gamedata['text'] += f'Next - \n{emj[e]} turn, enter coords:'
    return gamedata

def main():
    gd = tictactoe()
    while gd['result'] == 3:
        gd = tictactoe(gd)
    print(result_to_text(gd['result']))

if __name__ == '__main__':
    main()