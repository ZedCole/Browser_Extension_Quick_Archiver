import click, os, shutil

parentDir = os.getcwd()
tempDir = "ext_temp"
path = os.path.join(parentDir,tempDir)

@click.command()
@click.option('--overwrite', '-o', is_flag=True, help="Will overwrite if zip file for current version already exists.")


# Rewrite this with final code
def package(overwrite):
    if overwrite:
        click.echo("Overwriting...")
    click.echo("Temporary")
    createTempDir()
    copyFileItem("test.txt")
    os.chdir(path)
    archive()

"""
    Create function to read a ext_pack.json file
    Create function to read manifest.json for name & version
    Loop through files needed
    Delete ext_temp directory when done
"""

def createTempDir():
    os.mkdir(path)

def removeTempDir():
    shutil.rmtree(path)

def copyFileItem(fileName):
    srcFile = os.path.join(parentDir, fileName)
    destFile = os.path.join(path, fileName)
    shutil.copyfile(srcFile, destFile)

def archive(archiveName):
    outputFolder = os.path.join(parentDir,'output')
    outputFile = os.path.join(outputFolder,archiveName)
    shutil.make_archive(outputFile, 'zip', path)

if __name__ == '__main__':
    package()