#!/usr/bin/bash

echo "
============ AltruZ ============
Copyright (c) 2021 TeamAltruZ | @TheAltruZ 

- Running Pyrogram!
- Installing AltruZ
- Done!
- Running AltruZ
- Starting AltruZ on your Telegram!
================================
"

start_altruz () {
    if [[ -z "$PYRO_STR_SESSION" ]]
    then
	    echo "Please add Pyrogram String Session"
    else
	    python3 -m altruz
    fi
  }

_install_altruz () {
    start_altruz
  }

_install_altruz
