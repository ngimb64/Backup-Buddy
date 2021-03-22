from shutil import copyfile
from time import sleep
from datetime import datetime
import os, re, shutil, logging

time_check = lambda file: datetime.fromtimestamp(os.stat(file).st_mtime) 

def copy_file(src_file, dest_file):
    try:
        shutil.copy(src_file, dest_file)
    except (IOError, shutil.SameFileError) as err:
        logging.exception('* Error occured copying file: {} *'.format(err))

def file_handler(src_file, dest_file):
    if os.path.isfile(dest_file) == True:
        src_check, dest_check = time_check(src_file), time_check(dest_file)
        if src_check > dest_check:
            copy_file(src_file, dest_file)
    else:
        copy_file(src_file, dest_file)

def dir_handler(dir_path):
    return dir_path if os.path.isdir(dir_path) == True else os.mkdir(dir_path)

def main():
    reg_path = re.compile(r'^C:(?:\\[A-Za-z0-9_]{1,25})+')
    while True: 
        os.system('cls')
        # Prompt user for destination & source paths for backups #
        src_path = input('C:\\Enter\\absolute\\path\\of\\source\\folder OR hit enter to use srcDock:\n')
        dest_path = input('\nC:\\Enter\\absolute\\path\\of\\destination\\folder OR hit enter to use destDock:\n')

        # Input validation #
        if (re.search(reg_path, src_path) == None and src_path != '') or \
        (re.search(reg_path, dest_path) == None and dest_path != ''):
            print('* Impromper format provided .. try again *')
            sleep(2)
            continue

        if src_path == '':
            src_path = '.\\srcDock'

        if dest_path == '':
            dest_path = '.\\destDock'

        break

    # Prompt user for singular or recursive data copying #
    while True:
        prompt = input('\nSearch through folders in path recursivly or single directory (r or s): ')
        if prompt not in ('r', 's'):
            print('* Impromper format provided .. try again *')
            sleep(2)
            continue

        break

    # If recursive copying is selected #
    if prompt == 'r':
        reg_pathEdge = re.search(r'\\[A-Za-z0-9_]+$', src_path)
        reg_extPath = re.compile(r'(?<={0}).+'.format('\\' + str(reg_pathEdge.group(0))))
        for dirpath, dirnames, filenames in os.walk(src_path): 
            extPath = re.search(reg_extPath, dirpath)
            for dirname in dirnames:
                if extPath == None:
                    dir_path = dest_path + '\\' + dirname
                    dir_handler(dir_path)
                else:
                    dir_path = dest_path + '\\' + str(extPath.group(0)) + '\\' + dirname
                    dir_handler(dir_path)

            for file in filenames:
                if extPath == None:
                    src_file = dirpath + '\\' + file
                    dest_file = dest_path + '\\' + file
                    file_handler(src_file, dest_file)
                else:
                    src_file = dirpath + '\\' + file
                    dest_file = dest_path + '\\' + str(extPath.group(0)) + '\\' + file
                    file_handler(src_file, dest_file)

    # If single directory copying is selected #
    elif prompt == 's':
        for file in os.listdir(src_path):
            src_file = src_path + '\\' + file
            dest_file = dest_path + '\\' + file
            if os.path.isdir(src_file) == True:
                pass
            else:
                file_handler(src_file, dest_file)

    # Catches any abnormal input #
    else:
        print('* Improper control formatting .. exiting *')
        sleep(2)
        exit(1)

    print('\nAll finished!')

if __name__ == '__main__':
    logging.basicConfig(filename='./log.txt')
    src_check = os.path.isdir('./srcDock')
    dest_check = os.path.isdir('./destDock')

    # If either data docks are missing #
    if src_check == False or dest_check == False:
        if src_check == False:
            os.mkdir('./srcDock')
            print('* Source directory dock missing .. now created easy reference * ')   
            sleep(2)
        
        if dest_check == False:
            os.mkdir('./destDock')
            print('* Destination directory dock missing .. now created for easy reference *')
            sleep(2)

    try:
        main()
    except KeyboardInterrupt:
        print('\n* Ctrl + C detected .. exiting *')
    except Exception as err:
        logging.exception('* Error Occured: {} *'.format(err))