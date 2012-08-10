#!/usr/bin/env python
# encoding: utf-8
"""
run.py

Created by Jerome Yang on 2012-04-06.
Copyright (c) 2012 MMH & NCKU. All rights reserved.
"""

import os
import sqlite3 as lite
import report_classify.settings


def components_check():
    status_file = open(STATUS_FILE, 'rw')
    
    # Get all modules in the modules folder
    module_groups = [name for name in os.listdir(MODULE_FOLDER) if os.path.isdir(os.path.join(MODULE_FOLDER, name))]
    module_table = dict()
    for module_group in module_groups:
        module_table[module_group] = os.listdir(MODULE_FOLDER, module_group)
        
         
    
    status_file.close()
    for checkpoint in checkpoints:
        if current[checkpoint] != status[checkpoint]:
            flags[checkpoint] = True


def main():
	components_check()

if __name__ == '__main__':
	main()

