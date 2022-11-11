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
    init_hash();
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    hply = 0;
    set_board(INIT_FEN);
    set_hash();
    if (!open_book())
    {
        printf("Warning: opening book missing\n");
    }

    while (TRUE)
    {
        if (side == computer_side)
        {
            move = search(post, book);
            if (move.bytes.type & NO_MOVE || !make_move(move))
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
        if (fgets(input, MAX_INPUT_LENGTH, stdin) == NULL)
        {
            printf("\n");
            exit(0);
        }
        if (!strchr(input, '\n'))
        {
            while (getchar() != '\n');
        }
        command = strtok(input, " \n"); // TODO: ? command
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
            book = TRUE;
            set_board(INIT_FEN);
            set_hash();
            continue;
        }
        if (!strcmp(command, "fen") || !strcmp(command, "setboard"))
        {
            char *fen = strtok(NULL, "\n");
            hply = 0;
            book = FALSE;
            if (!xboard)
            {
                computer_side = EMPTY;
            }
            if (fen == NULL || !set_board(fen))
            {
                book = TRUE;
                set_board(INIT_FEN);
                printf("Error: wrong FEN format\n");
            }
            set_hash();
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
        if (move.bytes.type & NO_MOVE)
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
        if (move.bytes.type & ILLEGAL_MOVE || !make_move(move))
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

// Move to LAN
char *move_to_lan(move_t move)
{
    static char lan[MAX_LAN_LENGTH];

    lan[0] = FILE(move.bytes.from) + 'a';
    lan[1] = RANK(move.bytes.from) + '1';
    lan[2] = FILE(move.bytes.to) + 'a';
    lan[3] = RANK(move.bytes.to) + '1';

    if (move.bytes.type & PROMOTION)
    {
        lan[4] = piece_char[move.bytes.prom] | ' ';
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

// LAN to pseudo-legal move
move_t lan_to_move(char *lan)
{
    move_t move;
    int n_moves;
    gen_t move_list[MAX_GEN_MOVES];

    if (lan[0] < 'a' || lan[0] > 'h' ||
        lan[1] < '1' || lan[1] > '8' ||
        lan[2] < 'a' || lan[2] > 'h' ||
        lan[3] < '1' || lan[3] > '8')
    {
        move.bytes.type = NO_MOVE;
        return move;
    }

    move.bytes.from = SQUARE(lan[0], lan[1]);
    move.bytes.to = SQUARE(lan[2], lan[3]);
    move.bytes.type = ILLEGAL_MOVE;
    switch (lan[4])
    {
    case ' ':
    case '\n':
    case '\0':
        move.bytes.prom = EMPTY;
        break;
    case 'n':
        move.bytes.prom = KNIGHT;
        break;
    case 'b':
        move.bytes.prom = BISHOP;
        break;
    case 'r':
        move.bytes.prom = ROOK;
        break;
    case 'q':
        move.bytes.prom = QUEEN;
        break;
    default:
        return move;
    }

    n_moves = gen_moves(move_list, FALSE);

    for (int m = 0; m < n_moves; m++)
    {
        if ((move_list[m].move.id & 0xFFFFFF) == (move.id & 0xFFFFFF))
        {
            return move_list[m].move;
        }
    }

    return move;
}

// Print result at end of game
bool print_result()
{
    int m;
    int n_moves;
    gen_t move_list[MAX_GEN_MOVES];

    n_moves = gen_moves(move_list, FALSE);

    for (m = 0; m < n_moves; m++)
    {
        if (make_move(move_list[m].move))
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
    if (repetition() >= 3)
    {
        printf("1/2-1/2 {Draw by repetition}\n");
        return TRUE;
    }
    if (halfmove >= 100)
    {
        printf("1/2-1/2 {Draw by fifty move rule}\n");
        return TRUE;
    }

    return FALSE;
}