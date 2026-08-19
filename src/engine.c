#include "engine.h"

void init_engine(Engine *engine)
{
}

void set_hash_size(Engine *engine, int size)
{
}

void reset_engine(Engine *engine)
{
}

Move engine_search(Engine *engine, Position *position, int max_time, int max_depth, int max_nodes)
{
    Move best_move;
    engine->stop = false;
    engine->best_move = best_move;
    return engine->best_move;
}