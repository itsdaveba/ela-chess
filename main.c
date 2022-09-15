#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

int main()
{
    printf("Random Chess Program\n\n");

    srand(time(NULL));

    move_t move;
    char command[MAX_COMMAND_LENGTH];
    int computer_side = EMPTY;

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

        if (!strcmp(command, "fen"))
        {
            getchar();
            fgets(fen, MAX_FEN_LENGTH, stdin);
            fen[strcspn(fen, "\n")] = '\0';
            if (!set_board(fen))
            {
                printf("Error: wrong FEN format\n");
            }
            continue;
        }
        if (!strcmp(command, "d"))
        {
            print_board();
            continue;
        }
        if (!strcmp(command, "moves"))
        {
            for (int m = 0; m < n_moves; m++)
            {
                printf("%s\n", move_to_lan(move_list[m]));
            }
            continue;
        }
        if (!strcmp(command, "exit"))
        {
            break;
        }
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
        if (color[move.from] == WHITE)
        {
            lan[4] = piece_to_char[move.prom];
        }
        else
        {
            lan[4] = piece_to_char[move.prom] | ' ';
        }
        lan[5] = '\0';
    }
    else if (lan[4] != '\0')
    {
        lan[4] = '\0';
    }

    return lan;
}