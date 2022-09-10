#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "data.h"

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
    castling = 0;
    if (castl != NULL && strcmp(castl, "-"))
    {
        for (int i = 0; i < strlen(castl); i++)
        {
            if (castl[i + 1] != '\0' && castl[i] >= castl[i + 1])
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
        passant = ((pass[1] - '1') << 3) + pass[0] - 'a';
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

    int s = 0;
    char *row = strtok(brd, "/");
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

    int c = 0;
    
    for (int s = 0; s < 64; s++)
    {
        if (piece[board[s]] == EMPTY)
        {
            int ctr;
            for (ctr = 1; FILE(board[s]) != FILE_H && piece[board[s + 1]] == EMPTY; s++)
            {
                ctr++;
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