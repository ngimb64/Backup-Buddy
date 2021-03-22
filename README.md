## Prereqs
> This program was written on Python 3.9, but should work on most versions of 3. 
> This project has many modules incorporated, some of which are not included by default.
> Any missing modules have to be installed with PIP before the program can run. I recommend simply looking up the module name and finding the documentation. 
> The PIP command for installation is usually one of the first things mentioned.
> Also with Python it is common to have multiple modules with a similar names.
> So if errors are being raised about not having a certain module; it is most likely the wrong module with a similar name to the one that is required was installed instead of the required module.

## Installation
- Look up python in search engine
- Make sure any external modules are installed
- Open up command prompt, traverse to program directory, & execute

## Purpose
> This tool makes keeping an updated backup of different systems a breeze.
> It takes a source & destination path to then either copy or update data.
> If the data doesn't exist it is automatically copied.
> If the data already exist the source & destination files last modified timestamps are compared.
> If the the source file has a more recent last modified timestamp .. the destination is updated accordingly.
> There are also built in srcDoc/destDock  directories that can be utilized by simply hitting enter then providing an absolute path.