#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from os.path import expanduser
from os import environ
import platform
import subprocess
import logging
import argparse
import re
from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.styles import Style

# ---- Argument parser ----
def GetVersion() -> str:
    return "0.4.0"

def GetArgParser() -> argparse.ArgumentParser:
    tArgParser = argparse.ArgumentParser(usage="%(prog)s [OPTIONS]",
                                         description="List and connect to host entries from your ssh configuration")

    tArgParser.add_argument("-v", "--version", action="version", version = f"{tArgParser.prog} version {GetVersion()}")
    tArgParser.add_argument("-c", "--config", help="Path to configuration file", type=str, default=None, required=False)
    tArgParser.add_argument("-e", "--exclude", help="Exclude hosts based on python regular expression", type=str, default=None, required=False)
    tArgParser.add_argument("-s", "--ssh_command", help="SSH command", type=str, default="ssh", required=False)
    tArgParser.add_argument("-l", "--loop", help="Do not exit when ssh session ends, show host list again instead", action="store_true")
    tArgParser.add_argument("-t", "--terminal_tab_mode", help="Attempt to start ssh session in new tab/window of terminal", action="store_true")
    tArgParser.add_argument("-o", "--sort_host_entries", help="Sort host entries", action="store_true")
    tArgParser.add_argument("-r", "--reverse_order", help="Reverse sorting order", action="store_true")
    tArgParser.add_argument("-g", "--gui", help="Use a curses-like input dialog", action="store_true")
    return tArgParser

# -- Logger setup ---
def setuplogging():
    # Set application wide debug level and format
    #logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S',
                        level=logging.INFO)

# -- Read in host entries from a SSH client configuration file --
class SSHConfigHosts:
    HostsRegExp = r'^\s*Host\s+(.+)'
    IncludesRegExp = r'^\s*Include\s+([\w:\/\_\-\"\.\\]+)\s*'

    def __init__(self):
        self.ConfigFilePaths = []
        self.FilteredHosts = []
        self.AllHosts = []

    # -- Read in entries from ssh config file ---
    @staticmethod
    def CollectFromSSHConfig(Filename: str, RegExp: str, IgnoreCase: bool = False):
        try:
            with open(Filename, 'r') as f:
                Matches = re.findall(RegExp, f.read(), re.MULTILINE | (re.IGNORECASE if IgnoreCase else 0))
                #logging.debug (f'Searched {Filename} for {RegExp}. Result: {Matches}')
                return Matches
        except FileNotFoundError as e:
            logging.warning(f'File not found: {Filename}')
            return []
        except Exception as e:
            logging.debug(f'Skipping file {Filename}, cause: {str(e)}')
            return []

    def ReadInHosts(self, InitialConfigfile: str, RegEx = None, SortList = False, ReverseOrder = False):
        # Check for includes
        self.ConfigFilePaths = []
        self.ConfigFilePaths.append(InitialConfigfile)
        IncludedConfigs = SSHConfigHosts.CollectFromSSHConfig(InitialConfigfile, SSHConfigHosts.IncludesRegExp, IgnoreCase = True)
        for i in IncludedConfigs: self.ConfigFilePaths.append(i)
        logging.debug(f'Searching SSH configuration files: {self.ConfigFilePaths}')

        # Read in Host entries from all found configuration files
        self.AllHosts = []
        for i in self.ConfigFilePaths:
            Hosts = SSHConfigHosts.CollectFromSSHConfig(i, SSHConfigHosts.HostsRegExp, IgnoreCase = True)
            for j in Hosts: self.AllHosts.append(j)
        logging.debug(f'Host list: {self.AllHosts}')

        # Filter unwanted entries
        if not self.FilterHosts(RegEx): return False

        # Sort list if requested
        if SortList: self.SortHosts(ReverseOrder)
        return True

    # -- Filter hosts --
    def FilterHosts(self, RegEx = None):
        self.FilteredHosts = []
        try:
            if RegEx: self.FilteredHosts = [i for i in self.AllHosts if not ('*' in i) and not ('?' in i) and not ('!' in i) and not re.fullmatch(RegEx, i)]
            else:     self.FilteredHosts = [i for i in self.AllHosts if not ('*' in i) and not ('?' in i) and not ('!' in i)]
        except re.error as e:
            logging.error(f'Invalid regular expression: {e.msg}')
            return False
        return True

    # -- Sort list --
    def SortHosts(self, ReverseOrder = False):
        self.FilteredHosts.sort(key = str.lower, reverse = ReverseOrder)

class ConsoleFuncs:

    Prompt_toolkit_style = {
        'dialog': 'bg:#284A6B',
        'button': 'bg:#e8612c',
        'checkbox': '#073B6B',
        'dialog shadow': 'bg:#073B6B',
    }

    def __init__(self):
        self.Platform = platform.system().lower()

    # -- List strings and get choice from user ---
    @staticmethod
    def PickChoice(ChoicesList, Prompt: str = "? ", Caption: str = "", Gui: bool = True):
        if Gui:
            # Use prompt toolkit to show a curses-like dialog
            ChoicesToShow = list()
            for index, item in enumerate(ChoicesList):
                ChoicesToShow.append( (index, item) )
            Results = checkboxlist_dialog(title=Prompt,
                                          text=Caption,
                                          values=ChoicesToShow,
                                          style = Style.from_dict(ConsoleFuncs.Prompt_toolkit_style)
                                          ).run()
            return Results
        else:
            # Simple input: Show list and let user input a number
            Message = str()
            for index, item in enumerate(ChoicesList):
                Message += f'{index + 1}) {item}\n'
            Message = Message.replace('"','') # Quotes not needed for display, looks a bit more clean

            try:
                # User may input more than one number, separated by whitespaces.
                # Thus: Split string, try to convert every substring into an integer and check
                # if it is a valid index value. Return a list of valid choices.
                Input = input(f'\n{Caption}\n{Message}{Prompt}')
                Choices = Input.split()
                ChoicesChecked = []
                for i in Choices:
                    try:
                        if 0 < int(i) <= len(ChoicesList): ChoicesChecked.append(int(i) - 1)
                    except ValueError: pass # Ignore ValueError - those entries will not be added to the ChoicesChecked list because the exception hits before the 'append' happens. No need to take further action here.
                return ChoicesChecked
            except KeyboardInterrupt:
                return []

    # -- Clear console on supported platforms --
    def Clear(self):
        if 'windows' in self.Platform: subprocess.run('cls',   shell = True, check = False)
        if 'linux'   in self.Platform: subprocess.run('clear', shell = True, check = False)
        return

# -- Get ssh config from users home directory if no path was supplied ---
def GetHomeSSHConfigPath():
    return expanduser('~/.ssh/config')

# -- Get commandline to start new ssh connection --
def CommandLine(SSHCommand: str, Host:str, TerminalTabMode: bool = False):
    # Is it good style to hardcode this stuff here? Probably not. Do I care? Nope.
    Host_no_quotes = Host.replace('"','')
    WindowTitle = f'SSH {Host_no_quotes}'
    if TerminalTabMode and ("WT_SESSION" in environ): return f'wt -w 0 new-tab --title "{WindowTitle}" {SSHCommand} {Host}'
    if TerminalTabMode and ("TMUX" in environ):       return f'tmux new-window -n "{WindowTitle}" {SSHCommand} {Host}'
    return f'{SSHCommand} {Host}' # no TerminalTabMode or unsupported terminal

# --- main routine ----
def run_program():
    # setup logging
    setuplogging()

    # read in command line arguments
    parser = GetArgParser()
    targs = parser.parse_args()

    # Get host entries from configuration file
    ConfHosts = SSHConfigHosts()
    SSHConfigFile = targs.config if targs.config is not None else GetHomeSSHConfigPath()
    logging.info(f'Reading host entries from {SSHConfigFile}')

    if not ConfHosts.ReadInHosts(SSHConfigFile,
                                 targs.exclude,
                                 targs.sort_host_entries,
                                 targs.reverse_order):
        logging.error('Error reading in host entries, exit.')
        return 1
    if len(ConfHosts.FilteredHosts) == 0:
        logging.info("No hosts, exit.")
        return 0

    # Let user choose a host and start ssh connection
    Console = ConsoleFuncs()
    Caption_message = "Choose one or more hosts"
    if not targs.ssh_command == 'ssh': Caption_message += f"\n(SSH command: \"{targs.ssh_command}\")"
    while True:
        Choice = Console.PickChoice(ConfHosts.FilteredHosts,
                                    'Connect to: ',
                                    Caption_message,
                                    targs.gui)
        if not Choice:  # Abort right away if list of choices is empty
            logging.info('Abort')
            return 0
        for i in Choice: # loop through list of chosen host indices, and run the ssh command for each one
            logging.info(f'Connecting to "{ConfHosts.FilteredHosts[i]}"')
            try:
                Completed = subprocess.run(CommandLine(targs.ssh_command,
                                                       ConfHosts.FilteredHosts[i],
                                                       targs.terminal_tab_mode),
                                           shell = True)
                logging.info(f'"{Completed.args}" returned "{Completed.returncode}"')
                if (not targs.loop) and (len(Choice) == 1):
                    return Completed.returncode # When not in loop mode and only 1 choice was give: return exit code of the ssh session
                if targs.loop and targs.terminal_tab_mode:
                    Console.Clear() # When running in terminal tab mode AND loop mode: Clear the console after launching new tabs/windows, looks more clean
            except KeyboardInterrupt:
                logging.info('Canceled by user')
                return 0
        if not targs.loop:
            return 0 # When in 'loop' mode: do not return, display list again and pick next choice

if __name__ == '__main__':
    sys.exit(run_program())
