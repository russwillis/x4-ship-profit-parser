# x4-ship-profit-parser
A small program to get the gzipped save file from X4 and extract just the mining and trading logs and spit out a csv the other end


# How to use

*Update*: Added x4-parser.exe - this should be an all in one package. You only need to download and run this one file.
Also added an .app file for mac but that shows as a folder in github... no idea why

Works on Windows 10 - not tested on any other system

* Needs Python installed (https://www.python.org/downloads/)

* Needs command line access (I use git-bash - https://github.com/git-for-windows/git/releases/tag/v2.20.1.windows.1)

* navigate to the directory where you've place the x4_parser.py file

* run this command : `python x4_parser.py`

* you'll have a (very) basic UI. Click the browse button, it'll take you to your save file location. Select your user id folder then the save file you wish to extract.

* Click generate csv button. After a slight pause of around 20 seconds (these save files are enormous!) you'll have a new csv file called `extracted_logs.csv`

* I personally like importing this file into google sheets as data, then generating a chart from it making sure to collate the ship names so that all their trades are on one line.


# future wishlist (will probably never happen)

* create a chart similar to the one google sheets does in the x4_parser app itself.

* add switches to reorder data

* ~~make this a standalone .exe so save people from messing aroound installing python and whatnot~~
