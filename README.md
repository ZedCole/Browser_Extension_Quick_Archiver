# Browser Extension Quick Archiver
*BEQA* or *Becca*

A command line tool to quickly archive brower extensions into a .zip file for distribution.

Becca includes functionality to ignore any file in your extensions directory with the ".becignore" file
```python
ignorethisfile.txt #this file will be ignored in every directory
lol/pleaseignoreme.txt #this file will only be ignored in the lol directory
notme/ #this directory will be ignored from the projects root directory
lol/ignorethisfolder/ #lol will not be ignored but ignorethisfolder will
```

Todo:
 - [ ] Add *.extension ignore capability
 - [ ] Release on github