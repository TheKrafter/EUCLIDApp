#!/usr/bin/env python3
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

from typing import Optional
import urllib.request
import tempfile
import zipfile
import tkinter
import shutil
import yaml
import sys
import os

DEFAULT_UPDATE_URL = 'https://raw.githubusercontent.com/TheKrafter/EUCLIDApp/main/example_remote_config.yml'
CONFIG_FILE_NAME = 'euclid.cfg'

class NoMinecraftFolder(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

def locate_config() -> str:
    """ Find the Path to the EUCLID config file """
    if sys.platform == 'linux' or sys.platform == 'linux2':
        config_path = f'{os.environ("HOME")}/.config/euclid/'
    elif sys.platform == 'darwin':
        config_path = f'{os.environ("HOME")}/Library/Application Support/EUCLID/'
    elif sys.platform == 'win32':
        config_path = f'{os.getenv("APPDATA")}/EUCLID/'
    else:
        raise NotImplementedError
    
    if not os.path.exists(config_path):
        os.mkdir(config_path)
    
    if not os.path.exists(config_path + CONFIG_FILE_NAME):
        config = {
            'update_url': DEFAULT_UPDATE_URL,
            'modules': {},
        }
        with open(config_path + CONFIG_FILE_NAME, 'w') as file:
            yaml.dump_all(config, file)
    
    with open(config_path + CONFIG_FILE_NAME, 'r') as file:
        cfg = yaml.load_all(file)
    
    return cfg

def get_remote_config(config: dict) -> dict:
    """ Get the remote config from the server's update url as configured in the config.
    Returns a dictionary of the loaded config """
    path = tempfile.gettempdir() + 'euclid_remote_config.yml'

    # Download and save remote config file
    with urllib.request.urlopen(config['update_url']) as response, open(path, 'wb') as out_file: 
        shutil.copyfileobj(response, out_file)
    
    with open(path, 'r') as file:
        remote = yaml.load_all(file)
    
    return remote

def check_for_updates(config: dict, remote_config: dict) -> dict:
    """ Check if updates are available
    Returns dict of module IDs containing None if no update is necessary, str url if update is needed. """
    updates = {}
    for module in remote_config['modules']:
        if module['version'] > config['modules'][module['id']]:
            updates[module['id']] = True
        else:
            updates[module['id']] = False
    
    return updates

def update_modules(config: dict, remote_config: dict, updates: dict):
    """ Update files based `updates`, the dict returned from check_for_updates. """
    cache = tempfile.gettempdir() + '/euclid_module_cache/'
    os.mkdir(cache)
    for module in updates:
        if updates['module'] != None:
            # 1. Download File
            path = f'{cache}/{module}.zip'
            with urllib.request.urlopen(updates['module']) as response, open(path, 'wb') as out_file: 
                shutil.copyfileobj(response, out_file)
            # 2. Make dest. folder
            if config['minecraft_folder'] == None:
                raise NoMinecraftFolder()
            else:
                dest = config['minecraft_folder'] + '/' + module + '/'
                os.mkdir(dest)
            # 3. Unzip file into dest. folder
            with zipfile.ZipFile(path, 'r') as zip_ref:
                zip_ref.extractall(dest)
