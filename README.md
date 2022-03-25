# Backup Buddy
![alt text](https://github.com/ngimb64/Backup-Buddy/blob/main/BackupBuddy.png?raw=true)

## Prereqs
> This program runs on Windows & Linux, written in Python 3.9
> It uses only built-modules, so it should be ready to run right out of the package.

## Purpose
> This shell tool makes keeping an updated backup of different systems a breeze.
> It takes a source & destination path to then either copy or update data.
> If the data doesn't exist it is automatically copied.
> If the data already exist the source & destination files last modified timestamps are compared.
> If the source file has a more recent last modified timestamp, the destination is updated accordingly.
> There are also built in srcDoc/destDock directories that can be utilized by simply hitting enter then providing an absolute path.