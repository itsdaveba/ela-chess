#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

bool set_board(char *fen)
{
    char copy[MAX_FEN_LENGTH];

    if (strlen(fen) >= MAX_FEN_LENGTH)
    {
        printf("Error: max fen length reached\n");
        exit(1);
    }
    strcpy(copy, fen);

    char *brd = strtok(copy, " ");

    char *sd = strtok(NULL, " ");
    if (sd == NULL || !strcmp(sd, "w"))
    {
        side = WHITE;
    }
    else if (!strcmp(sd, "b"))
    {
        side = BLACK;
    }
    else
    {
        return FALSE;
    }

    char *castl = strtok(NULL, " ");
    castling = 0b0000;
    if (castl != NULL && strcmp(castl, "-"))
    {
        for (int i = 0; i < strlen(castl); i++)
        {
            if (castl[i] <= castl[i - 1])
            {
                return FALSE;
            }
            switch (castl[i])
            {
            case 'K':
                castling |= 0b1000;
                break;
            case 'Q':
                castling |= 0b0100;
                break;
            case 'k':
                castling |= 0b0010;
                break;
            case 'q':
                castling |= 0b0001;
                break;
            default:
                return FALSE;
            }
        }
    }

    char *pass = strtok(NULL, " ");
    if (pass == NULL || !strcmp(pass, "-"))
    {
        passant = -1;
    }
    else if (pass[0] >= 'a' && pass[0] <= 'h' && (pass[1] == '3' || pass[1] == '6') && pass[2] == '\0')
    {
        passant = SQUARE(pass[0], pass[1]);
    }
    else
    {
        return FALSE;
    }

    char *hf = strtok(NULL, "");
    if (hf == NULL)
    {
        halfmove = 0;
        fullmove = 1;
    }
    else if (sscanf(hf, "%d %d", &halfmove, &fullmove) < 2 || halfmove < 0 || fullmove < 1)
    {
        return FALSE;
    }

    char *row = strtok(brd, "/");
    int s = 0;
    while (row != NULL)
    {
        if (strlen(row) > 8 || FILE(bigend_rank[s]) != FILE_A)
        {
            return FALSE;
        }
        for (int c = 0; c < strlen(row); c++)
        {
            if (row[c] & '@')
            {
                if (row[c] & ' ')
                {
                    row[c] ^= ' ';
                    color[bigend_rank[s]] = BLACK;
                }
                else
                {
                    color[bigend_rank[s]] = WHITE;
                }
                switch (row[c])
                {
                case 'P':
                    piece[bigend_rank[s++]] = PAWN;
                    break;
                case 'N':
                    piece[bigend_rank[s++]] = KNIGHT;
                    break;
                case 'B':
                    piece[bigend_rank[s++]] = BISHOP;
                    break;
                case 'R':
                    piece[bigend_rank[s++]] = ROOK;
                    break;
                case 'Q':
                    piece[bigend_rank[s++]] = QUEEN;
                    break;
                case 'K':
                    piece[bigend_rank[s++]] = KING;
                    break;
                default:
                    return FALSE;
                }
            }
            else if (row[c] >= '1' && row[c] <= '8')
            {
                for (int i = 0; i < row[c] - '0'; i++)
                {
                    piece[bigend_rank[s]] = EMPTY;
                    color[bigend_rank[s++]] = EMPTY;
                }
            }
            else
            {
                return FALSE;
            }
        }
        row = strtok(NULL, "/");
    }
    if (s != 64)
    {
        return FALSE;
    }

    return TRUE;
}

char *get_fen()
{
    static char fen[MAX_FEN_LENGTH];

    int c = 0;

    for (int s = 0; s < 64; s++)
    {
        if (piece[bigend_rank[s]] == EMPTY)
        {
            int ctr;
            for (ctr = 1; FILE(bigend_rank[s]) != FILE_H && piece[bigend_rank[s + 1]] == EMPTY; ctr++)
            {
                s++;
            }
            fen[c++] = ctr + '0';
        }
        else
        {
            if (color[bigend_rank[s]] == WHITE)
            {
                fen[c++] = piece_char[piece[bigend_rank[s]]];
            }
            else
            {
                fen[c++] = piece_char[piece[bigend_rank[s]]] | ' ';
            }
        }
        if (FILE(bigend_rank[s]) == FILE_H && s != 63)
        {
            fen[c++] = '/';
        }
    }
    fen[c++] = ' ';

    if (side == WHITE)
    {
        fen[c++] = 'w';
    }
    else
    {
        fen[c++] = 'b';
    }
    fen[c++] = ' ';

    if (castling != 0)
    {
        int bit = 0b1000;
        for (int i = 0; i < 4; i++)
        {
            if (castling & bit)
            {
                fen[c++] = castling_char[i];
            }
            bit >>= 1;
        }
    }
    else
    {
        fen[c++] = '-';
    }
    fen[c++] = ' ';

    if (passant != -1)
    {
        fen[c++] = FILE(passant) + 'a';
        fen[c++] = RANK(passant) + '1';
    }
    else
    {
        fen[c++] = '-';
    }
    fen[c++] = ' ';

    sprintf(fen + c, "%d %d", halfmove, fullmove);

    if (strlen(fen) >= MAX_FEN_LENGTH)
    {
        printf("Error: max fen length reached\n");
        exit(1);
    }

    return fen;
}

void print_board()
{
    char *fen = get_fen();

    printf("\n%s\n", fen);
    printf("\n  A B C D E F G H");
    for (int s = 0; s < 64; s++)
    {
        if (FILE(bigend_rank[s]) == FILE_A)
        {
            printf("\n%d", RANK(bigend_rank[s]) + 1);
        }
        if (color[bigend_rank[s]] == BLACK)
        {
            printf(" %c", piece_char[piece[bigend_rank[s]]] | ' ');
        }
        else
        {
            printf(" %c", piece_char[piece[bigend_rank[s]]]);
        }
    }
    printf("\n\n");
}

void add_move(int from, int to, int type, int *n_moves, gen_t *move_list)
{
    if (*n_moves >= MAX_GEN_MOVES)
    {
        printf("Error: max gen moves reached\n");
        exit(1);
    }
    gen_t *gen_p = &move_list[*n_moves];

    if (type & PROMOTION)
    {
        for (int prom = KNIGHT; prom <= QUEEN; prom++)
        {
            (*n_moves)++;
            gen_p->move.bytes.from = from;
            gen_p->move.bytes.to = to;
            gen_p->move.bytes.prom = prom;
            gen_p->move.bytes.type = type;
            gen_p++->score = __INT_MAX__ - piece_value[QUEEN] - piece_value[PAWN] + piece_value[prom];
        }
    }
    else
    {
        (*n_moves)++;
        gen_p->move.bytes.from = from;
        gen_p->move.bytes.to = to;
        gen_p->move.bytes.prom = EMPTY;
        gen_p->move.bytes.type = type;
        if (type & CAPTURE)
        {
            gen_p->score = see_capture(gen_p->move);
            if (gen_p->score > -piece_value[PAWN])
            {
                gen_p->score += __INT_MAX__ - piece_value[QUEEN] - piece_value[PAWN];
            }
        }
        else
        {
            gen_p->score = heuristic[from][to];
        }
    }
}

int gen_moves(gen_t *move_list, bool quiesce)
{
    int type;
    int n_moves = 0;

    for (int s = 0; s < 64; s++)
    {
        if (color[s] == side)
        {
            if (piece[s] == PAWN)
            {
                type = PAWN_MOVE;
                if (side == WHITE)
                {
                    if (piece[s + UP] == EMPTY && !quiesce)
                    {
                        if (RANK(s) == RANK_7)
                        {
                            add_move(s, s + UP, type | PROMOTION, &n_moves, move_list);
                        }
                        else
                        {
                            add_move(s, s + UP, type, &n_moves, move_list);
                        }
                        if (RANK(s) == RANK_2 && piece[s + DOUBLE_UP] == EMPTY)
                        {
                            add_move(s, s + DOUBLE_UP, type | PAWN_DOUBLE_MOVE, &n_moves, move_list);
                        }
                    }
                    type |= CAPTURE;
                    if (FILE(s) != FILE_A && color[s + UP_LEFT] == BLACK)
                    {
                        if (RANK(s) == RANK_7)
                        {
                            add_move(s, s + UP_LEFT, type | PROMOTION, &n_moves, move_list);
                        }
                        else
                        {
                            add_move(s, s + UP_LEFT, type, &n_moves, move_list);
                        }
                    }
                    if (FILE(s) != FILE_H && color[s + UP_RIGHT] == BLACK)
                    {
                        if (RANK(s) == RANK_7)
                        {
                            add_move(s, s + UP_RIGHT, type | PROMOTION, &n_moves, move_list);
                        }
                        else
                        {
                            add_move(s, s + UP_RIGHT, type, &n_moves, move_list);
                        }
                    }
                }
                else
                {
                    if (piece[s + DOWN] == EMPTY && !quiesce)
                    {
                        if (RANK(s) == RANK_2)
                        {
                            add_move(s, s + DOWN, type | PROMOTION, &n_moves, move_list);
                        }
                        else
                        {
                            add_move(s, s + DOWN, type, &n_moves, move_list);
                        }
                        if (RANK(s) == RANK_7 && piece[s + DOUBLE_DOWN] == EMPTY)
                        {
                            add_move(s, s + DOUBLE_DOWN, type | PAWN_DOUBLE_MOVE, &n_moves, move_list);
                        }
                    }
                    type |= CAPTURE;
                    if (FILE(s) != FILE_A && color[s + DOWN_LEFT] == WHITE)
                    {
                        if (RANK(s) == RANK_2)
                        {
                            add_move(s, s + DOWN_LEFT, type | PROMOTION, &n_moves, move_list);
                        }
                        else
                        {
                            add_move(s, s + DOWN_LEFT, type, &n_moves, move_list);
                        }
                    }
                    if (FILE(s) != FILE_H && color[s + DOWN_RIGHT] == WHITE)
                    {
                        if (RANK(s) == RANK_2)
                        {
                            add_move(s, s + DOWN_RIGHT, type | PROMOTION, &n_moves, move_list);
                        }
                        else
                        {
                            add_move(s, s + DOWN_RIGHT, type, &n_moves, move_list);
                        }
                    }
                }
            }
            else
            {
                for (int d = 0; d < n_directions[piece[s]]; d++)
                {
                    for (int n = s;;)
                    {
                        n = mailbox[mailbox64[n] + direction[piece[s]][d]];
                        if (n == -1)
                        {
                            break;
                        }
                        if (color[n] != EMPTY)
                        {
                            if (color[n] == (side ^ 1))
                            {
                                add_move(s, n, CAPTURE, &n_moves, move_list);
                            }
                            break;
                        }
                        if (!quiesce)
                        {
                            add_move(s, n, 0, &n_moves, move_list);
                        }
                        if (!slider[piece[s]])
                        {
                            break;
                        }
                    }
                }
            }
        }
    }

    if (castling != 0 && !quiesce)
    {
        if (side == WHITE)
        {
            if (attacker(E1, BLACK, 0) == -1)
            {
                if (castling & 0b1000)
                {
                    if (piece[F1] == EMPTY && piece[G1] == EMPTY && attacker(F1, BLACK, 0) == -1)
                    {
                        add_move(E1, G1, CASTLE, &n_moves, move_list);
                    }
                }
                if (castling & 0b0100)
                {
                    if (piece[D1] == EMPTY && piece[C1] == EMPTY && piece[B1] == EMPTY && attacker(D1, BLACK, 0) == -1)
                    {
                        add_move(E1, C1, CASTLE, &n_moves, move_list);
                    }
                }
            }
        }
        else
        {
            if (attacker(E8, WHITE, 0) == -1)
            {
                if (castling & 0b0010)
                {
                    if (piece[F8] == EMPTY && piece[G8] == EMPTY && attacker(F8, WHITE, 0) == -1)
                    {
                        add_move(E8, G8, CASTLE, &n_moves, move_list);
                    }
                }
                if (castling & 0b0001)
                {
                    if (piece[D8] == EMPTY && piece[C8] == EMPTY && piece[B8] == EMPTY && attacker(D8, WHITE, 0) == -1)
                    {
                        add_move(E8, C8, CASTLE, &n_moves, move_list);
                    }
                }
            }
        }
    }

    if (passant != -1)
    {
        type = PAWN_MOVE | CAPTURE | EP_CAPTURE;
        if (side == WHITE)
        {
            if (FILE(passant) != FILE_A && piece[passant + DOWN_LEFT] == PAWN && color[passant + DOWN_LEFT] == WHITE)
            {
                add_move(passant + DOWN_LEFT, passant, type, &n_moves, move_list);
            }
            if (FILE(passant) != FILE_H && piece[passant + DOWN_RIGHT] == PAWN && color[passant + DOWN_RIGHT] == WHITE)
            {
                add_move(passant + DOWN_RIGHT, passant, type, &n_moves, move_list);
            }
        }
        else
        {
            if (FILE(passant) != FILE_A && piece[passant + UP_LEFT] == PAWN && color[passant + UP_LEFT] == BLACK)
            {
                add_move(passant + UP_LEFT, passant, type, &n_moves, move_list);
            }
            if (FILE(passant) != FILE_H && piece[passant + UP_RIGHT] == PAWN && color[passant + UP_RIGHT] == BLACK)
            {
                add_move(passant + UP_RIGHT, passant, type, &n_moves, move_list);
            }
        }
    }

    return n_moves;
}

move_t gen_capture(int from, int to, int prom)
{
    move_t move;

    move.bytes.from = from;
    move.bytes.to = to;
    move.bytes.prom = EMPTY;
    move.bytes.type = CAPTURE;

    if (piece[from] == PAWN)
    {
        move.bytes.type |= PAWN_MOVE;
        if ((side == WHITE && RANK(from) == RANK_7) || (side == BLACK && RANK(from) == RANK_2))
        {
            move.bytes.prom = prom;
            move.bytes.type |= PROMOTION;
        }
    }

    if (passant == to)
    {
        move.bytes.type |= EP_CAPTURE;
    }

    return move;
}

int attacker(int square, int side, int skip)
{
    if (side == WHITE && RANK(square) > RANK_2)
    {
        if (FILE(square) != FILE_A && piece[square + DOWN_LEFT] == PAWN && color[square + DOWN_LEFT] == WHITE)
        {
            if (skip-- <= 0)
            {
                return square + DOWN_LEFT;
            }
        }
        if (FILE(square) != FILE_H && piece[square + DOWN_RIGHT] == PAWN && color[square + DOWN_RIGHT] == WHITE)
        {
            if (skip-- <= 0)
            {
                return square + DOWN_RIGHT;
            }
        }
    }
    else if (side == BLACK && RANK(square) < RANK_7)
    {
        if (FILE(square) != FILE_A && piece[square + UP_LEFT] == PAWN && color[square + UP_LEFT] == BLACK)
        {
            if (skip-- <= 0)
            {
                return square + UP_LEFT;
            }
        }
        if (FILE(square) != FILE_H && piece[square + UP_RIGHT] == PAWN && color[square + UP_RIGHT] == BLACK)
        {
            if (skip-- <= 0)
            {
                return square + UP_RIGHT;
            }
        }
    }

    for (int p = KNIGHT; p <= KING; p++)
    {
        for (int d = 0; d < n_directions[p]; d++)
        {
            for (int n = square;;)
            {
                n = mailbox[mailbox64[n] + direction[p][d]];
                if (n == -1)
                {
                    break;
                }
                if (piece[n] == p && color[n] == side)
                {
                    if (skip-- <= 0)
                    {
                        return n;
                    }
                }
                if (color[n] != EMPTY || !slider[p])
                {
                    break;
                }
            }
        }
    }

    return -1;
}

bool in_check(int side)
{
    for (int s = 0; s < 64; s++)
    {
        if (piece[s] == KING && color[s] == side)
        {
            if (attacker(s, side ^ 1, 0) != -1)
            {
                return TRUE;
            }
            break;
        }
    }

    return FALSE;
}

bool make_move(move_t move)
{
    if (hply >= MAX_HPLY)
    {
        printf("Error: max history ply reached\n");
        exit(1);
    }
    history[hply].move = move;
    history[hply].castling = castling;
    history[hply].passant = passant;
    history[hply].halfmove = halfmove;
    history[hply].capture = piece[move.bytes.to];
    history[hply++].hash = hash;
    ply++;

    if (passant != -1)
    {
        if (side == WHITE)
        {
            if ((FILE(passant) != FILE_A && piece[passant + DOWN_LEFT] == PAWN && color[passant + DOWN_LEFT] == WHITE) ||
                (FILE(passant) != FILE_H && piece[passant + DOWN_RIGHT] == PAWN && color[passant + DOWN_RIGHT] == WHITE))
            {
                hash ^= hash_table[FILE(passant)][PAWN][WHITE];
            }
        }
        else
        {
            if ((FILE(passant) != FILE_A && piece[passant + UP_LEFT] == PAWN && color[passant + UP_LEFT] == BLACK) ||
                (FILE(passant) != FILE_H && piece[passant + UP_RIGHT] == PAWN && color[passant + UP_RIGHT] == BLACK))
            {
                hash ^= hash_table[FILE(passant)][PAWN][WHITE];
            }
        }
    }

    if (piece[move.bytes.to] != EMPTY)
    {
        hash ^= hash_table[move.bytes.to][piece[move.bytes.to]][side ^ 1];
    }

    if (move.bytes.type & PROMOTION)
    {
        hash ^= hash_table[move.bytes.to][move.bytes.prom][side];
        piece[move.bytes.to] = move.bytes.prom;
    }
    else
    {
        hash ^= hash_table[move.bytes.to][piece[move.bytes.from]][side];
        piece[move.bytes.to] = piece[move.bytes.from];
    }
    hash ^= hash_table[move.bytes.from][piece[move.bytes.from]][side];
    color[move.bytes.to] = side;
    piece[move.bytes.from] = EMPTY;
    color[move.bytes.from] = EMPTY;

    if (castling != 0)
    {
        hash ^= hash_table[(castling + A8) & H8][PAWN][BLACK];
        castling &= castling_rights[move.bytes.from] & castling_rights[move.bytes.to];
        hash ^= hash_table[(castling + A8) & H8][PAWN][BLACK];
    }

    if (move.bytes.type & PAWN_DOUBLE_MOVE)
    {
        if ((FILE(move.bytes.to) != FILE_A && piece[move.bytes.to + LEFT] == PAWN && color[move.bytes.to + LEFT] == (side ^ 1)) ||
            (FILE(move.bytes.to) != FILE_H && piece[move.bytes.to + RIGHT] == PAWN && color[move.bytes.to + RIGHT] == (side ^ 1)))
        {
            hash ^= hash_table[FILE(move.bytes.to)][PAWN][WHITE];
        }
        if (side == WHITE)
        {
            passant = move.bytes.to + DOWN;
        }
        else
        {
            passant = move.bytes.to + UP;
        }
    }
    else if (passant != -1)
    {
        passant = -1;
    }

    if (move.bytes.type & (PAWN_MOVE | CAPTURE))
    {
        halfmove = 0;
    }
    else
    {
        halfmove++;
    }

    if (side == BLACK)
    {
        fullmove++;
    }

    if (move.bytes.type & CASTLE)
    {
        int from, to;
        switch (move.bytes.to)
        {
        case G1:
            from = H1;
            to = F1;
            break;
        case C1:
            from = A1;
            to = D1;
            break;
        case G8:
            from = H8;
            to = F8;
            break;
        case C8:
            from = A8;
            to = D8;
            break;
        }
        hash ^= hash_table[to][ROOK][side];
        piece[to] = ROOK;
        color[to] = side;
        hash ^= hash_table[from][ROOK][side];
        piece[from] = EMPTY;
        color[from] = EMPTY;
    }

    if (move.bytes.type & EP_CAPTURE)
    {
        if (side == WHITE)
        {
            hash ^= hash_table[move.bytes.to + DOWN][PAWN][BLACK];
            piece[move.bytes.to + DOWN] = EMPTY;
            color[move.bytes.to + DOWN] = EMPTY;
        }
        else
        {
            hash ^= hash_table[move.bytes.to + UP][PAWN][WHITE];
            piece[move.bytes.to + UP] = EMPTY;
            color[move.bytes.to + UP] = EMPTY;
        }
    }

    hash ^= hash_table[A8][PAWN][WHITE];
    side = side ^ 1;

    if (in_check(side ^ 1))
    {
        take_back();
        return FALSE;
    }

    return TRUE;
}

void take_back()
{
    hist_t hist = history[--hply];
    --ply;

    side = side ^ 1;

    castling = hist.castling;
    passant = hist.passant;
    halfmove = hist.halfmove;
    hash = hist.hash;

    if (side == BLACK)
    {
        fullmove--;
    }

    if (hist.move.bytes.type & PROMOTION)
    {
        piece[hist.move.bytes.from] = PAWN;
    }
    else
    {
        piece[hist.move.bytes.from] = piece[hist.move.bytes.to];
    }
    color[hist.move.bytes.from] = side;
    if (hist.capture == EMPTY)
    {
        piece[hist.move.bytes.to] = EMPTY;
        color[hist.move.bytes.to] = EMPTY;
    }
    else
    {
        piece[hist.move.bytes.to] = hist.capture;
        color[hist.move.bytes.to] = side ^ 1;
    }

    if (hist.move.bytes.type & CASTLE)
    {
        int from, to;
        switch (hist.move.bytes.to)
        {
        case G1:
            from = H1;
            to = F1;
            break;
        case C1:
            from = A1;
            to = D1;
            break;
        case G8:
            from = H8;
            to = F8;
            break;
        case C8:
            from = A8;
            to = D8;
            break;
        }
        piece[from] = ROOK;
        color[from] = side;
        piece[to] = EMPTY;
        color[to] = EMPTY;
    }

    if (hist.move.bytes.type & EP_CAPTURE)
    {
        if (side == WHITE)
        {
            piece[hist.move.bytes.to + DOWN] = PAWN;
            color[hist.move.bytes.to + DOWN] = BLACK;
        }
        else
        {
            piece[hist.move.bytes.to + UP] = PAWN;
            color[hist.move.bytes.to + UP] = WHITE;
        }
    }
}

int repetition()
{
    int rep = 1;

    for (int h = hply - halfmove; h < hply; h++)
    {
        if (history[h].hash == hash)
        {
            rep++;
        }
    }

    return rep;
}

u64 perft(int depth)
{
    u64 nodes;
    int n_moves;
    gen_t move_list[MAX_GEN_MOVES];

    if (depth == 0)
    {
        return 1ULL;
    }

    nodes = 0;
    n_moves = gen_moves(move_list, FALSE);

    for (int m = 0; m < n_moves; m++)
    {
        if (make_move(move_list[m].move))
        {
            nodes += perft(depth - 1);
            take_back();
        }
    }

    return nodes;
}