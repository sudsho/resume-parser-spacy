"""Quick CLI for parsing resumes from terminal."""
import argparse
import json
import sys

from .api import parse_resume_file


def main(argv=None):
    parser = argparse.ArgumentParser(description="parse a resume")
    parser.add_argument("path", help="path to .pdf, .docx, or .txt")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)

    result = parse_resume_file(args.path)
    indent = 2 if args.pretty else None
    print(json.dumps(result, indent=indent, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
