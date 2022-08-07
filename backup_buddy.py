""" Built-in modules """
import logging
import os
import re
import shutil
import sys
import time
from datetime import datetime
from sys import stderr


def time_check(filename: str):
    """
    Returns time of last modification.

    :param filename:  The file name to check time of last modification.
    :return:  Time of last file modification.
    """
    return datetime.fromtimestamp(os.stat(filename).st_mtime)


def file_check(filename: str) -> bool:
    """
    Checks is file exists.

    :param filename:  The name of the file to check if exists.
    :return:  True/False whether file exists/not-exists.
    """
    return os.path.isfile(filename)


def dir_check(dirname: str) -> bool:
    """
    Check if directory exists.

    :param dirname:  The name of the directory to check if exists.
    :return:  True/False whether directory exists/not-exists.
    """
    return os.path.isdir(dirname)


def copy_file(src_file: str, dest_file: str):
    """
    Copies file in error validated wrapper.

    :param src_file:  The source file to be copied.
    :param dest_file:  The dest file where the source file will be copied to.
    :return:  Nothing
    """
    try:
        # Copy file from source to destination #
        shutil.copy(src_file, dest_file)

    # If unexpected same file error occurs #
    except shutil.SameFileError:
        pass

    # Catches input/output error or if the source and dest file are the same #
    except IOError as copy_err:
        logging.exception('Error occurred copying file: %s\n\n', copy_err)


def copy_handler(src_file: str, dest_file: str):
    """
    If file exists check if the source file has a more recent time stamp than the destination \
    file, if so copy the file. If the file does not exist, simply copy the file.

    :param src_file:  The source file to be copied.
    :param dest_file:  The dest file where the source file will be copied to.
    :return:  Nothing
    """
    # If the file exists #
    if file_check(dest_file):
        # If the source file has a newer timestamp than the dest file #
        if time_check(src_file) > time_check(dest_file):
            # Copy the source file to the destination #
            copy_file(src_file, dest_file)
            print(f'File Updated: {dest_file}')
    # If the file does not exist #
    else:
        # Copy the source file to the destination #
        copy_file(src_file, dest_file)
        print(f'File Copied: {dest_file}')


def dir_copy(dir_path: str):
    """
    Confirms the directory of the destination path exists. If not, the directory is created to \
    prevent errors.

    :param dir_path:  The path to the directory to check.
    :return:  Nothing
    """
    # If the directory does not exist #
    if not dir_check(dir_path):
        try:
            # Create the missing directory #
            os.makedirs(dir_path, exist_ok=True)
            print(f'Directory Copied: {dir_path}')

        # If directory already exists #
        except OSError:
            pass


def print_err(msg: str, seconds: int):
    """
   Prints time controlled error message via stderr.

    :param msg:  The message to be displayed.
    :param seconds:  The time interval in seconds the message will be displayed.
    :return:  Nothing
    """
    print(f'\n* [ERROR]: {msg} *\n', file=stderr)
    time.sleep(seconds)


def file_handler(ext_path: str, folder: str, dst_path: str, filename: str):
    """
    Handles the file copy whether it is the base path or a folder in the recursive path.

    :param ext_path:  Recursive path, if exists.
    :param folder:  The name of the folder where the file is stored.
    :param dst_path:  The destination path where the directory is to be created.
    :param filename:  The name of the file to be copied.
    :return:
    """
    # If regex failed (base path passed in) #
    if not ext_path:
        # If the OS is Windows #
        if os.name == 'nt':
            src_file = f'{folder}\\{filename}'
            dest_file = f'{dst_path}\\{filename}'
        # If the OS is Linux #
        else:
            src_file = f'{folder}/{filename}'
            dest_file = f'{dst_path}/{filename}'

        # Call the function to handle file copying #
        copy_handler(src_file, dest_file)
    # If the path is part of recursive structure #
    else:
        # If the OS is Windows #
        if os.name == 'nt':
            src_file = f'{folder}\\{filename}'
            dest_file = f'{dst_path}\\{ext_path}\\{filename}'
        # If the OS is Linux #
        else:
            src_file = f'{folder}/{filename}'
            dest_file = f'{dst_path}/{ext_path}/{filename}'

        # Call the function to handle file copying #
        copy_handler(src_file, dest_file)


def dir_handler(ext_path: str, dst_path: str, folder: str):
    """
    Handles the directory copy whether it is the base path or a folder in the recursive path.

    :param ext_path:  Recursive path, if exists.
    :param dst_path:  The destination path where the directory is to be created.
    :param folder:  The name of the directory to be created.
    :return:  Nothing
    """
    # If regex failed (base path passed in) #
    if not ext_path:
        # If the OS is Windows #
        if os.name == 'nt':
            dir_path = f'{dst_path}\\{folder}'
        # If the OS is Linux #
        else:
            dir_path = f'{dst_path}/{folder}'

        # Copy the directory #
        dir_copy(dir_path)

    # If the path is part of recursive structure #
    else:
        # If the OS is Windows #
        if os.name == 'nt':
            dir_path = f'{dst_path}\\{ext_path}\\{folder}'
        # If the OS is Linux #
        else:
            dir_path = f'{dst_path}/{ext_path}/{folder}'

        # Copy the directory #
        dir_copy(dir_path)


def single_mode(src_path: str, dest_path: str):
    """
    Copies contents of source path to dest path in non-recursive manner.

    :param src_path:  The path to the source directory containing data.
    :param dest_path:  The path to the destination directory where the data will go.
    :return:  Nothing
    """
    # Iterate through directory source directory #
    for file in os.scandir(src_path):
        # If the OS is Windows #
        if os.name == 'nt':
            src_file = f'{src_path}\\{file.name}'
            dest_file = f'{dest_path}\\{file.name}'
        # If the OS is Linux #
        else:
            src_file = f'{src_path}/{file.name}'
            dest_file = f'{dest_path}/{file.name}'

        # If the iteration is not a dir #
        if not dir_check(src_file):
            # Call the function to handle file copying #
            copy_handler(src_file, dest_file)


def mode_input() -> str:
    """
    Prompt user whether they want to recursively copy or just a single directory.

    :return:  The copy mode selected by the user.
    """
    while True:
        prompt = input('\nSearch through folders in path recursively or'
                       ' single directory (r or s): ')
        # If input is not one of the two options #
        if prompt not in ('r', 's'):
            print_err('Improper format provided .. try again', 2)
            continue

        break

    return prompt


def path_input(cmd: str, reg_path) -> tuple:
    """
    Gets the source path where to the data is to be copied from and the destination path where the \
    data is to be copied to.

    :param cmd:  Clear display command syntax.
    :param reg_path:  The compiled regex for path matching.
    :return:  The input source and destination path.
    """
    while True:
        # Clear the display per iteration #
        os.system(cmd)

        # Prompt user for destination & source paths for backups #
        src_path = input('C:\\enter\\Windows\\path OR /enter/Linux/path OR'
                         ' hit enter to use srcDock:\n')
        dest_path = input('\nC:\\enter\\Windows\\path OR /enter/Linux/path OR'
                          ' hit enter to use destDock:\n')

        # Validates input to either match the regex or detect enter to default dir #
        if (not re.search(reg_path, src_path) and src_path != '') or \
        (not re.search(reg_path, dest_path) and dest_path != ''):
            print_err('Improper format provided .. try again', 2)
            continue

        # If the source directory does not exist #
        if not dir_check(src_path):
            print_err('source path does not exist, try again', 2)
            continue

        # If default source path detected #
        if src_path == '':
            src_path = src_dir

        # If default destination path detected #
        if dest_path == '':
            dest_path = dest_dir

        break

    return src_path, dest_path


def main():
    """
    Gathers users input and executes file copy operations based on the source and destination path \
    provided.

    :return:  Nothing
    """
    # Initiate command syntax in immutable tuple #
    cmds = ('cls', 'clear')

    # If OS is Windows #
    if os.name == 'nt':
        # Shell-escape command syntax #
        cmd = cmds[0]
        # Compile the path matching regex #
        reg_path = re.compile(r'[^<>\"/|?*]{1,255}[a-z]$')
    # If OS is Linux #
    else:
        # Shell-escape command syntax #
        cmd = cmds[1]
        # Compile the path matching regex #
        reg_path = re.compile(r'[^\\<>|?*]{1,255}[a-z]$')

    # Prompt the user for the source and destination path #
    src_path, dest_path = path_input(cmd, reg_path)
    # Prompt user for singular or recursive data copying #
    prompt = mode_input()

    print(f'\n\n{19 * "*"} Starting copy {51 * "*"}')

    # If recursive copying is selected #
    if prompt == 'r':
        # Grab only the rightmost directory of path save result in other regex
        # as anchor point for confirming recursive directories while crawling #
        if os.name == 'nt':
            re_edge_path = re.search(r'[^\\]{1,255}$', src_path)
            # Insert path edge regex match into regex to match any path past the edge anchor point #
            re_ext_path = re.compile(rf'(?<={re.escape(str(re_edge_path.group(0)))}\\).+$')
        else:
            re_edge_path = re.search(r'[^/]{1,255}$', src_path)
            # Insert path edge regex match into regex to match any path past the edge anchor point #
            re_ext_path = re.compile(rf'(?<={re.escape(str(re_edge_path.group(0)))}/).+$')

        # Recursively walk through the file system of the source path #
        for dir_path, dir_names, file_names in os.walk(src_path):
            # Attempt to match recursive path extending beyond base dir #
            match = re.search(re_ext_path, dir_path)
            # If match is successful #
            if match:
                # save the match as string #
                recursive_path = str(match.group(0))
            else:
                recursive_path = None

            print(f'\nIn path: {dir_path}\n{(9 + len(dir_path)) * "*"}')

            # Iterate through the directories #
            for dir_name in dir_names:
                # Call handler function to check if folder needs to be copied #
                dir_handler(recursive_path, dest_path, dir_name)

            # Iterate through files #
            for file in file_names:
                # Call handler function to check if folder needs to be copied #
                file_handler(recursive_path, dir_path, dest_path, file)

    # If single directory copying is selected #
    else:
        # Copy source to destination directory in single mode #
        single_mode(src_path, dest_path)

    print(f'\n\n{18 * "*"} All finished!!! {50 * "*"}\n\n')


if __name__ == '__main__':
    # Get the current working directory #
    cwd = os.getcwd()

    # If the OS is Windows #
    if os.name == 'nt':
        path = f'{cwd}\\'
    # If the OS is Linux #
    else:
        path = f'{cwd}/'

    # Set the log file name #
    logging.basicConfig(level=logging.DEBUG, filename=f'{path}CopyLog.log')

    # Set the included dock paths #
    src_dir = f'{path}srcDock'
    dest_dir = f'{path}destDock'

    # If the source dir does not exist #
    if not dir_check(src_dir):
        # Create the missing dir #
        os.mkdir(src_dir)

    # If the dest dir does not exist #
    if not dir_check(dest_dir):
        # Create the missing dir #
        os.mkdir(dest_dir)

    try:
        main()

    # If Ctrl + c is detected #
    except KeyboardInterrupt:
        print('\n* Ctrl + C detected .. exiting *')

    # If unknown exception occurs #
    except Exception as err:
        print_err('Unexpected exception occurred .. exiting, check log', 2)
        logging.exception('Unexpected error Occurred: %s\n\n', err)
        sys.exit(1)

    sys.exit(0)
