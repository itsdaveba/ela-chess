#define WHITE 1
#define BLACK -1

#define EMPTY 0
#define PAWN 1
#define ROOK 2
#define KNIGHT 3
#define BISHOP 4
#define QUEEN 5
#define KING 6

#define FILE_A 0

#define RANK(s) (s >> 3)
#define FILE(s) (s & 7)