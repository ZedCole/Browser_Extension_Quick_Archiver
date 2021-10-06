import click, os, shutil, json

from click.utils import echo

PARENTDIRECTORY = os.getcwd()
TEMPDIRECTORY  = os.path.join(PARENTDIRECTORY,"ext_temp")
CONFIGFILE = 'ex_pack_list.txt'
FILEARRAY = []

@click.command()
@click.option('--overwrite', '-o', is_flag=True, help="Will overwrite if zip file for current version already exists.")


# Rewrite this with final code
def package(overwrite):
    if overwrite:
        click.echo("Overwriting...")
    click.echo("Temporary")
    # copyFileItem("test.txt")
    # os.chdir(TEMPDIRECTORY)
    # archive()
    copyFileTree()

"""
    Create function to read a ext_pack.json file
    Create function to read manifest.json for name & version
    Loop through files needed
    Delete ext_temp directory when done
"""
def copyFileTree():
    createTempDir()
    f = open(CONFIGFILE,'r')
    currentDir = None
    for line in f:
        if line.startswith('d:'):
            if line.startswith('d:base') is False:
                remNewLine = line.strip()
                dirName = remNewLine.split(':')
                currentDir = dirName
                newDir = os.path.join(TEMPDIRECTORY,dirName[1])
                os.mkdir(newDir)
            else:
                currentDir = "base"
        else:
            remNewLine = line.strip()
            fileName = remNewLine.split(':')
            if currentDir == "base":
                print(fileName)
                copyFileItem(fileName[1])
            else:
                # newFilePath = os.path.join(currentDir,fileName[1])
                # click.echo(newFilePath)
                copyFileItem(currentDir,fileName[1]) #something wrong here - no like directory
    f.close()

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