from chess import Position


def perft(position: Position, depth: int):
    if depth == 0:
        return 1

    nodes = 0
    for move in position.move_list:
        if position.make_move(move):
            nodes += perft(position, depth - 1)
            position.undo_move()

    return nodes


position = Position("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")
max_depth = 6

for depth in range(1, max_depth + 1):
    nodes = perft(position, depth)
    print(f"{depth=}\t\t{nodes=}")
