#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

int main() {

    printf("Ela Chess Program\n\n");

    srand(time(NULL));

    int m;
    char *lan;
    int computer_side;
    char fen[MAX_FEN_LENGTH];
    char command[MAX_COMMAND_LENGTH];

    set_board(INIT_FEN);
    gen_moves();
    
    while(TRUE) {

        if(side == computer_side) {
            m = search();
            lan = move_to_lan(m);
            printf("Ela's move: %s\n", lan);
            make_move(m);
            gen_moves();
            print_result();
            continue;
        }

        printf("ela> ");
        scanf("%s", command);

        if(!strcmp(command, "new")) {
            set_board(INIT_FEN);
            gen_moves();
            continue;
        }
        if(!strcmp(command, "fen")) {
            getchar();
            fgets(fen, MAX_FEN_LENGTH, stdin);
            fen[strcspn(fen, "\n")] = '\0';
            if(!set_board(fen)) {
                set_board(INIT_FEN);
                printf("Error: wrong FEN format\n");
            }
            gen_moves();
            continue;
        }
        if(!strcmp(command, "d")) {
            print_board();
            continue;
        }
        if(!strcmp(command, "on")) {
            computer_side = side;
            continue;
        }
        if(!strcmp(command, "off")) {
            computer_side = EMPTY;
            continue;
        }
        if(!strcmp(command, "exit")) {
            break;
        }
        if(!strcmp(command, "xboard")) {
            xboard();
            break;
        }

        m = lan_to_move(command);
        if(m == -1) {
            printf("Error: uknown command\n");
            continue;
        }
        if(m == -2 || !make_move(m)) {
            printf("Illegal move\n");
            continue;
        }
        gen_moves();
        print_result();

    }

    return 0;
}