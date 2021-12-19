#include <stdio.h>
#include <string.h>
#include "defs.h"
#include "data.h"
#include "protos.h"

int main() {
    printf("Ela Chess Program\n\n");

    char command[MAX_COMMAND_LENGTH];
    
    while(TRUE) {
        printf("ela> ");
        scanf("%s", command);

        if(!strcmp(command, "board")) {
            print_board();
        }
        if(!strcmp(command, "exit")) {
            break;
        }
    }

    return 0;
}