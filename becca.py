import click, os, shutil, json
from click.utils import echo

#### CONFIGURATION VARIABLES ####

CONFIGFILE = '.becignore'
IGNOREDIRS = ['ext_temp','release','.git'] # [TEMP FOLDER, ARCIVE FOLDER, GIT]
IGNOREFILES = [CONFIGFILE,'.gitignore']
PARENTDIRECTORY = os.getcwd()
TEMPDIRECTORY  = os.path.join(PARENTDIRECTORY,IGNOREDIRS[0])
EXCLUDED = [] # (path, directory, file)

#### COMMAND LINE OPTIONS ####

@click.command()
@click.option('--overwrite', '-o', is_flag=True, help="Will overwrite if zip file for current version already exists.")

#### MAIN LOOP ####

def package(overwrite):
    filename = readManifestFile()
    if filename is not None:
        readIgnoreFile()
        createTempDir()
        filesystemProcess()
        archive(filename,overwrite)
        removeTempDir()
    else:
        pass

#### FILE SYSTEM OPERATIONS ####

# Walk through the subdirectories and recreate files and directories in ext_temp folder,
# will ignore any files or directories in EXCLUDED, IGNOREDIRS, AND IGNOREFILES.
def filesystemProcess():
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        dirs[:] = [d for d in dirs if d not in IGNOREDIRS]
        files[:] = [f for f in files if f not in IGNOREFILES]
        path = readPath(root)
        if path == "":
            path = None
        removeIgnoredFiles(path,files)
        removeIgnoredDirectories(path,dirs)
        createDirectories(path,dirs)
        copyFiles(path,files)

def removeIgnoredDirectories(path,directory_list):
    for item in EXCLUDED:
        if item[0] == path and item[1] is not None:
            directory_list.remove(item[1])
    
    return directory_list

def removeIgnoredFiles(path,file_list):
    """Todo: add functionality for ignoring extensions i.e. *.log"""
    for item in EXCLUDED:
        if item[0] is None and str(item[2]).find("*") != -1:
            ignoreFiles = str(item[2]).split(".")
            for file in reversed(file_list):
                extension = file.split(".")
                if extension[1] == ignoreFiles[1]:
                    file_list.remove(file)
        elif item[0] is None and item[2] is not None:
            try:
                file_list.remove(item[2])
            except:
                pass
        elif item[0] == path and item[2] is not None:
            file_list.remove(item[2])
    return file_list

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

def archive(archiveName,overwrite):
    os.chdir(TEMPDIRECTORY)
    outputDirectory = os.path.join(PARENTDIRECTORY,IGNOREDIRS[1])
    if os.path.isdir(outputDirectory):
        pass
    else:
        os.mkdir(outputDirectory)
    
    outputFile = os.path.join(outputDirectory,archiveName)

    if overwrite:
        shutil.make_archive(outputFile, 'zip', TEMPDIRECTORY)
    else:
        if os.path.isfile(outputFile+'.zip'):
            click.echo("An archive file already exists for: \"" + archiveName + '.zip\"')
            if click.confirm("Would you like to continue?: "):
                click.echo("Overwriting existing archive...")
                shutil.make_archive(outputFile, 'zip', TEMPDIRECTORY)
            else:
                pass
        else:
            shutil.make_archive(outputFile, 'zip', TEMPDIRECTORY)
    
    os.chdir(PARENTDIRECTORY)

#### UTILITY FUNCTIONS ####

def readIgnoreFile():
    with open(CONFIGFILE,'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.find('/') != -1:
            seperator = '/'
        elif line.find('\\') != -1:
            seperator = '\\'
        else:
            seperator = None
        
        if seperator is not None:
            newLine = line.strip().rsplit(seperator)
            if len(newLine) == 2:
                if newLine[1] == "":
                    EXCLUDED.append(tuple([None,newLine[0],None]))
                else:
                    EXCLUDED.append(tuple([newLine[0],None,newLine[1]]))
            else:
                EXCLUDED.append(tuple([newLine[0],newLine[1],None]))
        else:
            EXCLUDED.append(tuple([None,None,line.strip()]))
    file.close()

def readManifestFile():
    if os.path.isfile('manifest.json'):
        with open('manifest.json','r') as file:
            data = file.read()
        
        item = json.loads(data)
        export = str(item['name']) + "-" + str(item['version'])
        return export
    else:
        click.echo("Exiting script, no manifest file found.")
        return None

def createTempDir():
    removeTempDir()
    os.mkdir(TEMPDIRECTORY)

def removeTempDir():
    if os.path.isdir(TEMPDIRECTORY):
        shutil.rmtree(TEMPDIRECTORY)

def readPath(root):
    lenPar = len(str(PARENTDIRECTORY))
    return root[lenPar + 1:]

#### RUN SCRIPT ####

if __name__ == '__main__':
    package()