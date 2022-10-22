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
    char *command;
    char input[MAX_INPUT_LENGTH];

    int computer_side = EMPTY;
    bool xboard = FALSE;
    bool post = FALSE;
    bool book = TRUE;

    search_time = DEFAULT_TIME;
    search_depth = __INT_MAX__;

    printf("Ela Chess Program\n\n");

    srand(time(NULL));
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    hply = 0;
    set_board(INIT_FEN);
    if (!open_book())
    {
        printf("Warning: opening book missing\n");
    }

    while (TRUE)
    {
        if (side == computer_side)
        {
            move = search(post, book);
            if (move.type & NO_MOVE || !make_move(move))
            {
                computer_side = EMPTY;
                printf("Error: no legal moves\n");
                continue;
            }
            char *lan = move_to_lan(move);
            if (xboard)
            {
                printf("move %s\n", lan);
            }
            else
            {
                printf("Ela's move: %s\n", lan);
            }
            print_result();
            continue;
        }

        if (!xboard)
        {
            printf("ela> ");
        }
        fgets(input, MAX_INPUT_LENGTH, stdin);
        command = strtok(input, " \n");
        if (command == NULL)
        {
            continue;
        }

        if (!strcmp(command, "new"))
        {
            if (xboard)
            {
                computer_side = BLACK;
                search_time = DEFAULT_TIME;
                search_depth = __INT_MAX__;
            }
            else
            {
                computer_side = EMPTY;
            }
            hply = 0;
            set_board(INIT_FEN);
            continue;
        }
        if (!strcmp(command, "fen") || !strcmp(command, "setboard"))
        {
            char *fen = strtok(NULL, "\n");
            hply = 0;
            if (!xboard)
            {
                computer_side = EMPTY;
            }
            if (fen == NULL || !set_board(fen))
            {
                set_board(INIT_FEN);
                printf("Error: wrong FEN format\n");
            }
            continue;
        }
        if (!strcmp(command, "d"))
        {
            print_board();
            continue;
        }
        if (!strcmp(command, "on") || !strcmp(command, "go"))
        {
            computer_side = side;
            continue;
        }
        if (!strcmp(command, "off") || !strcmp(command, "force"))
        {
            computer_side = EMPTY;
            continue;
        }
        if (!strcmp(command, "st"))
        {
            char *temp = strtok(NULL, " \n");
            if (temp == NULL || sscanf(temp, "%d", &search_time) == 0 || search_time < 0)
            {
                search_time = DEFAULT_TIME;
                printf("Error: wrong search time\n");
                continue;
            }
            search_time *= 100;
            continue;
        }
        if (!strcmp(command, "sd"))
        {
            search_time = __INT_MAX__;
            char *temp = strtok(NULL, " \n");
            if (temp == NULL || sscanf(temp, "%d", &search_depth) == 0 || search_depth < 0)
            {
                search_depth = DEFAULT_DEPTH;
                printf("Error: wrong search depth\n");
            }
            continue;
        }
        if (!strcmp(command, "undo"))
        {
            if (hply == 0)
            {
                printf("Error: no previous move\n");
                continue;
            }
            if (!xboard)
            {
                computer_side = EMPTY;
            }
            take_back();
            continue;
        }
        if (!strcmp(command, "post"))
        {
            post = TRUE;
            continue;
        }
        if (!strcmp(command, "nopost"))
        {
            post = FALSE;
            continue;
        }
        if (!strcmp(command, "book"))
        {
            book = TRUE;
            continue;
        }
        if (!strcmp(command, "nobook"))
        {
            book = FALSE;
            continue;
        }
        if (!strcmp(command, "perft"))
        {
            int depth;
            u64 nodes;
            char *temp = strtok(NULL, " \n");
            computer_side = EMPTY;
            if (temp == NULL || sscanf(temp, "%d", &depth) == 0 || depth < 1)
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
            xboard = !xboard;
            printf("\n");
            continue;
        }
        if (!strcmp(command, "exit") || !strcmp(command, "quit"))
        {
            break;
        }

        move = lan_to_move(command);
        if (move.type & NO_MOVE)
        {
            if (xboard)
            {
                printf("Error (unknown command): %s\n", command);
            }
            else
            {
                printf("Error: uknown command\n");
            }
            continue;
        }
        if (move.type & ILLEGAL_MOVE || !make_move(move))
        {
            if (xboard)
            {
                printf("Illegal move: %s\n", command);
            }
            else
            {
                printf("Error: illegal move\n");
            }
            continue;
        }
        if (print_result())
        {
            computer_side = EMPTY;
        }
    }

    close_book();

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
        lan[4] = piece_char[move.prom] | ' ';
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
    int n_moves;
    move_t move_list[MAX_GEN_MOVES];

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
    move.type = ILLEGAL_MOVE;
    switch (lan[4])
    {
    case ' ':
    case '\n':
    case '\0':
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
        return move;
    }

    n_moves = gen_moves(move_list, FALSE);

    for (int m = 0; m < n_moves; m++)
    {
        if (move_list[m].from == move.from && move_list[m].to == move.to && move_list[m].prom == move.prom)
        {
            return move_list[m];
        }
    }

    return move;
}

bool print_result()
{
    int m;
    int n_moves;
    move_t move_list[MAX_GEN_MOVES];

    n_moves = gen_moves(move_list, FALSE);

    for (m = 0; m < n_moves; m++)
    {
        if (make_move(move_list[m]))
        {
            take_back();
            break;
        }
    }

    if (m == n_moves)
    {
        if (in_check(side))
        {
            if (side == WHITE)
            {
                printf("0-1 {Black mates}\n");
            }
            else
            {
                printf("1-0 {White mates}\n");
            }
        }
        else
        {
            printf("1/2-1/2 {Stalemate}\n");
        }
        return TRUE;
    }
    if (halfmove >= 100)
    {
        printf("1/2-1/2 {Draw by fifty move rule}\n");
        return TRUE;
    }

    return FALSE;
}