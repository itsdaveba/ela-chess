#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

void xboard()
{
    move_t move;
    char line[MAX_COMMAND_LENGTH];
    char command[MAX_COMMAND_LENGTH];
    int computer_side = EMPTY;
    
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    printf("\n");

    while (TRUE)
    {
        if (side == computer_side)
        {
            move = search();
            char *lan = move_to_lan(move);
            printf("move %s\n", lan);
            make_move(move);
            ply = 0;
            gen_moves();
            continue;
        }

        fgets(line, MAX_COMMAND_LENGTH, stdin);
        sscanf(line, "%s", command);

        if (!strcmp(command, "new"))
        {
            computer_side = BLACK;
            set_board(INIT_FEN);
            hply = 0;
            ply = 0;
            gen_moves();
            continue;
        }
        if (!strcmp(command, "setboard"))
        {
            char *fen = line + 9;
            fen[strcspn(fen, "\n")] = '\0';
            set_board(fen);
            hply = 0;
            ply = 0;
            gen_moves();
            continue;
        }
        if (!strcmp(command, "go"))
        {
            computer_side = side;
            continue;
        }
        if (!strcmp(command, "force"))
        {
            computer_side = EMPTY;
            continue;
        }
        if (!strcmp(command, "undo"))
        {
            take_back();
            ply = 0;
            gen_moves();
            continue;
        }
        if (!strcmp(command, "quit"))
        {
            break;
        }

        move = lan_to_move(command);
        if (move.type == NO_MOVE)
        {
            printf("Error (unknown command): %s\n", command);
            continue;
        }
        if (move.type == ILLEGAL_MOVE || !make_move(move))
        {
            printf("Illegal move: %s\n", command);
            continue;
        }
        ply = 0;
        gen_moves();
    }
}