#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "protos.h"

int main()
{
    char fen[MAX_FEN_LENGTH];
    char command[MAX_COMMAND_LENGTH];

    set_board(INIT_FEN);

    while (TRUE)
    {
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
        if (!strcmp(command, "exit"))
        {
            break;
        }
    }

    return 0;
}