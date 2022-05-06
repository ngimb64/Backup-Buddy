# Backup Buddy
![alt text](https://github.com/ngimb64/Backup-Buddy/blob/main/BackupBuddy.png?raw=true)

## Prereqs
> This program runs on Windows & Linux, written in Python 3.9

## Installation
- Run the setup.py script to build a virtual environment and install all external packages in the created venv.

> Example:<br>
> python3 setup.py "venv name"

- Once virtual env is built traverse to the Scripts directory in the environment folder just created.
- In the Scripts directory, execute the "activate" script to activate the virtual environment.

## Purpose
> This shell tool makes keeping an updated backup of different systems a breeze.
> It takes a source & destination path to then either copy or update data.
> If the data doesn't exist it is automatically copied.
> If the data already exist the source & destination files last modified timestamps are compared.
> If the source file has a more recent last modified timestamp, the destination is updated accordingly.
> There are also built in srcDoc/destDock directories that can be utilized by simply hitting enter then providing an absolute path.

## How to use
- Open up shell such as command prompt or terminal
- Enter directory containing program and execute in shell
- Enter the absolute path of the source & destination directories to copy/update data either in a single directory or recursively
- OR if you would like to exit hit Ctrl + C (KeyboardInterrupt)