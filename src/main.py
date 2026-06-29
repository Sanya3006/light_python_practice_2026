import argparse
from step1 import validate_path
from step2 import scan_folder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='Source folder')
    args = parser.parse_args()
    src_path = validate_path(args.source)
    files = scan_folder(src_path)
    print(f"Found {len(files)} files:")
    for f in files:
        print(f"{f['rel']} (size={f['size']}, mtime={f['mtime']})")

if __name__ == '__main__':
    main()