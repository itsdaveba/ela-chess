#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include "position.h"
#include "engine.h"
#include "move.h"

#define MAX_INPUT_LENGTH 128

typedef struct
{
    Engine *engine;
    Position *position;
    int time;
    int depth;
    int nodes;
} SearchArgs;

void *search(void *arg)
{
    SearchArgs *args = arg;
    Move best_move = engine_search(args->engine, args->position, args->time, args->depth, args->nodes);
    if (!args->engine->stop)
    {
        char best_move_str[6];
        move_string(best_move, best_move_str);
        printf("bestmove %s\n", best_move_str);
        fflush(stdout);
    }

    return NULL;
}

int main()
{
    pthread_t thread;
    Position position;
    Engine engine;

    reset_position(&position, STARTING_POSITION_FEN);
    init_engine(&engine);

    char line[MAX_INPUT_LENGTH];
    char *command;

    while (true)
    {
        fgets(line, MAX_INPUT_LENGTH, stdin);
        command = strtok(line, " \n");
        if (!command)
            continue;

        if (!strcmp(command, "uci"))
        {
            printf("id name ElaChess 1.0\n");
            printf("id author Dave Barragan\n");
            printf("option name Hash type spin default %u min %u max %u\n", DEFAULT_HASH_SIZE, MIN_HASH_SIZE, MAX_HASH_SIZE);
            printf("uciok\n");
            fflush(stdout);
        }
        else if (!strcmp(command, "setoption"))
        {
            strtok(NULL, " \n");
            char *name = strtok(NULL, " \n");
            strtok(NULL, " \n");
            char *value = strtok(NULL, " \n");
            if (!name || !value)
                continue;
            if (!strcmp(name, "Hash"))
            {
                int size = atoi(value);
                if (size < MIN_HASH_SIZE || size > MAX_HASH_SIZE)
                    continue;
                set_hash_size(&engine, size);
            }
            else
            {
                printf("No such option: '%s'\n", name);
                fflush(stdout);
            }
        }
        else if (!strcmp(command, "isready"))
        {
            printf("readyok\n");
            fflush(stdout);
        }
        else if (!strcmp(command, "ucinewgame"))
        {
            reset_engine(&engine);
        }
        else if (!strcmp(command, "position"))
        {
            char *param = strtok(NULL, " \n");
            if (!param)
                continue;
            if (!strcmp(param, "startpos"))
            {
                reset_position(&position, STARTING_POSITION_FEN);
            }
            else if (!strcmp(param, "fen"))
            {
                char *fen = strtok(NULL, "m\n");
                reset_position(&position, fen);
            }
            else
                continue;
            strtok(NULL, " \n");
            char *lan = strtok(NULL, " \n");
            while (lan)
            {
                Move move = parse_move(lan);
                make_move(&position, move);
                lan = strtok(NULL, " \n");
            }
        }
        else if (!strcmp(command, "go"))
        {
            int time = -1;
            int depth = -1;
            int nodes = -1;

            char *subcommand = strtok(NULL, " \n");
            if (!subcommand)
                continue;
            if (!strcmp(subcommand, "perft"))
            {
                char *value = strtok(NULL, " \n");
                if (!value)
                    continue;
                depth = atoi(value);
                if (!depth)
                    continue;
                clock_t start = clock();
                nodes = perft(&position, depth);
                time = 1000 * (clock() - start) / CLOCKS_PER_SEC;
                printf("info depth %d nodes %d nps %d time %d\n", depth, nodes, 1000 * nodes / time, time);
                fflush(stdout);
                continue;
            }

            if (!strcmp(subcommand, "movetime"))
            {
                char *value = strtok(NULL, " \n");
                if (!value)
                    continue;
                time = atoi(value);
                if (!time)
                    continue;
            }
            else if (!strcmp(subcommand, "depth"))
            {
                char *value = strtok(NULL, " \n");
                if (!value)
                    continue;
                depth = atoi(value);
                if (!depth)
                    continue;
            }
            else if (!strcmp(subcommand, "nodes"))
            {
                char *value = strtok(NULL, " \n");
                if (!value)
                    continue;
                nodes = atoi(value);
                if (!nodes)
                    continue;
            }
            else
            {
                char *wtime = strtok(NULL, " \n");
                strtok(NULL, " \n");
                char *btime = strtok(NULL, " \n");
                strtok(NULL, " \n");
                char *winc = strtok(NULL, " \n");
                strtok(NULL, " \n");
                char *binc = strtok(NULL, " \n");
                if (position.side == WHITE)
                {
                    if (wtime && winc)
                        time = atoi(wtime) / 20 + atoi(winc) / 2;
                }
                else if (position.side == BLACK)
                {
                    if (btime && binc)
                        time = atoi(btime) / 20 + atoi(binc) / 2;
                }
            }

            SearchArgs args;
            args.engine = &engine;
            args.position = &position;
            args.time = time;
            args.depth = depth;
            args.nodes = nodes;

            pthread_create(&thread, NULL, search, &args);
        }
        else if (!strcmp(command, "stop"))
        {
            engine.stop = true;
            if (pthread_join(thread, NULL) == EINVAL)
            {
                char best_move_str[6];
                move_string(engine.best_move, best_move_str);
                printf("bestmove %s\n", best_move_str);
                fflush(stdout);
            }
        }
        else if (!strcmp(command, "d"))
        {
            display_position(&position);
            char fen[MAX_FEN_LENGTH];
            get_fen(&position, fen);
            printf("FEN: %s\n", fen);
            fflush(stdout);
        }
        else if (!strcmp(command, "eval"))
        {
            printf("%+.2f (white side)\n", (double)position.eval / 100);
            fflush(stdout);
        }
        else if (!strcmp(command, "quit"))
        {
            engine.stop = true;
            pthread_join(thread, NULL);
            break;
        }
        else
        {
            printf("Unknown command '%s'\n", command);
            fflush(stdout);
        }
    }

    return 0;
}