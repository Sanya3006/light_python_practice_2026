import os,sys
def validate_path(p):
    if not os.path.isdir(p): print(f"Error: '{p}' not exists"); sys.exit(1)
    return os.path.abspath(p)