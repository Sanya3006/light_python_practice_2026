import hashlib
def compute_hash(p,chunk=65536):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(chunk),b''): h.update(b)
    return h.hexdigest()

def add_hashes(files):
    for f in files: f['hash']=compute_hash(f['path'])
    return files

def find_duplicates(files):
    groups={}
    for f in files: groups.setdefault(f['hash'],[]).append(f['rel'])
    return {h:lst for h,lst in groups.items() if len(lst)>1}