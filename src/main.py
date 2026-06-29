import argparse
import argparse
from step1 import validate_path
from step2 import scan_folder
from step3 import add_hashes, find_duplicates

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='Source folder')
    args = parser.parse_args()
    src_path = validate_path(args.source)
    files = scan_folder(src_path)
    files = add_hashes(files)
    dups = find_duplicates(files)
    print(f"Total files: {len(files)}")
    print(f"Unique files: {len(set(f['hash'] for f in files))}")
    print(f"Duplicate groups: {len(dups)}")
    for h, paths in dups.items():
        print(f"Hash {h[:16]}...: {len(paths)} files")
        for p in paths:
            print(f"  {p}")

if __name__ == '__main__':
    main()
