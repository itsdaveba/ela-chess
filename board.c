#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

bool set_board(char *fen)
{
    char copy[MAX_FEN_LENGTH];
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
        if (strlen(row) > 8 || FILE(board[s]) != FILE_A)
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
                    color[board[s]] = BLACK;
                }
                else
                {
                    color[board[s]] = WHITE;
                }
                switch (row[c])
                {
                case 'P':
                    piece[board[s++]] = PAWN;
                    break;
                case 'R':
                    piece[board[s++]] = ROOK;
                    break;
                case 'N':
                    piece[board[s++]] = KNIGHT;
                    break;
                case 'B':
                    piece[board[s++]] = BISHOP;
                    break;
                case 'Q':
                    piece[board[s++]] = QUEEN;
                    break;
                case 'K':
                    piece[board[s++]] = KING;
                    break;
                default:
                    return FALSE;
                }
            }
            else if (row[c] >= '1' && row[c] <= '8')
            {
                for (int i = 0; i < row[c] - '0'; i++)
                {
                    piece[board[s]] = EMPTY;
                    color[board[s++]] = EMPTY;
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

    int ctr;
    int c = 0;

    for (int s = 0; s < 64; s++)
    {
        if (piece[board[s]] == EMPTY)
        {
            for (ctr = 1; FILE(board[s]) != FILE_H && piece[board[s + 1]] == EMPTY; ctr++)
            {
                s++;
            }
            fen[c++] = ctr + '0';
        }
        else
        {
            if (color[board[s]] == WHITE)
            {
                fen[c++] = piece_to_char[piece[board[s]]];
            }
            else
            {
                fen[c++] = piece_to_char[piece[board[s]]] | ' ';
            }
        }
        if (FILE(board[s]) == FILE_H && s != 63)
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

    return fen;
}

void print_board()
{
    char *fen = get_fen();

    printf("\n%s\n", fen);
    printf("\n  A B C D E F G H");
    for (int s = 0; s < 64; s++)
    {
        if (FILE(board[s]) == FILE_A)
        {
            printf("\n%d", RANK(board[s]) + 1);
        }
        if (color[board[s]] == BLACK)
        {
            printf(" %c", piece_to_char[piece[board[s]]] | ' ');
        }
        else
        {
            printf(" %c", piece_to_char[piece[board[s]]]);
        }
    }
    printf("\n\n");
}

void add_move(int from, int to, int type)
{
    move_t *move_p = &move_list[n_moves];

    if (type & PROMOTION)
    {
        for (int prom = ROOK; prom <= QUEEN; prom++)
        {
            n_moves++;
            move_p->from = from;
            move_p->to = to;
            move_p->prom = prom;
            move_p->type = type;
        }
    }
    n_moves++;
    move_p->from = from;
    move_p->to = to;
    move_p->prom = EMPTY;
    move_p->type = type;
}

void gen_moves()
{
    int type;

    n_moves = 0;

    for (int s = 0; s < 64; s++)
    {
        if (color[s] == side)
        {
            if (piece[s] == PAWN)
            {
                type = PAWN_MOVE;
                if (side == WHITE)
                {
                    if (piece[s + UP] == EMPTY)
                    {
                        if (RANK(s) == RANK_7)
                        {
                            add_move(s, s + UP, type | PROMOTION);
                        }
                        else
                        {
                            add_move(s, s + UP, type);
                        }
                        if (RANK(s) == RANK_2 && piece[s + DOUBLE_UP] == EMPTY)
                        {
                            add_move(s, s + DOUBLE_UP, type | PAWN_DOUBLE_MOVE);
                        }
                    }
                    type |= CAPTURE;
                    if (FILE(s) != FILE_A && color[s + UP_LEFT] == BLACK)
                    {
                        if (RANK(s) == RANK_7)
                        {
                            add_move(s, s + UP_LEFT, type | PROMOTION);
                        }
                        else
                        {
                            add_move(s, s + UP_LEFT, type);
                        }
                    }
                    if (FILE(s) != FILE_H && color[s + UP_RIGHT] == BLACK)
                    {
                        if (RANK(s) == RANK_7)
                        {
                            add_move(s, s + UP_RIGHT, type | PROMOTION);
                        }
                        else
                        {
                            add_move(s, s + UP_RIGHT, type);
                        }
                    }
                }
                else
                {
                    if (piece[s + DOWN] == EMPTY)
                    {
                        if (RANK(s) == RANK_2)
                        {
                            add_move(s, s + DOWN, type | PROMOTION);
                        }
                        else
                        {
                            add_move(s, s + DOWN, type);
                        }
                        if (RANK(s) == RANK_7 && piece[s + DOUBLE_DOWN] == EMPTY)
                        {
                            add_move(s, s + DOUBLE_DOWN, type | PAWN_DOUBLE_MOVE);
                        }
                    }
                    type |= CAPTURE;
                    if (FILE(s) != FILE_A && color[s + DOWN_LEFT] == WHITE)
                    {
                        if (RANK(s) == RANK_2)
                        {
                            add_move(s, s + DOWN_LEFT, type | PROMOTION);
                        }
                        else
                        {
                            add_move(s, s + DOWN_LEFT, type);
                        }
                    }
                    if (FILE(s) != FILE_H && color[s + DOWN_RIGHT] == WHITE)
                    {
                        if (RANK(s) == RANK_2)
                        {
                            add_move(s, s + DOWN_RIGHT, type | PROMOTION);
                        }
                        else
                        {
                            add_move(s, s + DOWN_RIGHT, type);
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
                            if (color[n] == -side)
                            {
                                add_move(s, n, CAPTURE);
                            }
                            break;
                        }
                        add_move(s, n, 0);
                        if (!slider[piece[s]])
                        {
                            break;
                        }
                    }
                }
            }
        }
    }

    if (castling != 0)
    {
        if (side == WHITE)
        {
            if ((castling & 0b1000) && piece[F1] == EMPTY && piece[G1] == EMPTY)
            {
                add_move(E1, G1, CASTLE);
            }
            if ((castling & 0b0100) && piece[D1] == EMPTY && piece[C1] == EMPTY && piece[B1] == EMPTY)
            {
                add_move(E1, C1, CASTLE);
            }
        }
        else
        {
            if ((castling & 0b0010) && piece[F8] == EMPTY && piece[G8] == EMPTY)
            {
                add_move(E8, G8, CASTLE);
            }
            if ((castling & 0b0001) && piece[D8] == EMPTY && piece[C8] == EMPTY && piece[B8] == EMPTY)
            {
                add_move(E8, C8, CASTLE);
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
                add_move(passant + DOWN_LEFT, passant, type);
            }
            if (FILE(passant) != FILE_H && piece[passant + DOWN_RIGHT] == PAWN && color[passant + DOWN_RIGHT] == WHITE)
            {
                add_move(passant + DOWN_RIGHT, passant, type);
            }
        }
        else
        {
            if (FILE(passant) != FILE_A && piece[passant + UP_LEFT] == PAWN && color[passant + UP_LEFT] == BLACK)
            {
                add_move(passant + UP_LEFT, passant, type);
            }
            if (FILE(passant) != FILE_H && piece[passant + UP_RIGHT] == PAWN && color[passant + UP_RIGHT] == WHITE)
            {
                add_move(passant + UP_RIGHT, passant, type);
            }
        }
    }
}