from tempfile import mkstemp
from shutil import move
from os import fdopen, remove, listdir

BASE_PATH = 'graphml'

def replace_file(file_path):
    index = 0
    #Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                subs = f'edge id="{index}"'
                for i in range(3):
                    line = line.replace(f'edge id="{i}"', subs)
                new_file.write(line)
                index = index + 1
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def fix_graphml_edges():
    for graphml_file in listdir(BASE_PATH):
        path = f"{BASE_PATH}/{graphml_file}"
        replace_file(path)

if __name__ == "__main__":
    fix_graphml_edges()