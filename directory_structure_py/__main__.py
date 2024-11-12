"""directory_structure_py"""


from .src.main import main, DEFAULT_OUTPUT_NAME


if __name__ == "__main__":
    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str)
    parser.add_argument(
        "--dst", dest="dst", type=str, default=""
    )
    parser.add_argument(
        "--include_root_path", dest="include_root_path", action="store_true"
    )
    parser.add_argument(
        "--in_tree", dest="in_tree", action="store_true"
    )
    parser.add_argument(
        "--to_tsv", dest="to_tsv", action="store_true"
    )
    args = parser.parse_args()
    if not args.dst:
        if os.path.isdir(args.src):
            args.dst = os.path.join(args.src, DEFAULT_OUTPUT_NAME)
        else:
            args.dst = os.path.join(os.path.dirname(args.src), DEFAULT_OUTPUT_NAME)
    main(args.src, args.dst, args.include_root_path, args.in_tree, args.to_tsv)
