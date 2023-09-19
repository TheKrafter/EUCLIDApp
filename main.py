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


# Imports
# Yes ik arranging them by length is dumb
#  but so is this project so...
from kivy.logger import Logger as logger

import minecraft_launcher_lib as launcher
from dulwich import porcelain
from typing import Optional
import multiprocessing
import urllib.request
import subprocess
import tempfile
import zipfile
import shutil
import yaml
import sys
import os

import kivy
# NOTE: Other Kivy imports come later in main()

# Constants
DEFAULT_GIT_URL = 'https://github.com/TheKrafter/EUCLIDSource.git'
DEFAULT_GIT_BRANCH = 'main'
DEFAULT_JVM_ARGS = ["-Xmx2G", "-Xms2G"]
DEFAULT_MINECRAFT_SUBDIRECTORY = 'minecraft/'
DEFAULT_MINECRAFT_DATASUBDIR = 'data/'
DEFAULT_MINECRAFT_VERSION = '1.18.2'

CONFIG_FILE_NAME = 'euclid-git3.yml'

MICROSOFT_CLIENT_ID = None
MICROSOFT_SECRET = None

# If this should also have
# buttons and stuff to launch minecraft
if 'launcher' in sys.argv:
    APP_IS_LAUNCHER = True
else:
    APP_IS_LAUNCHER = False


def locate_config() -> str:
    """ Locate the EUCLID config file, creating it if it's not there. """
    if sys.platform == 'linux' or sys.platform == 'linux2':
        logger.debug('Detected Linux.')
        config_path = f'{os.getenv("HOME")}/.config/euclid/'
        data_dir = f'{os.getenv("HOME")}/.local/var/euclid/'
    elif sys.platform == 'darwin':
        logger.debug('Detected Darwin.')
        config_path = f'{os.getenv("HOME")}/Library/Application Support/EUCLID/'
        data_dir = config_path
    elif sys.platform == 'win32':
        logger.debug('Detected Windows.')
        config_path = f'{os.getenv("APPDATA")}/EUCLID/'
        data_dir = config_path
    else:
        logger.warn(f'Platform "{sys.platform}" not supported!')
        logger.info('Please contribute for your platform at https://github.com/TheKrafter/EUCLIDApp')
        raise NotImplementedError
        sys.exit(1)
    
    if not os.path.exists(config_path):
        os.mkdir(config_path)
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)
    
    if not os.path.exists(config_path + CONFIG_FILE_NAME):
        config = {
            'git_url': DEFAULT_GIT_URL,
            'git_branch': DEFAULT_GIT_BRANCH,
            'mc_dir': data_dir + DEFAULT_MINECRAFT_SUBDIRECTORY,
            'mc_data': data_dir + DEFAULT_MINECRAFT_DATASUBDIR,
            'mc_ver': DEFAULT_MINECRAFT_VERSION,
            'jvm_args': DEFAULT_JVM_ARGS,
            'ms_user': None,
            'ms_token': None,
            'ms_refresh': None,
            'installed': False
        }

        if not os.path.exists(config["mc_dir"]):
            os.mkdir(config["mc_dir"])
        if not os.path.exists(config["mc_data"]):
            os.mkdir(config["mc_data"])

        with open(config_path + CONFIG_FILE_NAME, 'w') as file:
            yaml.dump(config, file)
        logger.info('Created missing config file with default options!')
    
    return config_path + CONFIG_FILE_NAME


def load_config() -> dict:
    """ Load the EUCLID config file into a dict """

    path = locate_config()
    with open(path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    if config == None:
        os.remove(path)
        with open(locate_config(), 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

    logger.info(f'Loaded config file: {config}')

    return config


def dump_config(config: dict) -> None:
    """ Save the EUCLID config file to disk
    DISABLED: PROBLEMATIC """

    with open(locate_config(), 'w') as file:
        yaml.dump(config, file)

    logger.debug('Saved config file!')

    return None

def unsync(config: dict, interactive: bool = True) -> Optional[bool]:
    """ Remove synced data """
    if interactive:
        i = input(f'>> ARE YOU SURE YOU WANT TO REMOVE THE CONTENTS OF\n>> \'{config["mc_dir"]}\' ?\n>> [y/N]')
        if i.lower().strip() == 'y':
            return None
    
    logger.warning('REMOVING SYNCED DATA!')
    shutil.rmtree(config["mc_dir"])

    logger.warning('Removed Synced Data!')
    config['installed'] = False
    dump_config(config)


def initialize(config: dict) -> bool:
    """ Run setup on minecraft directory and install minecraft and fabric
    Returns True if successful, False if already installed. """
    logger.info('Running initial setup...')

    logger.info('Cloning Repo...')
    try:
        repo = porcelain.clone(
            config["git_url"],
            config["mc_dir"],
            branch = config["git_branch"]
        )
    except FileExistsError:
        logger.warning('Already cloned from git!')
        logger.info('Pulling...')
        #repo = porcelain.init(
        #    config["mc_dir"]
        #)
        porcelain.pull(
            config["mc_dir"],
            #config["git_url"]
        )
        

    logger.info('Installing Minecraft...')
    launcher.install.install_minecraft_version(config["mc_ver"], config["mc_dir"])

    logger.info('Installing Fabric...')
    launcher.fabric.install_fabric(config["mc_ver"], config["mc_dir"])

    config['installed'] = True
    dump_config(config)

    logger.info('Installed!')

    return None

def login(config: dict) -> bool:
    """ Placeholder """
    return True

def run(config: dict) -> None:
    """ Run Minecraft. """

    login = launcher.utils.generate_test_options() # TODO: LOGIN
    login["jvmArguments"] = config["jvm_args"]
    #login["gameDirectory"] = config["mc_data"]

    command = launcher.command.get_minecraft_command(config["mc_ver"], config["mc_dir"], login)

    logger.info('Starting Minecraft...')
    subprocess.run(command)

    logger.info('Stopped Minecraft.')
    return None

def main(args: list) -> None:
    """ The Application itself. """
    from kivy.app import App
    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.gridlayout import GridLayout
    from kivy.properties import StringProperty, AliasProperty
    
    
    logger.info('Starting Application...')

    class EUCLIDApp(App):

        def build(self) -> GridLayout:
            self.window = GridLayout()
            self.window.cols = 1

            title = "E. U. C. L. I. D.\nBSD-3-Clause License\nBy Krafter"
            self.label = Label(text=title)
            self.window.add_widget(
                self.label
            )

            config = load_config()
            if config == None:
                label = "INSTALL"
            elif config['installed']:
                label = "UPDATE"
            else:
                label = "INSTALL"
            self.button = Button(text=label)
            self.button.bind(
                on_press = self._callback_install
            )
            self.window.add_widget(
                self.button
            )

            global APP_IS_LAUNCHER

            if APP_IS_LAUNCHER:
                self.launch = Button(text="LAUNCH")
                self.launch.bind(
                    on_press = self._callback_run
                )
                self.window.add_widget(
                    self.launch
                )

            #self.status = Label(text="...")
            #self.window.add_widget(
            #    self.status
            #)

            return self.window

        def _change_status(self, status: str) -> None:
            #self.window.remove_widget(self.status)
            #self.status = Label(text=status)
            #self.window.add_widget(
            #    self.status
            #)
            #logger.debug(f'Changed status to: {status}')

            return None
        
        def _callback_install(self, instance) -> None:
            self.button.set_disabled(True)

            config = load_config()

            self._change_status("Installing...")

            init = multiprocessing.Process(target=initialize, args=(config, ))
            init.start()

            self._change_status("Installed.")

            self.button.set_disabled(False)
            return None
        
        def _callback_run(self, instance) -> None:
            self._change_status("Launching...")

            try:
                config = load_config()
            except:
                self._change_status("Failed.\nPlease click Install First.")
            
            if config["installed"]:
                self.launch.set_disabled(True)
                init = multiprocessing.Process(target=run, args=(config, ))
                init.start()

                init.join()
                self.launch.set_disabled(False)
            else:
                self._change_status('Not Installed.\nClick "INSTALL" first.')
            
            self._change_status("...")


            return None

    
    EUCLIDApp().run()
    
    logger.info('Exit.')
    return None

if __name__ == "__main__":
    main(sys.argv)