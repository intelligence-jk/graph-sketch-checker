import json
import sys
from .core import check_sketch


def main(argv=None):
    a = sys.argv[1:] if argv is None else argv
    if len(a) != 2:
        print("usage: python -m sketchcheck '[1,-3,2]' '{\"roots\":[1]}'")
        return 2
    problems = check_sketch(json.loads(a[0]), json.loads(a[1]))
    print("\n".join(problems) if problems else "Sketch is consistent.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
