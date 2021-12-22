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
    u64 nodes;
    int perft_depth;
    char fen[MAX_FEN_LENGTH];
    char command[MAX_COMMAND_LENGTH];
    int computer_side = EMPTY;

    set_board(INIT_FEN);
    hply = 0;
    ply = 0;    
    gen_moves();
    
    while(TRUE) {

        if(side == computer_side) {
            m = search();
            if(m == -1) {
                computer_side = EMPTY;
                continue;
            }
            lan = move_to_lan(m);
            printf("Ela's move: %s\n", lan);
            make_move(m);
            ply = 0;
            gen_moves();
            print_result();
            continue;
        }

        fflush(stdin);
        printf("ela> ");
        scanf("%s", command);

        if(!strcmp(command, "new")) {
            computer_side = EMPTY;
            set_board(INIT_FEN);
            gen_moves();
            continue;
        }
        if(!strcmp(command, "fen")) {
            computer_side = EMPTY;
            getchar();
            fgets(fen, MAX_FEN_LENGTH, stdin);
            fen[strcspn(fen, "\n")] = '\0';
            if(!set_board(fen)) {
                set_board(INIT_FEN);
                printf("Error: wrong FEN format\n");
            }
            hply = 0;
            ply = 0;
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
        if(!strcmp(command, "undo")) {
            if(hply == 0) {
                continue;
            }
            computer_side = EMPTY;
            take_back();
            ply = 0;
            gen_moves();
            continue;
        }
        if(!strcmp(command, "perft")) {
            computer_side = EMPTY;
            if(scanf("%d", &perft_depth) == 0 || perft_depth < 1) {
                printf("Error: wrong perft depth\n");
                continue;
            }
            for(int d = 1; d <= perft_depth; d++) {
                nodes = Perft(d);
                printf("perft(%d)= %10llu\n", d, nodes);
            }
            ply = 0;
            gen_moves();
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
        ply = 0;
        gen_moves();
        print_result();

    }

    return 0;
}