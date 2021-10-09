import click, os, shutil, json

from click.utils import echo

PARENTDIRECTORY = os.getcwd()
TEMPDIRECTORY  = os.path.join(PARENTDIRECTORY,"ext_temp")
CONFIGFILE = '.packignore'

@click.command()
@click.option('--overwrite', '-o', is_flag=True, help="Will overwrite if zip file for current version already exists.")
@click.option('--conf', '-c', is_flag=True, help="Pass a config file.")

# New direction to take script:
# store files & directories in an array (check how to search directory recursively)
# check current file against array
# if it exists in the array ignore the current one
# if id does not exist in the array copy the file

# build a function to check the current line for "\/." and count that as a file (edge case "files that dont have extensions")
# read each division and  enter into a set array (dir,file) 
# do the appropriate

# Rewrite this with final code
def package(overwrite,conf):
    if overwrite:
        click.echo("Overwriting...")
    click.echo("Temporary")
    if conf:
        file = readconfig(conf) #this is not done
    else:
        file = readconfig(CONFIGFILE)
    for line in file:
        print("Line " + ": " + line.strip())
    checkDir()
    # copyFileItem("test.txt")
    # os.chdir(TEMPDIRECTORY)
    # archive()
    # copyFileTree()
    # createTempDir()
    # removeTempDir()

"""
    Create function to read a ext_pack.json file
    Create function to read manifest.json for name & version
    Loop through files needed
    Delete ext_temp directory when done
"""

def readconfig(config):
    read = os.path.join(PARENTDIRECTORY, config)
    file = open(read, 'r')
    return file

# use tuples? [(path, directory), (path, directory)]
# only remove directory if it exists under path

excludeDir = ["notme","ignorethisfolder"]
excludeFile = ["pleaseignoreme.txt",".packignore"]
# run through directories & sub-directories
def checkDir():
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        dirs[:] = [d for d in dirs if d not in excludeDir]
        files[:] = [f for f in files if f not in excludeFile]
        print(root)
        print(dirs)
        print(files)
        print("-----------")

def createTempDir():
    os.mkdir(TEMPDIRECTORY)

def removeTempDir():
    shutil.rmtree(TEMPDIRECTORY)

def copyFileItem(fileName):
    srcFile = os.path.join(PARENTDIRECTORY, fileName)
    destFile = os.path.join(TEMPDIRECTORY, fileName)
    shutil.copyfile(srcFile, destFile)

def archive(archiveName):
    outputFolder = os.path.join(PARENTDIRECTORY,'output')
    outputFile = os.path.join(outputFolder,archiveName)
    shutil.make_archive(outputFile, 'zip', TEMPDIRECTORY)

if __name__ == '__main__':
    package()