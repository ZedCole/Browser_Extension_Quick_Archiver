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
    removeTempDir()

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
    # print(root[lenPar + 1:])

# run through directories & sub-directories
def checkDir():
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        dirs[:] = [d for d in dirs if d not in IGNOREDIRS]      # use these to remove other files & directories
        files[:] = [f for f in files if f not in IGNOREFILES]   # copy what is left, just loop the array 
        path = readPath(root)
        debugPrint(path,dirs,files)   

def debugPrint(path,directory_list,file_list):
    print("Current Directory: ", "Base Directory" if path == "" else path)
    print("Sub Directories: " + str(directory_list))
    print("Files: " + str(file_list))
    print("---------------\n")

def createTempDir():
    os.mkdir(TEMPDIRECTORY)

def removeTempDir():
    if os.path.isdir(TEMPDIRECTORY):
        shutil.rmtree(TEMPDIRECTORY)

def copyFileItem(fileName):
    srcFile = os.path.join(PARENTDIRECTORY, fileName)
    destFile = os.path.join(TEMPDIRECTORY, fileName)
    shutil.copyfile(srcFile, destFile)

def archive(archiveName):
    os.chdir(TEMPDIRECTORY)
    # Check if output folder exists fist
    outputFolder = os.path.join(PARENTDIRECTORY,'output')
    outputFile = os.path.join(outputFolder,archiveName)
    shutil.make_archive(outputFile, 'zip', TEMPDIRECTORY)

if __name__ == '__main__':
    package()