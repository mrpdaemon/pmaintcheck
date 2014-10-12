pmaintcheck
===========

pmaintcheck is a tool for distribution package maintainers to automatically
watch packages that they maintain to see if a new version has been released or
not. It is built in a modular way allowing for plugins to be written for all
kinds of upstream hosting mechanisms.

## Usage

pmaintcheck can be used by simply invoking

    ./pmaintcheck.py

which will read the `example.cfg` config file. The user can add/remove packages
to that file to watch more/less packages.
