import argparse
import sys
from step1 import validate_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='Source folder')
    args = parser.parse_args()
    path = validate_path(args.source)
    print(f"Path '{path}' is valid.")

if __name__ == '__main__':
    main()