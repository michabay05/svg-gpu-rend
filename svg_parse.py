import sys
import svgelements as se

def parse_svg_to_data(svg_filename):
    svg = se.SVG.parse(svg_filename)
    final_paths = []

    for element in svg.elements():
        if isinstance(element, se.Shape):
            # 1. Apply transforms (scale, rotation, groups)
            absolute_shape = element * element.transform

            # 2. Get the path object
            #    If it's a Rect/Circle, convert to Path. If it's already a Path, use it.
            if isinstance(absolute_shape, se.Path):
                path_obj = absolute_shape
            else:
                path_obj = absolute_shape.as_path()

            path_commands = []

            # 3. Iterate through segments manually
            #    This fixes the AttributeError by checking each segment type.
            for segment in path_obj:

                # --- Complex Curves: Arcs & Quadratics ---
                # These need to be converted to Cubic Beziers for your C engine
                if isinstance(segment, (se.Arc, se.QuadraticBezier)):
                    for curve in segment.as_cubic_curves():
                        path_commands.append(("C", [
                            curve.control1.x, curve.control1.y,
                            curve.control2.x, curve.control2.y,
                            curve.end.x, curve.end.y
                        ]))

                # --- Standard Cubic Bezier ---
                elif isinstance(segment, se.CubicBezier):
                    path_commands.append(("C", [
                        segment.control1.x, segment.control1.y,
                        segment.control2.x, segment.control2.y,
                        segment.end.x, segment.end.y
                    ]))

                # --- Simple Lines & Moves ---
                elif isinstance(segment, se.Move):
                    path_commands.append(("M", [segment.end.x, segment.end.y]))

                elif isinstance(segment, se.Line):
                    path_commands.append(("L", [segment.end.x, segment.end.y]))

                elif isinstance(segment, se.Close):
                    path_commands.append(("Z", []))

            if path_commands:
                final_paths.append(path_commands)

    return final_paths

if len(sys.argv) != 2:
    print("Provide a single argument (input: svg to parse)")
    sys.exit(1)

paths = parse_svg_to_data(sys.argv[1])

for path in paths:
    for x in path:
        sp = ""
        for i, s in enumerate(x[1]):
            v = round(s, 5)
            if v == -0.0:
                v = 0

            if i != 0:
                sp += ", "
            sp += str(v)
        print(f"{x[0]} {sp}")
