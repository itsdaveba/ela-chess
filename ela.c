#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

int main() {

    printf("Ela Chess Program\n\n");

    char *fen;
    char command[MAX_COMMAND_LENGTH];

    set_board(INIT_FEN);
    fen = get_fen();
    
    while(TRUE) {
        printf("ela> ");
        scanf("%s", command);

        if(!strcmp(command, "d")) {
            print_board();
        }
        if(!strcmp(command, "fen")) {
            getchar();
            fgets(fen, MAX_FEN_LENGTH, stdin);
            fen[strcspn(fen, "\n")] = '\0';
            if(!set_board(fen)) {
                set_board(INIT_FEN);
                printf("Error: wrong FEN format\n");
            }
        }
        if(!strcmp(command, "exit")) {
            break;
        }
    }

    return 0;
}