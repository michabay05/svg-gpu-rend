#include "vendor/include/raylib.h"
#define ARENA_IMPLEMENTATION
#include "vendor/include/arena.h"

typedef float f32;

int main(void)
{
    SetTraceLogLevel(LOG_WARNING);
    InitWindow(800, 600, "svg render - gpu");
    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        BeginDrawing(); {
            ClearBackground(BLACK);
        } EndDrawing();
    }

    CloseWindow();
    return 0;
}
