import click, os, shutil

from click.utils import echo

PARENTDIRECTORY = os.getcwd()
TEMPDIRECTORY  = os.path.join(PARENTDIRECTORY,"ext_temp")
CONFIGFILE = '.extensionpackignore'
IGNOREDIRS = ['ext_temp','output','.git']
IGNOREFILES = ['.extensionpackignore','.gitignore']
EXCLUDED = [(None,None,'ignorethisfile.txt'),(None,'notme',None),
            ('lol','ignorethisfolder',None),('lol',None,'pleaseignoreme.txt')] # (path, directory, file)

@click.command()
@click.option('--overwrite', '-o', is_flag=True, help="Will overwrite if zip file for current version already exists.")

def package(overwrite):
    removeTempDir()
    if overwrite:
        click.echo("Overwriting...")
    createTempDir()
    checkDir()
    # readPath()
    # archive()
    # removeTempDir()

"""
    TO DO:
     - Create function to read manifest.json for name & version
"""

def readconfig(config):
    read = os.path.join(PARENTDIRECTORY, config)
    file = open(read, 'r')
    return file

def readPath(root):
    lenPar = len(str(PARENTDIRECTORY))
    return root[lenPar + 1:]

# run through directories & sub-directories
def checkDir():
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        dirs[:] = [d for d in dirs if d not in IGNOREDIRS]      # use these to remove other files & directories
        files[:] = [f for f in files if f not in IGNOREFILES]   # copy what is left, just loop the array 
        path = readPath(root)
        if path == "":
            path = None
        removeIgnoredFiles(path,files)
        removeIgnoredDirectory(path,dirs)
        debugPrint(path,dirs,files)
        createDirectories(path,dirs)
        copyFiles(path,files)
        print("---------------\n")

def removeIgnoredDirectory(path,directory_list):
    for item in EXCLUDED:
        if item[0] == path and item[1] is not None:
            directory_list.remove(item[1])
    
    return directory_list

def removeIgnoredFiles(path,file_list):
    # Check for *.extension expressions
    """Todo: add functionality for ignoring extensions i.e. *.log"""
    for item in EXCLUDED:
        if item[0] is None and item[2] is not None:
            try:
                file_list.remove(item[2])
            except:
                pass
        elif item[0] == path and item[2] is not None:
            file_list.remove(item[2])

    return file_list

def debugPrint(path,directory_list,file_list):
    print("Current Directory: ", "Base Directory" if path is None else path)
    print("Sub Directories: " + str(directory_list))
    print("Files: " + str(file_list))

def copyFiles(path,file_list):
    for file in file_list:
        if path is not None:
            srcFile = os.path.join(PARENTDIRECTORY,path,file)
            destFile = os.path.join(TEMPDIRECTORY,path,file)
        else:
            srcFile = os.path.join(PARENTDIRECTORY,file)
            destFile = os.path.join(TEMPDIRECTORY,file)
        
        shutil.copyfile(srcFile,destFile)

def createDirectories(path,directory_list):
    for dir in directory_list:
        if path is not None:
            newDir = os.path.join(TEMPDIRECTORY,path,dir)
            os.mkdir(newDir)
        else:
            newDir = os.path.join(TEMPDIRECTORY,dir)
            os.mkdir(newDir)

def createTempDir():
    os.mkdir(TEMPDIRECTORY)

def removeTempDir():
    if os.path.isdir(TEMPDIRECTORY):
        shutil.rmtree(TEMPDIRECTORY)

def archive(archiveName):
    os.chdir(TEMPDIRECTORY)
    # Check if output folder exists fist
    outputFolder = os.path.join(PARENTDIRECTORY,'output')
    outputFile = os.path.join(outputFolder,archiveName)
    shutil.make_archive(outputFile, 'zip', TEMPDIRECTORY)

if __name__ == '__main__':
    package()