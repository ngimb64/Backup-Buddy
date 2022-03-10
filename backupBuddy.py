# Built-in Modules #
###############################
import os, re, shutil, logging
from datetime import datetime
from shlex import quote
from shutil import copyfile
from sys import stderr
from time import sleep

# Function Index
#################################################################################################
# CopyFile(src_file, dest_file) - Copies file in error validated wrapper.
# FileHandler(src_file, dest_file) - If file exists check if the source file has a more recent \
#                                    time stamp than the destination file, if so copy the file. \
#                                    If the file does not exist, simply copy the file.
# DirHandler(dir_path) - Confirms the directory of the destination path exists, if not .. the \
#                        directory is created to prevent errors.
# main(cmd) - Gathers users input and executes file copy operations based on the source and \
#             destination path provided.
#################################################################################################

# Globals #
#################################################################################################
TimeCheck = lambda filename: datetime.fromtimestamp(os.stat(filename).st_mtime)
FileCheck = lambda filename: os.path.isfile(filename)
DirCheck = lambda dirname: os.path.isdir(dirname)
AccessCheck = lambda filename: os.access(filename, os.R_OK)
#################################################################################################

'''
#################################################################################################
Name:    CopyFile
Purpose: Copies file in error validated wrapper.
Params:  The source file to be copied, and the dest file where the source \
         file will be copied to.
Returns: None
#################################################################################################
'''
def CopyFile(src_file, dest_file):
    try:
        # Copy file from source to destination #
        shutil.copy(src_file, dest_file)

    # Catches input/output error or if the source and dest file are the same #
    except (IOError, shutil.SameFileError) as err:
        logging.exception(f'* Error occured copying file: {err} *\n\n')

'''
#################################################################################################
Name:    FileHandler
Purpose: If file exists check if the source file has a more recent time \
         stamp than the destination file, if so copy the file. If the file \
         does not exist, simply copy the file.
Params:  The source file to be copied, and the dest file where the source \
         file will be copied to.
Returns: None
#################################################################################################
'''
def FileHandler(src_file, dest_file):
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
#################################################################################################
Name:    DirHandler
Purpose: Confirms the directory of the destination path exists, if not .. \
         the directory is created to prevent errors.
Params:  The path to the directory to check.
Returns: None
#################################################################################################
'''
def DirHandler(dir_path):
    # If the directory does not exist #
    if not DirCheck(dir_path):
        try:
            # Create the missing directory #
            os.makedirs(dir_path, exist_ok=True)
            print(f'Directory Copied: {dir_path}')

        # If directory already exists #
        except OSError as err:
            logging.exception(f'* Error occured making directory: {err} *\n\n')

'''
#################################################################################################
Name:    PrintErr
Purpose: Prints time controled error message.
Params:  The error message to be printed and the number of seconds \
         it should be displayed before clearing the screen.
Returns: Exits program when Ctrl+C is pressed.
#################################################################################################
'''
def PrintErr(msg, seconds):
    print(f'\n* [ERROR]: {msg} *\n', file=stderr)
    sleep(seconds)

'''
#################################################################################################
Name:    main
Purpose: Gathers users input and executes file copy operations based on \
         the source and destination path provided.
Params:  The command syntax to clear the screen based on OS.
Returns: None
#################################################################################################
'''
def main(cmd):
    # Compile the path matching regex #
    reg_path = re.compile(r'^C:(?:\\[a-zA-Z0-9_"\' \.,\-]{1,25})+')

    while True:
        # Clear the display per iteration #
        clear = os.system(cmd)

        # Prompt user for destination & source paths for backups #
        src_path = input('C:\\Enter\\absolute\\path\\of\\source\\folder OR hit enter to use srcDock:\n')
        dest_path = input('\nC:\\Enter\\absolute\\path\\of\\destination\\folder OR hit enter to use destDock:\n')

        # Validates input to either match the regex or detect enter fo default dir #
        if (not re.search(reg_path, src_path) and src_path != '') or \
        (not re.search(reg_path, dest_path) and dest_path != ''):
            PrintErr('Impromper format provided .. try again', 2)
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
        prompt = input('\nSearch through folders in path recursivly or single directory (r or s): ')
        # If input is not one of the two options @
        if prompt not in ('r', 's'):
            PrintErr('Impromper format provided .. try again', 2)
            continue

        break

    print('\n\n' + (19 * '*') + ' Starting copy ' + (51 * '*'))

    # If recursive copying is selected #
    if prompt == 'r':
        # Grab only the rightmost directory of path save result in other regex 
        # as anchor point for confirming rescursive directories while crawling #
        reg_pathEdge = re.search(r'[^\\]+$', src_path)
        # Insert path edge regex match into regex to match any path past the edge anchor point #
        reg_extPath = re.compile(r'(?<={0}\\).+$'.format(str(reg_pathEdge.group(0))))

        # Recursively walk through the file system of the source path #
        for dirpath, dirnames, filenames in os.walk(src_path):
            # Attempt to match recursive path extending beyond base dir #
            match = re.search(reg_extPath, dirpath)
            # If match is successfull #
            if match:
                # save the match as string #
                recursive_path = str(match.group(0))
            else:
                recursive_path = None

            print(f'\nIn path: {dirpath}\n' + ((9 + len(dirpath)) * '*') + '\n')

            # Iterate through the directories #
            for dirname in dirnames:
                # If regex failed (base path passed in) #
                if not recursive_path:
                    DirHandler(dest_path+'\\'+dirname)
                # If the path is part of recursive structure #
                else:
                    DirHandler(dest_path+'\\'+recursive_path+'\\'+dirname)

            # Iterate through files #
            for file in filenames:
                # If regex failed (base path passed in) #
                if not recursive_path:
                    # Call function to handle file copying #
                    FileHandler((dirpath+'\\'+file), (dest_path+'\\'+file))
                # If the path is part of recursive structure #
                else:
                    # Call function to handle file copying #
                    FileHandler((dirpath+'\\'+file), (dest_path+'\\'+recursive_path+'\\'+file))

    # If single directory copying is selected #
    else:
        # If the source path exists #
        if DirCheck(src_path):
            # Iterate through directory source directory #
            for file in os.listdir(src_path):
                # Call function to handle file copying #
                FileHandler((src_path+'\\'+file), (dest_path+'\\'+file))

    print('\n\n' + (18 * '*') + ' All finished!!! ' + (50 * '*') + '\n\n')


if __name__ == '__main__':
    # Set the log file name #
    logging.basicConfig(level=logging.DEBUG, filename='.\\CopyLog.log')

    # Clear display boolean switch #
    clear = False

    # Initiate command syntax in immutable tuple #
    cmds = ('cls', 'clear')

    # If the operating system is Windows #
    if os.name == 'nt':
        cmd = quote(cmds[0])
    else:
        cmd = quote(cmds[1])

    # Set the included dock paths #
    src_dir = '.\\srcDock'
    dest_dir = '.\\destDock'

    # If the source dir does not exist #
    if not DirCheck(src_dir):
        # Create the missing dir #
        os.mkdir('.\\srcDock')
        print('[INFO] Source directory dock missing .. now created easy reference\n') 
        clear = True

    # If the dest dir does not exist #
    if not DirCheck(dest_dir):
        # Create the missing dir #
        os.mkdir('.\\destDock')
        print('[INFO] Destination directory dock missing .. now created for easy reference\n')
        clear = True

    # If screen has info messages #
    if clear:
        # Sleep 3 seconds#
        sleep(2)
        # Clear display #
        os.system(cmd)

    try:
        main(cmd)

    # If ctrl + c is detected #
    except KeyboardInterrupt:
        print('\n* Ctrl + C detected .. exiting *')

    # If an unknown exception occurs #
    except Exception as err:
        print('\n* [ERROR] exception occured .. exiting, check log *')
        logging.exception(f'* Error Occured: {err} *')