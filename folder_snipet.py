import os
import shutil
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("origin", help="Provide the origin path to search files with backslash.")
parser.add_argument("destination", help="Provide the destination path to copy files with backslash.")
parser.add_argument("extension", help="Give the extension of the files")
args = parser.parse_args()

#DIRECTORY = os.path.dirname(os.path.realpath(__file__)) 
origin = os.path.expanduser(f"~{args.origin}")
destination = os.path.expanduser(f"~{args.destination}")
extension = args.extension

def change_folder(origin):
    """ Change folder to the source directory """
    try:
        os.chdir(origin)
    except:
        print("The folder doesn't exist.")

def find_extension(ext):
    """ Walk directory and copy the files to new one """
    for root, dir, files in os.walk('.'):
        for f in files:
            try:
                if f.endswith(str(ext)) and os.path.exists(destination):
                    shutil.copy(f, destination)
                    #print(f, "primero")
                elif f.endswith(str(ext)):
                    os.mkdir(destination)
                    shutil.copy(f, destination)
                    #print(f, "segundo")
                else:
                    continue
            except FileNotFoundError as e:
                pass

change_folder(str(origin))
find_extension(extension)
print("Done")