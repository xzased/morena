#!/bin/bash

if [ "$1" == "--help" ]; then
    echo
    echo "Available options:"
    echo
    echo "    init-db"
    echo "        Initializes db data."
    echo
    exit 1
fi
INIT=$1

### FIX ME: Add logic here to automatically check (needs to support Fedora
### Debian, Ubuntu, CentOS, Red Hat).

echo $@ | grep -- "--noprompt" 2>&1 >/dev/null
if [ "$?" != 0 ]; then
    echo
    echo "Required System Packages:"
    echo
    echo "    mongodb (and running)"
    echo
    echo -n "Is it installed? [y|N] "
    read res

    if [ "$res" != "y" ]; then
        exit 1
    fi
    echo "Seems we got a badass over here  . . . "
fi

if [ -z "$VIRTUAL_ENV" ]; then
    echo "Not running in a virtualenv??? Well fuck you too."
    exit 1
fi

pip install -r requirements.txt -I --upgrade
python setup.py develop


if [ "$INIT" == "init-db" ]; then
    # initialize basic db data
    python utils/init-data.py
fi