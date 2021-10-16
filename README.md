# Extension Packager

Command line tool to pack Chome extensions into a .zip file for distribution.

Functions:
 - [x] Read a config file for files to ignore.
 - [x] Read manifest.json for extesion name & version.
 - [x] Warn user if a (.zip/version) exists and ask if they would like to overwrite it.
 - [x] Have a tag to allow overwrite without a promt.
 - [x] Directory must have a manifest file to run.
 - [ ] Add *.extension ignore capability