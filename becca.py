import click
import os
import shutil
import json
from click.utils import echo

#### CONFIGURATION VARIABLES ####

CONFIG_FILE = '.becignore'
IGNORE_DIRS = ['bectmp', 'release', '.git'] # [TEMP FOLDER, ARCIVE FOLDER, GIT]
IGNORE_FILES = [CONFIG_FILE, '.gitignore']
PARENT_DIRECTORY = os.getcwd()
TEMP_DIRECTORY = os.path.join(PARENT_DIRECTORY, IGNORE_DIRS[0])
EXCLUDED = []  # (path, directory, file)

#### COMMAND LINE OPTIONS ####
@click.command()
@click.option('--overwrite', '-o', is_flag=True, help="Will overwrite if zip file for current version already exists.")


#### MAIN LOOP ####
def package(overwrite):
    filename = read_manifest_file()
    if filename is not None:
        read_ignore_file()
        create_temp_dir()
        filesystem_process()
        archive(filename, overwrite)
        remove_temp_dir()
    else:
        pass


#### FILE SYSTEM OPERATIONS ####

# Walk through the subdirectories and recreate files and directories in IGNORE_DIRS[0] folder,
# will ignore any files or directories in EXCLUDED, IGNOREDIRS, AND IGNOREFILES.
def filesystem_process():
    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        files[:] = [f for f in files if f not in IGNORE_FILES]
        path = read_path(root)
        if path == "":
            path = None
        remove_ignored_files(path, files)
        remove_ignored_directories(path, dirs)
        create_directories(path, dirs)
        copy_files(path, files)


def remove_ignored_directories(path, directory_list):
    for item in EXCLUDED:
        if item[0] == path and item[1] is not None:
            directory_list.remove(item[1])

    return directory_list


def remove_ignored_files(path, file_list):
    for item in EXCLUDED:
        if item[0] is None and str(item[2]).find("*") != -1:
            ignore_files = str(item[2]).split(".")
            for file in reversed(file_list):
                extension = file.split(".")
                if extension[1] == ignore_files[1]:
                    file_list.remove(file)
        elif str(item[2]).find("!") != -1:
            file = str(item[2]).split("!")
            if path is not None:
                keep_file = os.path.join(PARENT_DIRECTORY, path, file[1])
            else:
                keep_file = os.path.join(PARENT_DIRECTORY, file[1])

            if os.path.isfile(keep_file) and file_list.count(file[1]) == 0:
                file_list.append(file[1])
        elif item[0] is None and item[2] is not None:
            try:
                file_list.remove(item[2])
            except:
                pass
        elif item[0] == path and item[2] is not None:
            file_list.remove(item[2])
    return file_list


def copy_files(path, file_list):
    for file in file_list:
        if path is not None:
            src_file = os.path.join(PARENT_DIRECTORY, path, file)
            dest_file = os.path.join(TEMP_DIRECTORY, path, file)
        else:
            src_file = os.path.join(PARENT_DIRECTORY, file)
            dest_file = os.path.join(TEMP_DIRECTORY, file)

        shutil.copyfile(src_file, dest_file)


def create_directories(path, directory_list):
    for dir in directory_list:
        if path is not None:
            new_dir = os.path.join(TEMP_DIRECTORY, path, dir)
            os.mkdir(new_dir)
        else:
            new_dir = os.path.join(TEMP_DIRECTORY, dir)
            os.mkdir(new_dir)


def archive(archive_name, overwrite):
    os.chdir(TEMP_DIRECTORY)
    output_directory = os.path.join(PARENT_DIRECTORY, IGNORE_DIRS[1])
    if os.path.isdir(output_directory):
        pass
    else:
        os.mkdir(output_directory)

    output_file = os.path.join(output_directory, archive_name)

    if overwrite:
        shutil.make_archive(output_file, 'zip', TEMP_DIRECTORY)
    else:
        if os.path.isfile(output_file+'.zip'):
            click.echo("An archive file already exists for: \"" +
                       archive_name + '.zip\"')
            if click.confirm("Would you like to continue?: "):
                click.echo("Overwriting existing archive...")
                shutil.make_archive(output_file, 'zip', TEMP_DIRECTORY)
            else:
                pass
        else:
            shutil.make_archive(output_file, 'zip', TEMP_DIRECTORY)

    os.chdir(PARENT_DIRECTORY)


#### UTILITY FUNCTIONS ####

def read_ignore_file():
    with open(CONFIG_FILE, 'r') as file:
        lines = file.readlines()

    lines.sort(reverse=True)
    for line in lines:
        if line.find('/') != -1:
            seperator = '/'
        elif line.find('\\') != -1:
            seperator = '\\'
        else:
            seperator = None

        if seperator is not None:
            new_line = line.strip().rsplit(seperator)
            if len(new_line) == 2:
                if new_line[1] == "":
                    EXCLUDED.append(tuple([None, new_line[0], None]))
                else:
                    EXCLUDED.append(tuple([new_line[0], None, new_line[1]]))
            else:
                EXCLUDED.append(tuple([new_line[0], new_line[1], None]))
        else:
            EXCLUDED.append(tuple([None, None, line.strip()]))
    file.close()


def read_manifest_file():
    if os.path.isfile('manifest.json'):
        with open('manifest.json', 'r') as file:
            data = file.read()

        item = json.loads(data)
        export = str(item['name']) + "-" + str(item['version'])
        return export
    else:
        click.echo("Exiting script, no manifest file found.")
        return None


def create_temp_dir():
    remove_temp_dir()
    os.mkdir(TEMP_DIRECTORY)


def remove_temp_dir():
    if os.path.isdir(TEMP_DIRECTORY):
        shutil.rmtree(TEMP_DIRECTORY)


def read_path(root):
    len_par = len(str(PARENT_DIRECTORY))
    return root[len_par + 1:]


#### RUN SCRIPT ####

if __name__ == '__main__':
    package()
