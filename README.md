# Browser Extension Quick Archiver
*BEQA* or *Becca*

A command line tool to quickly archive brower extensions into a .zip file for distribution.

Becca includes functionality to ignore any file in your extensions directory with the ".becignore" file
```
ignorethisfile.txt # this file will be ignored in every directory
lol/pleaseignoreme.txt # this file will only be ignored in the lol directory
notme/ # this directory will be ignored from the project root directory
lol/ignorethisfolder/ # lol will not be ignored but ignorethisfolder will
```

Functions:
 - [x] Read a config file for files to ignore.
 - [x] Read manifest.json for extesion name & version.
 - [x] Warn user if a (.zip/version) exists and ask if they would like to overwrite it.
 - [x] Have a tag to allow overwrite without a promt.
 - [x] Directory must have a manifest file to run.
 - [ ] Add *.extension ignore capability