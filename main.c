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

    search_time = DEFAULT_TIME;
    search_depth = DEFAULT_DEPTH;

    set_board(INIT_FEN);
    hply = 0;
    ply = 0;    
    gen_moves();
    
    while(TRUE) {

        if(side == computer_side) {
            m = search(FALSE);
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
            hply = 0;
            ply = 0;
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
        if(!strcmp(command, "st")) {
            if(scanf("%d", &search_time) == 0 || search_time < 0) {
                search_time = DEFAULT_TIME;
                printf("Error: wrong search time\n");
            }
            else {
                search_time *= 100;
            }
            if(search_time > MAX_TIME) {
                search_time = MAX_TIME;
                printf("Error: maximum search time reached (%d seconds)\n", MAX_TIME / 100);
            }
            continue;
        }
        if(!strcmp(command, "sd")) {
            if(scanf("%d", &search_depth) == 0 || search_depth < 0) {
                search_depth = DEFAULT_DEPTH;
                printf("Error: wrong search depth\n");
            }
            if(search_depth > MAX_DEPTH) {
                search_depth = MAX_DEPTH;
                printf("Error: maximum search depth reached (%d plies)\n", MAX_DEPTH);
            }
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