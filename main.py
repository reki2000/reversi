

DIRECTIONS = [
    (-1, -1),   (-1, 0),   (-1, 1),
    (0, -1),   (0, 1),
    (1, -1),   (1, 0),   (1, 1)
]

EMPTY, WHITE, BLACK = 0, 1, 2

# board[y][x] = EMPTY(empty), 1(white), 2(black)
board = [[EMPTY] * 8 for _ in range(0, 8)]


def get_piece_char(c):
    if c == WHITE:
        return "x"
    elif c == BLACK:
        return "o"
    else:
        return " "


def build_board(b):
    line = " |1|2|3|4|5|6|7|8|\n"
    for y in range(1, 9):
        line += f"{y}|"
        for x in range(1, 9):
            line += f"{get_piece_char(get_piece(x,y))}|"
        line += "\n"
    return line


def set_piece(x, y, c):
    board[y-1][x-1] = c


def get_piece(x, y):
    return board[y-1][x-1]


def valid(x, y):
    return x > 0 and x <= 8 and y > 0 and y <= 8


def length(x, y, d, c):
    """ search from x,y to direction d where c continues and the end is enemy(c)"""
    l = 0
    dy, dx = d
    x, y = x + dx, y + dy
    while valid(x, y) and get_piece(x, y) == c:
        x, y = x + dx, y + dy
        l += 1

    if not valid(x, y):
        return 0
    if get_piece(x, y) != enemy(c):
        return 0

    return l


def explore(c):
    """explore board to find puttable points against c"""
    result = []
    for x in range(1, 9):
        for y in range(1, 9):
            if get_piece(x, y) != EMPTY:
                continue

            l = [0] * 8
            found = False
            for i, d in enumerate(DIRECTIONS):
                l[i] = length(x, y, d, c)
                if l[i] > 0:
                    found = True

            if found:
                result += [(x, y, l)]

    return result


def choose_hand(c):
    """find puttable position which has the longest reversibles"""
    max_put = (0, 0, 0)
    for hand in explore(enemy(c)):
        for l in hand[2]:
            if max_put[2] < l:
                max_put = (hand[0], hand[1], l)
    return max_put


def enemy(c):
    assert c == WHITE or c == BLACK
    if c == WHITE:
        return BLACK
    else:
        return WHITE


def reverse(x, y, turn):
    for d in DIRECTIONS:
        l = length(x, y, d, enemy(turn))
        xx, yy = x, y
        for _ in range(0, l):
            xx += d[1]
            yy += d[0]
            set_piece(xx, yy, turn)


def count(board):
    cnt = {}
    for row in board:
        for c in row:
            if c not in cnt:
                cnt[c] = 0
            cnt[c] += 1
    return cnt


if __name__ == "__main__":
    set_piece(4, 4, 2)
    set_piece(5, 5, 2)
    set_piece(4, 5, 1)
    set_piece(5, 4, 1)

    turn = WHITE  # the first turn starts with BLACK
    passed = False

    while True:
        turn = enemy(turn)
        print(build_board(board), end="")
        print(f"turn: {get_piece_char(turn)}")

        if turn == WHITE:
            hand = choose_hand(turn)
        else:
            while True:
                print("input x y: ", end="")
                x, y = map(int, input().split())
                ok = False
                for _, d in enumerate(DIRECTIONS):
                    l = length(x, y, d, enemy(turn))
                    if l > 0:
                        hand = (x, y, l)
                        ok = True
                        break
                if ok:
                    break
                print(f"cannot put on {x} {y}")

        if hand[2] == 0:
            print("pass")
            if passed:
                print("game end")
                break

            passed = True
            continue

        passed = False
        x, y = hand[0], hand[1]
        set_piece(x, y, turn)
        reverse(x, y, turn)

    cnt = count(board)
    print(
        f"{get_piece_char(WHITE)}:{cnt[WHITE]} {get_piece_char(BLACK)}:{cnt[BLACK]}")
