#!/bin/bash
mod_loc="$(python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])')"
filename="getStockDividends.zip"
cd $mod_loc && zip -r $filename .
cd ${OLDPWD}
mv $mod_loc/$filename .
zip -g $filename div_history.py
