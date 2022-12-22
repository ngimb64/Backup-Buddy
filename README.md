# Backup Buddy
![alt text](https://github.com/ngimb64/Backup-Buddy/blob/main/BackupBuddy.gif?raw=true)
![alt text](https://github.com/ngimb64/Backup-Buddy/blob/main/BackupBuddy.png?raw=true)

&#9745;&#65039; Bandit verified<br>
&#9745;&#65039; Synk verified<br>
&#9745;&#65039; Pylint verified 9.93/10

## Prereqs
This program runs on Windows 10 & Debian-based Linux, written in Python 3.9 and updated to version 3.10.6

## Purpose
This tool takes a source & destination path to then either copy or update data.
If the data doesn't exist it is automatically copied.
If the data already exist the source & destination files last modified timestamps are compared.
If the source file has a more recent last modified timestamp, the destination is updated accordingly.
There are also built in srcDoc/destDock directories that can be utilized by simply hitting enter then providing an absolute path.

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Examples:<br> 
>       &emsp;&emsp;- Windows:  `python setup.py venv`<br>
>       &emsp;&emsp;- Linux:  `python3 setup.py venv`

- Once virtual env is built traverse to the (Scripts-Windows or bin-Linux) directory in the environment folder just created.
- For Windows, in the venv\Scripts directory, execute `activate` or `activate.bat` script to activate the virtual environment.
- For Linux, in the venv/bin directory, execute `source activate` to activate the virtual environment.
- If for some reason issues are experienced with the setup script, the alternative is to manually create an environment, activate it, then run pip install -r packages.txt in project root.
- To exit from the virtual environment when finished, execute `deactivate`.

## How to use
- Open up shell such as command prompt or terminal
- Enter directory containing program and execute in shell
- Enter the absolute path of the source & destination directories to copy/update data either in a single directory or recursively
- OR if you would like to exit hit Ctrl + C

## Function Layout
-- backup_buddy.py --
> copy_file &nbsp;-&nbsp; Copies file in error validated wrapper.

> copy_handler &nbsp;-&nbsp; If file exists check if the source file has a more recent time stamp 
> than the destination file, if so copy the file. If the file does not exist, simply copy the file.

> dir_copy &nbsp;-&nbsp; Confirms the directory of the destination path exists. If not, the 
> directory is created to prevent errors.

> print_err &nbsp;-&nbsp; Prints time controlled error message via stderr.

> file_handler &nbsp;-&nbsp; Handles the file copy whether it is the base path or a folder in the 
> recursive path.

> dir_handler &nbsp;-&nbsp; Handles the directory copy whether it is the base path or a folder in
> the recursive path.

> single_mode &nbsp;-&nbsp; Copies contents of source path to dest path in non-recursive manner.

> mode_input &nbsp;-&nbsp; Prompt user whether they want to recursively copy or just a single 
> directory.

> path_input &nbsp;-&nbsp; Gets the source path where to the data is to be copied from and the 
> destination path where the data is to be copied to.

> main &nbsp;-&nbsp; Gathers users input and executes file copy operations based on the source and 
> destination path provided.

## Exit Codes
> 0 - Successful operation<br>
> 1 - Unexpected error occurred