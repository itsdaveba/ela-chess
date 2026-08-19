#ifndef ENGINE_H
#define ENGINE_H

#define MIN_HASH_SIZE 1
#define MAX_HASH_SIZE 8192
#define DEFAULT_HASH_SIZE 512

#include "move.h"
#include "position.h"

typedef struct
{
    bool stop;
    Move best_move;
} Engine;

void init_engine(Engine *engine);
void set_hash_size(Engine *engine, int size);
void reset_engine(Engine *engine);
Move engine_search(Engine *engine, Position *position, int max_time, int max_depth, int max_nodes);

#endif