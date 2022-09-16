#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

int main()
{
    move_t move;
    char command[MAX_COMMAND_LENGTH];
    int computer_side = EMPTY;

    printf("Random Chess Program\n\n");

    srand(time(NULL));

    set_board(INIT_FEN);
    hply = 0;
    ply = 0;
    gen_moves();

    while (TRUE)
    {
        if (side == computer_side)
        {
            move = search();
            if (move.type == NO_MOVE)
            {
                printf("No legal moves\n");
                computer_side = EMPTY;
                continue;
            }
            char *lan = move_to_lan(move);
            printf("Random move: %s\n", lan);
            make_move(move);
            ply = 0;
            gen_moves();
            continue;
        }

        printf("random> ");
        scanf("%s", command);

        if (!strcmp(command, "new"))
        {
            computer_side = EMPTY;
            set_board(INIT_FEN);
            hply = 0;
            ply = 0;
            gen_moves();
            continue;
        }
        if (!strcmp(command, "fen"))
        {
            char fen[MAX_FEN_LENGTH];
            computer_side = EMPTY;
            getchar();
            fgets(fen, MAX_FEN_LENGTH, stdin);
            fen[strcspn(fen, "\n")] = '\0';
            if (!set_board(fen))
            {
                set_board(INIT_FEN);
                printf("Error: wrong FEN format\n");
            }
            hply = 0;
            ply = 0;
            gen_moves();
            continue;
        }
        if (!strcmp(command, "d"))
        {
            print_board();
            continue;
        }
        if (!strcmp(command, "on"))
        {
            computer_side = side;
            continue;
        }
        if (!strcmp(command, "off"))
        {
            computer_side = EMPTY;
            continue;
        }
        if (!strcmp(command, "undo"))
        {
            if (hply == 0)
            {
                printf("Error: no previous move\n");
                continue;
            }
            computer_side = EMPTY;
            take_back();
            ply = 0;
            gen_moves();
            continue;
        }
        if (!strcmp(command, "perft"))
        {
            int depth;
            u64 nodes;
            computer_side = EMPTY;
            if (scanf("%d", &depth) == 0 || depth < 1)
            {
                printf("Error: wrong perft depth\n");
                continue;
            }
            for (int d = 1; d <= depth; d++)
            {
                nodes = perft(d);
                printf("perft(%d)= %10llu\n", d, nodes);
            }
            continue;
        }
        if (!strcmp(command, "xboard"))
        {
            xboard();
            break;
        }
        if (!strcmp(command, "exit"))
        {
            break;
        }

        move = lan_to_move(command);
        if (move.type == NO_MOVE)
        {
            printf("Error: uknown command\n");
            continue;
        }
        if (move.type == ILLEGAL_MOVE || !make_move(move))
        {
            printf("Error: illegal move\n");
            continue;
        }
        ply = 0;
        gen_moves();
    }

    return 0;
}

char *move_to_lan(move_t move)
{

    static char lan[MAX_LAN_LENGTH];

    lan[0] = FILE(move.from) + 'a';
    lan[1] = RANK(move.from) + '1';
    lan[2] = FILE(move.to) + 'a';
    lan[3] = RANK(move.to) + '1';

    if (move.type & PROMOTION)
    {
        if (side == WHITE)
        {
            lan[4] = piece_char[move.prom];
        }
        else
        {
            lan[4] = piece_char[move.prom] | ' ';
        }
        if (lan[5] != '\0')
        {
            lan[5] = '\0';
        }
    }
    else if (lan[4] != '\0')
    {
        lan[4] = '\0';
    }

    return lan;
}

move_t lan_to_move(char *lan)
{
    move_t move;

    if (lan[0] < 'a' || lan[0] > 'h' ||
        lan[1] < '1' || lan[1] > '8' ||
        lan[2] < 'a' || lan[2] > 'h' ||
        lan[3] < '1' || lan[3] > '8')
    {
        move.type = NO_MOVE;
        return move;
    }

    move.from = SQUARE(lan[0], lan[1]);
    move.to = SQUARE(lan[2], lan[3]);
    switch (lan[4] | ' ')
    {
    case ' ':
        move.prom = EMPTY;
        break;
    case 'r':
        move.prom = ROOK;
        break;
    case 'n':
        move.prom = KNIGHT;
        break;
    case 'b':
        move.prom = BISHOP;
        break;
    case 'q':
        move.prom = QUEEN;
        break;
    default:
        move.type = NO_MOVE;
        return move;
    }

    for (int m = 0; m < n_moves[0]; m++)
    {
        if (move_list[0][m].from == move.from && move_list[0][m].to == move.to && move_list[0][m].prom == move.prom)
        {
            return move_list[0][m];
        }
    }

    move.type = ILLEGAL_MOVE;
    return move;
}