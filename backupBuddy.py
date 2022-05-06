# Built-in Modules #
import logging
import os
import re
import shutil
import time
from datetime import datetime
from shlex import quote
from sys import stderr


##################
# Function Index #
########################################################################################################################
# CopyFile(src_file, dest_file) - Copies file in error validated wrapper.
# FileHandler(src_file, dest_file) - If file exists check if the source file has a more recent time stamp than the \
#                                    destination file, if so copy the file. If the file does not exist, simply copy \
#                                    the file.
# DirHandler(dir_path) - Confirms the directory of the destination path exists. If not, the directory is created to \
#                        prevent errors.
# main(cmd) - Gathers users input and executes file copy operations based on the source and destination path provided.
########################################################################################################################


# Globals #
# Returns time of last modification #
def TimeCheck(filename: str) -> int: return datetime.fromtimestamp(os.stat(filename).st_mtime)
# Check if file exists #
def FileCheck(filename: str) -> bool: return os.path.isfile(filename)
# Check if directory exists #
def DirCheck(dirname: str) -> bool: return os.path.isdir(dirname)
# Check if file has read access #
def AccessCheck(filename: str) -> bool: return os.access(filename, os.R_OK)


'''
########################################################################################################################
Name:    CopyFile
Purpose: Copies file in error validated wrapper.
Params:  The source file to be copied, and the dest file where the source file will be copied to.
Returns: None
########################################################################################################################
'''
def CopyFile(src_file: str, dest_file: str):
    try:
        # Copy file from source to destination #
        shutil.copy(src_file, dest_file)

    # Catches input/output error or if the source and dest file are the same #
    except (IOError, shutil.SameFileError) as copy_err:
        if IOError:
            logging.exception(f'* Error occurred copying file: {copy_err} *\n\n')


'''
########################################################################################################################
Name:    FileHandler
Purpose: If file exists check if the source file has a more recent time stamp than the destination file, if so copy \
         the file. If the file does not exist, simply copy the file.
Params:  The source file to be copied, and the dest file where the source file will be copied to.
Returns: None
########################################################################################################################
'''
def FileHandler(src_file: str, dest_file: str):
    # If the file exists #
    if FileCheck(dest_file):
        # If the source file has a newer timestamp than the dest file #
        if TimeCheck(src_file) > TimeCheck(dest_file):
            # Copy the source file to the destination #
            CopyFile(src_file, dest_file)
            print(f'File Updated: {dest_file}')
    else:
        # Copy the source file to the destination #
        CopyFile(src_file, dest_file)
        print(f'File Copied: {dest_file}')


'''
########################################################################################################################
Name:    DirHandler
Purpose: Confirms the directory of the destination path exists. If not, the directory is created to prevent errors.
Params:  The path to the directory to check.
Returns: None
########################################################################################################################
'''
def DirHandler(dir_path: str):
    # If the directory does not exist #
    if not DirCheck(dir_path):
        try:
            # Create the missing directory #
            os.makedirs(dir_path, exist_ok=True)
            print(f'Directory Copied: {dir_path}')

        # If directory already exists #
        except OSError:
            pass


'''
########################################################################################################################
Name:    PrintErr
Purpose: Prints time controlled error message.
Params:  The error message to be printed and the number of seconds it should be displayed before clearing the screen.
Returns: Exits program when Ctrl+C is pressed.
########################################################################################################################
'''
def PrintErr(msg: str, seconds: int):
    print(f'\n* [ERROR]: {msg} *\n', file=stderr)
    time.sleep(seconds)


'''
########################################################################################################################
Name:    main
Purpose: Gathers users input and executes file copy operations based on the source and destination path provided.
Params:  None
Returns: None
########################################################################################################################
'''
def main():
    # Initiate command syntax in immutable tuple #
    cmds = ('cls', 'clear')

    # If OS is Windows #
    if os.name == 'nt':
        # Shell-escape command syntax #
        cmd = quote(cmds[0])
        # Compile the path matching regex #
        reg_path = re.compile(r'^[A-Z]:(?:\\[a-zA-Z0-9_"\' .,\-]{1,25})+')
    # If OS is Linux #
    else:
        # Shell-escape command syntax #
        cmd = quote(cmds[1])
        # Compile the path matching regex #
        reg_path = re.compile(r'^(?:\\[a-zA-Z0-9_"\' .,\-]{1,25})+')

    while True:
        # Clear the display per iteration #
        os.system(cmd)

        # Prompt user for destination & source paths for backups #
        src_path = input('C:\\enter\\Windows\\path OR \\enter\\Linux\\path OR hit enter to use srcDock:\n')
        dest_path = input('\nC:\\enter\\Windows\\path OR \\enter\\Linux\\path OR hit enter to use destDock:\n')

        # Validates input to either match the regex or detect enter fo default dir #
        if (not re.search(reg_path, src_path) and src_path != '') or \
        (not re.search(reg_path, dest_path) and dest_path != ''):
            PrintErr('Improper format provided .. try again', 2)
            continue

        # If default source path detected #
        if src_path == '':
            src_path = '.\\srcDock'

        # If default destination path detected #
        if dest_path == '':
            dest_path = '.\\destDock'

        break

    # Prompt user for singular or recursive data copying #
    while True:
        prompt = input('\nSearch through folders in path recursively or single directory (r or s): ')
        # If input is not one of the two options #
        if prompt not in ('r', 's'):
            PrintErr('Improper format provided .. try again', 2)
            continue

        break

    print(f'\n\n{19 * "*"} Starting copy {51 * "*"}')

    # If recursive copying is selected #
    if prompt == 'r':
        # Grab only the rightmost directory of path save result in other regex 
        # as anchor point for confirming recursive directories while crawling #
        reg_pathEdge = re.search(r'[^\\]+$', src_path)
        # Insert path edge regex match into regex to match any path past the edge anchor point #
        reg_extPath = re.compile(r'(?<={0}\\).+$'.format(str(reg_pathEdge.group(0))))

        # Recursively walk through the file system of the source path #
        for dir_path, dir_names, file_names in os.walk(src_path):
            # Attempt to match recursive path extending beyond base dir #
            match = re.search(reg_extPath, dir_path)
            # If match is successful #
            if match:
                # save the match as string #
                recursive_path = str(match.group(0))
            else:
                recursive_path = None

            print(f'\nIn path: {dir_path}\n' + ((9 + len(dir_path)) * '*'))

            # Iterate through the directories #
            for dir_name in dir_names:
                # If regex failed (base path passed in) #
                if not recursive_path:
                    DirHandler(f'{dest_path}\\{dir_name}')
                # If the path is part of recursive structure #
                else:
                    DirHandler(f'{dest_path}\\{recursive_path}\\{dir_name}')

            # Iterate through files #
            for file in file_names:
                # If regex failed (base path passed in) #
                if not recursive_path:
                    # Call the function to handle file copying #
                    FileHandler(f'{dir_path}\\{file}', f'{dest_path}\\{file}')
                # If the path is part of recursive structure #
                else:
                    # Call the function to handle file copying #
                    FileHandler(f'{dir_path}\\{file}', f'{dest_path}\\{recursive_path}\\{file}')

    # If single directory copying is selected #
    else:
        # If the source path exists #
        if DirCheck(src_path):
            # Iterate through directory source directory #
            for file in os.listdir(src_path):
                # If the iteration is not a dir #
                if not DirCheck(f'{src_path}\\{file}'):
                    # Call the function to handle file copying #
                    FileHandler(f'{src_path}\\{file}', f'{dest_path}\\{file}')

    print(f'\n\n{18 * "*"} All finished!!! {50 * "*"}\n\n')


if __name__ == '__main__':
    # Set the log file name #
    logging.basicConfig(level=logging.DEBUG, filename='.\\CopyLog.log')

    # Set the included dock paths #
    src_dir = '.\\srcDock'
    dest_dir = '.\\destDock'

    # If the source dir does not exist #
    if not DirCheck(src_dir):
        # Create the missing dir #
        os.mkdir('.\\srcDock')

    # If the dest dir does not exist #
    if not DirCheck(dest_dir):
        # Create the missing dir #
        os.mkdir('.\\destDock')

    try:
        main()

    except KeyboardInterrupt:
        print('\n* Ctrl + C detected .. exiting *')
    except Exception as err:
        print('\n* [ERROR] exception occurred .. exiting, check log *')
        logging.exception(f'* Error Occurred: {err} *')
