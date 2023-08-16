#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause
# 
# EUCLID App
# ----------
# Designed to update EUCLID 
# Fabric Mods and kube.js files, etc.
#
# BSD 3-Clause License
# 
# Copyright (c) 2023, Krafter
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from logging42 import logger
from typing import Optional
import urllib.request
import tempfile
import zipfile
import dulwich
import tkinter
import shutil
import yaml
import sys
import os

DEFAULT_GIT_URL = 'https://github.com/TheKrafter/EUCLIDApp.git'
DEFAULT_GIT_BRANCH = 'source'
DEFAULT_MINECRAFT_SUBDIRECTORY = '.euclidminecraft/'
CONFIG_FILE_NAME = 'euclid-git.cfg'

class NoMinecraftFolder(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def locate_config() -> str:
    """ Find the Path to the EUCLID config file """
    if sys.platform == 'linux' or sys.platform == 'linux2':
        logger.debug('Detected Linux.')
        config_path = f'{os.environ("HOME")}/.config/euclid/'
        data_dir = f'{os.environ("HOME")}/.local/var/euclid/'
    elif sys.platform == 'darwin':
        logger.debug('Detected Darwin.')
        config_path = f'{os.environ("HOME")}/Library/Application Support/EUCLID/'
        data_dir = config_path
    elif sys.platform == 'win32':
        logger.debug('Detected Windows.')
        config_path = f'{os.getenv("APPDATA")}/EUCLID/'
        data_dir = config_path
    else:
        logger.critical(f'Platform "{sys.platform}" not supported!')
        logger.info('Please contribute for your platform at https://github.com/TheKrafter/EUCLIDApp')
        raise NotImplementedError
    
    if not os.path.exists(config_path):
        os.mkdir(config_path)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    
    if not os.path.exists(config_path + CONFIG_FILE_NAME):
        config = {
            'git_url': DEFAULT_GIT_URL,
            'git_branch': DEFAULT_GIT_BRANCH,
            'mc_default_dir': data_dir + DEFAULT_MINECRAFT_SUBDIRECTORY,
            'mc_current_dir': data_dir + DEFAULT_MINECRAFT_SUBDIRECTORY,
        }
        with open(config_path + CONFIG_FILE_NAME, 'w') as file:
            yaml.dump_all(config, file)
    
    with open(config_path + CONFIG_FILE_NAME, 'r') as file:
        cfg = yaml.load_all(file)
    
    logger.debug('Loaded config file successfully!')
    return cfg
