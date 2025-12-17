#include "vendor/include/raylib.h"
#define NOB_IMPLEMENTATION
#define ARENA_IMPLEMENTATION
#include "svg_parse.h"
#include "vendor/include/raylib.h"

Vector2 foo(Vector2 v)
{
    Vector2 offset = {200, 200};
    return Vector2Add(offset, Vector2Scale(v, 5.f));
}

int main(void)
{
    SetConfigFlags(FLAG_MSAA_4X_HINT);
    InitWindow(800, 600, "span - svg_rend");
    SetTargetFPS(90);

    Arena arena = {0};
    ActionList al = get_path_info(&arena);
    // Shader shader = LoadShader(NULL, "qloopblinn-fs.glsl");

    while (!WindowShouldClose()) {
        BeginDrawing(); {
            ClearBackground(BLACK);

            for (int i = 0; i < al.count; i++) {
                Action act = al.items[i];
                switch (act.kind) {
                    case ACT_MOVE:
                    case ACT_CLOSE: break;

                    case ACT_CUBIC: {
                        Vector2 *p = act.points.items;
                        DrawSplineSegmentBezierCubic(
                            foo(p[0]), foo(p[1]), foo(p[2]), foo(p[3]), 3.f, RED);
                    } break;

                    case ACT_HORZ_TO: {
                        Vector2 *p = act.points.items;
                        DrawLineEx(foo(p[0]), foo(p[1]), 3.f, RED);
                    } break;

                    default: {
                        UNREACHABLEF("Unknown kind of action: %d", act.kind);
                    } break;
                }
            }
        } EndDrawing();
    }

    CloseWindow();
}
