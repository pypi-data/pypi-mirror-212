#!/usr/bin/python3
# -*- coding: utf-8 -*-


# from __future__ import unicode_literals
import os
import sys
import time
import pydoc
import locale
import urllib3
import hashlib
import subprocess
from pathlib import Path
from datetime import date
from dialog import Dialog
from urllib3.exceptions import HTTPError
from sbo_create.templates import (
    SlackBuilds,
    slack_desc_template,
    info_template,
    doinst_script,
    douninst_script
)

from sbo_create.__metadata__ import __version__

locale.setlocale(locale.LC_ALL, '')


class SBoCreate:
    """ SlackBuild Create Class. """
    def __init__(self):
        # General defines
        self.choices = None
        self.data: list = []
        self.fields = None
        self.code = None
        self.handy_ruler = None
        self.editor: str = str()
        self.where_you_live: str = str()
        self.email: str = str()
        self.maintainer: str = str()
        self.editor_options: str = str()
        self.sources = None
        self.template = None
        self.slack_desc_comments = None
        self.slack_desc_user_text: list = []
        self.slack_desc_file_data: list = []
        self.current_folder: Path = Path.cwd()
        self.home_path: Path = Path.home()
        self.config_path: Path = Path(self.home_path, '.config', 'sbo-create')
        self.config_file: str = 'maintainer.config'
        self.maintainer_config: Path = Path(self.config_path, self.config_file)
        if not self.config_path.is_dir():
            self.config_path.mkdir(parents=True, exist_ok=True)
        # Default repository version
        self.sbo_repo_version: str = '15.0'

        # aboname.info initialize
        self.info_text: tuple = (
            'PRGNAM=', 'VERSION=', 'HOMEPAGE=', 'DOWNLOAD=',
            'MD5SUM=', 'DOWNLOAD_x86_64=', 'MD5SUM_x86_64=',
            'REQUIRES=', 'MAINTAINER=', 'EMAIL='
        )
        self.version: str = str()
        self.homepage: str = str()
        self.download_x86: str = str()
        self.md5sum_x86: str = str()
        self.download_x86_64: str = str()
        self.md5sum_x86_64: str = str()
        self.requires: str = str()

        # Set colors
        self.color: dict = {
            'bold': '\Zb',
            'reset_bold': '\ZB',
            'underline': '\Zu',
            'reset_underline': '\ZU',
            'reverse': '\Zr',
            'reset_reverse': 'Zr',
            'restore': '\Zn',
            'black': '\Z0',
            'red': '\Z1',
            'green': '\Z2',
            'yellow': '\Z3',
            'blue': '\Z4',
            'magenta': '\Z5',
            'cyan': '\Z6',
            'white': '\Z7'
        }
        self.error_title: str = f"{self.color['red']}Error{self.color['restore']}"

        # Define some configurations
        self.year: int = date.today().year
        self.dialog = Dialog(dialog='dialog')
        self.dialog.add_persistent_args(['--no-nl-expand', '--no-collapse', '--colors'])
        self.title: str = f'SlackBuild Create Tool {__version__}'
        self.dialog.set_background_title(self.title)
        self.prg_name: str = str(self.current_folder).split('/')[-1]
        self.read_maintainer_file()
        self.arguments()
        self.is_package_installed()

        # sboname.desktop initialize
        self.desktop_comment = str()
        self.desktop_exec: str = f'/usr/bin/{self.prg_name}'
        self.desktop_icon: str = f'/usr/share/pixmaps/{self.prg_name}.png'
        self.desktop_terminal: str = 'false'
        self.desktop_type: str = str()
        self.desktop_categories: str = str()
        self.desktop_generic_name: str = str()

    def arguments(self) -> None:
        """ Arguments for the cli menu control. """
        args: list = sys.argv
        args.pop(0)

        create_files: bool = False
        options: dict = {
            'help': ['-h', '--help'],
            'version': ['-v', '--version'],
            'prgnam': ['-n', '--prgnam'],
            'prg-version': ['-e', '--prg-version'],
            'template': ['-t', '--template'],
            'create-files': ['-f', '--create-files'],
            'maintainer': ['-m', '--maintainer'],
            'download': ['-d', '--download'],
            'check': ['-c', '--check']
        }
        # Creates lists to a list
        all_options: list = sum(options.values(), [])
        options_with_parameter: list = sum(
            [options['prgnam'],
             options['prg-version'],
             options['template'],
             options['check']],
            []
        )

        # Checks for valid options
        invalid: list = []
        for arg in args:
            if arg.startswith('-') and arg not in all_options:
                invalid.append(arg)
            if not arg.startswith('-') and args[args.index(arg) - 1] not in options_with_parameter:
                invalid.append(arg)

        if invalid and len(args) > 0:
            print(f"\nsbo-create: Error: Invalid options: {', '.join(set(invalid))}\n")
            raise SystemExit(1)

        for arg in args:
            try:
                if arg in options['prgnam']:
                    self.prg_name: str = args[args.index(arg) + 1]
                if arg in options['prg-version']:
                    self.version: str = args[args.index(arg) + 1]
                if arg in options['template']:
                    self.template: str = args[args.index(arg) + 1]
                if arg in options['check']:
                    self.prg_name: str = args[args.index(arg) + 1]
            except IndexError:
                print('\nsbo-create: Error: Missing an argument\n')
                raise SystemExit(1)

            if arg in options['create-files']:
                create_files: bool = True

        if len(args) > 7:
            self.usage()
        elif len(args) == 1 and args[0] in options['help']:
            self.usage()
        elif len(args) == 1 and args[0] in options['version']:
            print(f'Version: {__version__}')
            raise SystemExit()
        elif create_files:
            self.create_files()
        elif len(args) == 1 and args[0] in options['maintainer']:
            self.edit_maintainer_file()
        elif len(args) == 1 and args[0] in options['download']:
            self.sources_download()
        elif len(args) == 2 and args[0] in options['check']:
            self.is_the_sbo_exists()

    def create_files(self) -> None:
        """ It will create at least the following files:
            <prgnam>.SlackBuild
            <prgnam>.info
            README
            slack-desc
        """
        templates: dict = {
            'autotools': SlackBuilds(
                self.prg_name, self.version, self.year, self.maintainer,
                self.where_you_live).autotools,
            'cmake': SlackBuilds(
                self.prg_name, self.version, self.year, self.maintainer,
                self.where_you_live).cmake,
            'perl': SlackBuilds(
                self.prg_name, self.version, self.year, self.maintainer,
                self.where_you_live).perl,
            'python': SlackBuilds(
                self.prg_name, self.version, self.year, self.maintainer,
                self.where_you_live).python,
            'rubygem': SlackBuilds(
                self.prg_name, self.version, self.year, self.maintainer,
                self.where_you_live).rubygem,
            'haskell': SlackBuilds(
                self.prg_name, self.version, self.year, self.maintainer,
                self.where_you_live).haskell,
            'meson': SlackBuilds(
                self.prg_name, self.version, self.year, self.maintainer,
                self.where_you_live).meson,
        }

        try:
            slackbuild: str = templates[self.template]()
        except KeyError:
            slackbuild: str = str()

        info: str = info_template(self.prg_name, self.version, self.maintainer, self.email)
        slack_desc: str = slack_desc_template(self.prg_name)
        readme: str = str()

        files: dict = {
            f'{self.prg_name}.SlackBuild': slackbuild,
            f'{self.prg_name}.info': info,
            'slack-desc': slack_desc,
            'README': readme
        }

        created_files: list = []
        for file, content in files.items():
            with open(Path(self.current_folder, file), 'w') as f:
                f.write(content)
            created_files.append(file)

        print(f"Files created:\n")
        for file in created_files:
            print(f"{'':>2}> {file}")

        print()
        raise SystemExit()

    @staticmethod
    def usage() -> None:
        """ Optional arguments. """
        args: str = (
            "Usage: sbo-create [OPTIONS]\n\n"
            "Optional arguments:\n"
            "  -n, --prgnam NAME          Set the name of the SlackBuild.\n"
            "  -e, --prg-version VERSION  Set the version of the SlackBuild.\n"
            "  -t, --template TEMPLATE    Set the SlackBuild template:\n"
            "                             templates={autotools, cmake, perl, python,\n"
            "                                        rubygem, haskell, meson}\n"
            "  -f, --create-files         Creates the necessary files and exit:\n"
            "                             files={<prgnam>.SlackBuild, <prgnam>.info,\n"
            "                                    README, slack-desc}.\n"
            "  -m, --maintainer           Edit the maintainer file.\n"
            "  -d, --download             Download source files listed in the .info file.\n"
            "  -c, --check NAME           Check if the SBo exist in the repository.\n"
            "  -h, --help                 Display this message and exit.\n"
            "  -v, --version              Show version and exit.\n"
        )
        print(args)
        raise SystemExit()

    def menu_initialization(self) -> None:
        self.data: list = []

        self.choices: list = [
            ('Info', f'Edit {self.prg_name}.info file'),
            ('Slack desc', 'Edit slack-desc file'),
            ('SlackBuild', f'Edit {self.prg_name}.SlackBuild script'),
            ('Doinst.sh', 'Edit doinst.sh script'),
            ('Douninst.sh', 'Edit douninst.sh script'),
            ('README', 'Edit README file'),
            ('Desktop', f'Edit {self.prg_name}.desktop file'),
            ('Permissions', f'Chmod -+ {self.prg_name}.SlackBuild script'),
            ('Download', 'Download the sources'),
            ('Checksum', 'Md5sum the sources'),
            ('Check', f'Check if the {self.prg_name} SBo exists'),
            ('Maintainer', 'Edit maintainer data'),
            ('Directory', 'Change directory'),
            ('Help', 'Where to get help'),
            ('About', 'About sbo-create'),
            ('Exit', 'Exit the program')
        ]

    def main_menu(self) -> None:
        """ Dialog.menu(text, height=None, width=None, menu_height=None,
        choices=[], **kwargs) Display a menu dialog box. """
        self.menu_initialization()  # reset
        width: int = 56 + len(self.prg_name)
        text: str = "\nChoose an option or press <ESC> or <Cancel> to Exit."
        title = f"{self.color['bold']}{self.color['green']}SBO Create Tool{self.color['restore']}"
        code, tag = self.dialog.menu(
            text=text,
            title=title,
            height=27, width=width,
            menu_height=len(self.choices),
            choices=self.choices, help_button=True
        )

        if code == self.dialog.CANCEL or code == self.dialog.ESC or tag[0] == '0':
            self.clear_and_exit()
        elif code == 'help':
            self.get_help()

        case: dict = {
            'Info': self.edit_info_file,
            'Slack desc': self.edit_slack_desc_file,
            'SlackBuild': self.edit_slackbuild_file,
            'Doinst.sh': self.edit_doinst_file,
            'Douninst.sh': self.edit_douninst_file,
            'Desktop': self.edit_desktop_file_file,
            'README': self.edit_readme_file,
            'Permissions': self.change_permissions,
            'Download': self.sources_download,
            'Checksum': self.update_the_checksum,
            'Check': self.is_the_sbo_exists,
            'Maintainer': self.edit_maintainer_file,
            'Directory': self.update_working_directory,
            'Help': self.get_help,
            'About': self.about,
            'Exit': self.clear_and_exit
        }
        case[tag]()

    def edit_info_file(self) -> None:
        """ <prgnam>.info file handler. """
        info_file: str = f'{self.prg_name}.info'
        comments: str = f"\nCreates a '{info_file}' file."
        field_length: int = 72
        input_length: int = 100
        attributes: str = '0x0'

        maintainer: str = self.maintainer
        email: str = self.email

        self.read_info_file()

        # Replace maintainer data
        if maintainer and maintainer != self.maintainer:
            yesno: str = self.dialog.yesno('\nDo you want to replace the maintainer name or email?',
                                           height=7, width=57)

            if yesno == 'ok':
                self.maintainer: str = maintainer
                self.email: str = email

        elements: list = [
            (self.info_text[0], 1, 1, self.prg_name, 1, len(self.info_text[0]) + 1,
             field_length - len(self.info_text[0]), input_length, attributes),
            (self.info_text[1], 2, 1, self.version, 2, len(self.info_text[1]) + 1,
             field_length - len(self.info_text[1]), input_length, attributes),
            (self.info_text[2], 3, 1, self.homepage, 3, len(self.info_text[2]) + 1,
             field_length - len(self.info_text[2]), input_length * 2, attributes),
            (self.info_text[3], 4, 1, self.download_x86, 4, len(self.info_text[3]) + 1,
             field_length - len(self.info_text[3]), input_length * 10, attributes),
            (self.info_text[4], 5, 1, self.md5sum_x86, 5, len(self.info_text[4]) + 1,
             field_length - len(self.info_text[4]), input_length * 10, attributes),
            (self.info_text[5], 6, 1, self.download_x86_64, 6, len(self.info_text[5]) + 1,
             field_length - len(self.info_text[5]), input_length * 10, attributes),
            (self.info_text[6], 7, 1, self.md5sum_x86_64, 7, len(self.info_text[6]) + 1,
             field_length - len(self.info_text[6]), input_length * 10, attributes),
            (self.info_text[7], 8, 1, self.requires, 8, len(self.info_text[7]) + 1,
             field_length - len(self.info_text[7]), input_length * 4, attributes),
            (self.info_text[8], 9, 1, self.maintainer, 9, len(self.info_text[8]) + 1,
             field_length - len(self.info_text[8]), input_length, attributes),
            (self.info_text[9], 10, 1, self.email, 10, len(self.info_text[9]) + 1,
             field_length - len(self.info_text[9]), input_length, attributes)
        ]

        self.dialog_mixedform(comments=comments, title=info_file, elements=elements, height=19, width=78)

        if self.fields:
            self.version: str = self.fields[1]
            self.homepage: str = self.fields[2]
            self.download_x86: str = self.fields[3]
            self.md5sum_x86: str = self.fields[4]
            self.maintainer: str = self.fields[8]
            self.email: str = self.fields[9]

            if self.download_x86:
                self.sources: list = [source.split('/')[-1] for source in self.download_x86.split()]
            self.download_x86_64: str = self.fields[5]
            self.md5sum_x86_64: str = self.fields[6]

            if self.download_x86_64:
                self.sources: list = [source.split('/')[-1] for source in self.download_x86_64.split()]
            self.requires: str = self.fields[7]

        self.fix_quotation_mark()

        for item, line in zip(self.info_text, self.fields):
            self.data.append(f'{item}{line}')

        self.choose_for_write(Path(self.current_folder, info_file))

    def edit_slack_desc_file(self) -> None:
        """ slack-desc file handler. """
        self.slack_desc_handy_ruler_comments(1)
        field_length: int = 71 + len(self.prg_name)
        input_length: int = 70
        attributes: str = '0x0'
        elements: list = []
        self.read_slack_desc_file()
        start_from: int = 1  # Set up the line to start

        if not self.slack_desc_file_data[0]:  # check description
            start_from: int = 2
            elements: list = [
                (f'{self.prg_name}:', 1, 1, f' {self.prg_name} ()', 1,
                 len(self.prg_name) + 2, field_length - len(self.prg_name), input_length, attributes)
            ]

        for n, line in zip(range(start_from, 13), self.slack_desc_file_data):
            elements += [
                (f'{self.prg_name}:', n, 1, line, n,
                 len(self.prg_name) + 2, field_length - len(self.prg_name),
                 input_length, attributes)
            ]

        self.dialog_mixedform(comments=f'\n{self.slack_desc_comments}', title='slack-desc', elements=elements,
                              height=30, width=78 + len(self.prg_name))

        self.slack_desc_handy_ruler_comments(0)
        self.data: list = [line for line in self.slack_desc_comments.splitlines()]

        for line in self.fields:
            if not line.startswith(' ') and len(line) < 70:
                line: str = f' {line}'
            self.data.append(f'{self.prg_name}:{line}')

        self.choose_for_write(Path(self.current_folder, 'slack-desc'))
        
    def edit_slackbuild_file(self) -> None:
        """ <prgnam>.SlackBuild handler file. """
        self.read_info_file()
        version: str = self.version.replace('"', '')
        slackbuild: str = f'{self.prg_name}.SlackBuild'
        path_file: Path = Path(self.current_folder, slackbuild)

        if not path_file.is_file() and not self.template:
            choices: list = [
                ('autotools', 'autotools-template.SlackBuild', False),
                ('cmake', 'cmake-template.SlackBuild', False),
                ('perl', 'perl-template.SlackBuild', False),
                ('python', 'python-template.SlackBuild', False),
                ('rubygem', 'rubygem-template.SlackBuild', False),
                ('haskell', 'haskell-template.SlackBuild', False),
                ('meson', 'meson-template.SlackBuild', False)
            ]
            message: str = f"\nChoose a template for the '{slackbuild}' file."
            code, self.template = self.dialog.radiolist(message, title=slackbuild,
                                                        height=9, width=len(self.prg_name) + 50,
                                                        list_height=0, choices=choices)

            if code == 'cancel':
                self.main_menu()

        templates: dict = {
            'autotools': SlackBuilds(
                self.prg_name, version, self.year, self.maintainer,
                self.where_you_live).autotools().splitlines,
            'cmake': SlackBuilds(
                self.prg_name, version, self.year, self.maintainer,
                self.where_you_live).cmake().splitlines,
            'perl': SlackBuilds(
                self.prg_name, version, self.year, self.maintainer,
                self.where_you_live).perl().splitlines,
            'python': SlackBuilds(
                self.prg_name, version, self.year, self.maintainer,
                self.where_you_live).python().splitlines,
            'rubygem': SlackBuilds(
                self.prg_name, version, self.year, self.maintainer,
                self.where_you_live).rubygem().splitlines,
            'haskell': SlackBuilds(
                self.prg_name, version, self.year, self.maintainer,
                self.where_you_live).haskell().splitlines,
            'meson': SlackBuilds(
                self.prg_name, version, self.year, self.maintainer,
                self.where_you_live).meson().splitlines
        }

        if self.template:
            try:
                self.data = templates[self.template]()
            except KeyError:
                message: str = f"\nThe template '{self.template}' is not exist."
                self.dialog.msgbox(message, title=self.error_title, height=7, width=len(message) + 5)
                self.main_menu()

        if not self.template and not path_file.is_file():
            message: str = '\nNo SlackBuild template selected.'
            self.dialog.msgbox(message, title=self.error_title, height=7, width=len(message) + 5)
            self.edit_slackbuild_file()

        if not path_file.is_file():
            message: str = f'\n{path_file.stem}.SlackBuild script created.'
            self.write_file(path_file)
            self.dialog.msgbox(message, title='Done', height=7, width=len(message) + 5)

        self.edit_file(path_file)
        self.main_menu()

    def edit_doinst_file(self) -> None:
        """ doinst.sh file handler file. """
        os.system('clear')
        temp: str = '\n'.join(doinst_script().splitlines())
        pydoc.pipepager(temp, cmd='less -R')
        self.edit_file(Path(self.current_folder, 'doinst.sh'))
        self.main_menu()

    def edit_douninst_file(self) -> None:
        """ douninst.sh file handler file. """
        os.system('clear')
        temp: str = '\n'.join(douninst_script().splitlines())
        pydoc.pipepager(temp, cmd='less -R')
        self.edit_file(Path(self.current_folder, 'douninst.sh'))
        self.main_menu()

    def edit_desktop_file_file(self) -> None:
        """ <prgnam>.desktop file handler. """
        desktop_file: str = f'{self.prg_name}.desktop'
        comments: str = f"\nCreates a '{desktop_file}' file."
        field_length: int = 72
        input_length: int = 100
        attributes: str = '0x0'
        text: list = [
            '[Desktop Entry]', 'Name=', 'Comment=', 'Exec=', 'Icon=',
            'Terminal=', 'Type=', 'Categories=', 'GenericName='
        ]

        self.read_desktop_file()

        elements = [
            (text[0], 1, 1, '', 1, 1, field_length - len(text[0]), input_length, 0x1),
            (text[1], 2, 1, self.prg_name, 2, 6, field_length - len(text[1]),
             input_length, attributes),
            (text[2], 3, 1, self.desktop_comment, 3, 9, field_length - len(text[2]), input_length,
             attributes),
            (text[3], 4, 1, self.desktop_exec, 4, 6, field_length - len(text[3]), input_length,
             attributes),
            (text[4], 5, 1, self.desktop_icon, 5, 6, field_length - len(text[4]), input_length,
             attributes),
            (text[5], 6, 1, self.desktop_terminal, 6, 10, field_length - len(text[5]), input_length,
             attributes),
            (text[6], 7, 1, self.desktop_type, 7, 6, field_length - len(text[6]), input_length,
             attributes),
            (text[7], 8, 1, self.desktop_categories, 8, 12, field_length - len(text[7]),
             input_length, attributes),
            (text[8], 9, 1, self.desktop_generic_name, 9, 13, field_length - len(text[8]),
             input_length, attributes),
        ]

        self.dialog_mixedform(comments=comments, title=desktop_file, elements=elements, height=18, width=78)

        if self.fields:
            self.prg_name: str = self.fields[1]
            self.desktop_comment: str = self.fields[2]
            self.desktop_exec: str = self.fields[3]
            self.desktop_icon: str = self.fields[4]
            self.desktop_terminal: str = self.fields[5]
            self.desktop_type: str = self.fields[6]
            self.desktop_categories: str = self.fields[7]
            self.desktop_generic_name: str = self.fields[8]

        for item, line in zip(text, self.fields):
            self.data.append(item + line)

        self.choose_for_write(Path(self.current_folder, f'{self.prg_name}.desktop'))

    def edit_readme_file(self) -> None:
        """ README file handler file. """
        self.read_slack_desc_file()
        slack_desc: Path = Path(self.current_folder, 'slack-desc')
        readme: Path = Path(self.current_folder, 'README')
        readme_file_size: int = 0

        if readme.is_file():
            readme_file_size: int = Path(readme).stat().st_size

        if slack_desc.is_file() and len(self.slack_desc_user_text[1:]) > 0:
            if readme_file_size == 0:
                self.import_user_text_from_slack_desc_file()
                self.write_file(readme)

        self.edit_file(readme)
        self.main_menu()

    def change_permissions(self) -> None:
        """ Change the permissions to the <prgnam>.SlackBuild script. """
        if not Path(f'{self.prg_name}.SlackBuild').is_file():
            message: str = f"\nThere is no '{self.prg_name}.SlackBuild' script."
            self.dialog.msgbox(message, title=self.error_title, height=7, width=len(message) + 5)
            self.main_menu()

        text: str = '\nChange the permissions to the SlackBuild script.'
        choices: list = [
            ('chmod +x', f'{self.prg_name}.SlackBuild', False),
            ('chmod -x', f'{self.prg_name}.Slackbuild', False),
        ]

        code, tag = self.dialog.radiolist(text=text, title='Permissions', height=9,
                                          width=len(text) + 5, list_height=0, choices=choices)

        if code == 'cancel':
            self.main_menu()

        if not tag:
            message: str = f"\nYou didn't make a choice"
            self.dialog.msgbox(message, title=self.error_title, height=7, width=len(message) + 5)
            self.change_permissions()

        subprocess.call(f'{tag} {self.prg_name}.SlackBuild', shell=True)

        message: str = f'\nThe permissions has been changed in the script {self.prg_name}.SlackBuild.'
        self.dialog.msgbox(message, title='Done', height=7, width=len(message) + 5)
        self.main_menu()

    def sources_download(self) -> None:
        """ Download the sources. """
        self.read_info_file()

        if not self.download_x86 and not self.download_x86_64:
            message: str = f"\nThere are no DOWNLOAD in the '{self.prg_name}.info' file."
            self.dialog.msgbox(message, title=self.error_title, height=7, width=len(message) + 5)
            self.main_menu()

        if self.download_x86:
            for link in self.download_x86.split():
                self.download(link)

        if self.download_x86_64:
            for link in self.download_x86_64.split():
                self.download(link)

        self.main_menu()

    def update_the_checksum(self) -> None:
        """ Update the source checksum. """
        text1: str = '\nChoose which checksum you want to update.'
        text2: str = '\nSelect the type of the architecture.'
        files: dict = {}

        self.read_info_file()

        sources = self.download_x86
        if not self.download_x86:
            sources: str = self.download_x86_64

        if not sources:
            message: str = f"\nNo sources found in the '{self.prg_name}.info' file."
            self.dialog.msgbox(message, title=self.error_title, height=7, width=(len(message) + 5))
            self.main_menu()

        choices: list = []
        # Creating a dictionary with file and checksum
        for src in sources.split():
            file = src.split('/')[-1]
            files[file]: dict = self.source_check_sum(file)

        # Add the items to a list for choosing
        for k, v in files.items():
            choices += [
                (v, k, False)
            ]

        code1, tag1 = self.dialog.checklist(text=text1, title='Choose checksum', height=8 + len(files), width=78,
                                            list_height=0, choices=choices)
        if code1 == 'cancel':
            self.main_menu()

        choices: list = [
                ('MD5SUM_x86', 'For x86 sources', False),
                ('MD5SUM_x86_64', 'For x86_64 sources', False),
            ]

        code2, tag2 = self.dialog.radiolist(text=text2, title='Select architecture', height=9, width=78,
                                            list_height=0, choices=choices)
        if code2 == 'cancel':
            self.main_menu()

        if tag2 == 'MD5SUM_x86':
            self.md5sum_x86: str = ' '.join(tag1)
        elif tag2 == 'MD5SUM_x86_64':
            self.md5sum_x86_64: str = ' '.join(tag1)

        self.edit_info_file()

    def is_the_sbo_exists(self) -> None:
        """ Checks if the SlackBuild exist in the repository. """
        self.dialog.infobox(f"\nSearching for '{self.prg_name}' please wait...",
                            width=len(self.prg_name) + 36, height=5)
        title: str = 'Done'
        message: str = f"\nNo SlackBuild found with the name '{self.prg_name}' in the repository."

        mirror: str = f'https://slackbuilds.org/slackbuilds/{self.sbo_repo_version}/TAGS.txt'
        http = urllib3.PoolManager()

        try:
            repo = http.request('GET', mirror)
        except HTTPError:
            repo: str = str()
            message: str = f"\nsbo-create: Error: Failed to connect to '{mirror}'"

        height: int = 7
        width: int = len(message) + 5

        if repo:
            for sbo in repo.data.decode().splitlines():
                if self.prg_name == sbo.split(':')[0]:
                    width: int = 50 + len(self.prg_name)
                    title: str = self.error_title
                    message: str = f"\nThe SlackBuild '{self.prg_name}' exists in the repository."

        self.dialog.msgbox(text=message, title=title, height=height, width=width)
        self.main_menu()

    def edit_maintainer_file(self) -> None:
        """ Maintainer data handler. """
        comments: str = '\nEnter the details of the maintainer data.'
        field_length: int = 68
        input_length: int = 100
        attributes: str = '0x0'

        text: tuple = (
            'MAINTAINER=',
            'EMAIL=',
            'WHERE YOU LIVE=',
            'EDITOR=',
            'OPTIONS FOR EDITOR=',
            'SBO REPOSITORY VERSION='
        )

        elements: list = [
            (text[0], 1, 1, self.maintainer, 1, len(text[0]) + 1, field_length - len(text[0]), input_length,
             attributes),
            (text[1], 2, 1, self.email, 2, len(text[1]) + 1, field_length - len(text[1]), input_length,
             attributes),
            (text[2], 3, 1, self.where_you_live, 3, len(text[2]) + 1, field_length - len(text[2]), input_length,
             attributes),
            (text[3], 4, 1, self.editor, 4, len(text[3]) + 1, field_length - len(text[3]), input_length,
             attributes),
            (text[4], 5, 1, self.editor_options, 5, len(text[4]) + 1, field_length - len(text[4]), input_length,
             attributes),
            (text[5], 6, 1, self.sbo_repo_version, 6, len(text[5]) + 1, field_length - len(text[5]), input_length,
             attributes)
        ]

        self.dialog_mixedform(comments=comments, title='Maintainer Data', elements=elements, height=15, width=75)

        if self.fields:
            self.maintainer: str = self.fields[0].strip()
            self.email: str = self.fields[1].strip()
            self.where_you_live: str = self.fields[2].strip()
            self.editor: str = self.fields[3].strip()
            self.editor_options: str = self.fields[4].strip()
            self.sbo_repo_version: str = self.fields[5].strip()

            for item, field in zip(text, self.fields):
                self.data.append(f'{item}{field}')

        self.choose_for_write(self.maintainer_config)

    def update_working_directory(self) -> None:
        comments: str = f'\nCurrent directory: {self.current_folder}'
        elements: list = [
            ('New path=', 1, 1, str(self.current_folder), 1, 10, 90, 90, '0x0'),
        ]
        self.dialog_mixedform(comments=comments, title='Update directory', elements=elements, height=10, width=78)

        if self.fields:
            if not os.path.isdir(self.fields[0].strip()):
                message: str = f"\nDirectory '{self.fields[0].strip()}' is not exist."
                self.dialog.msgbox(message, title=self.error_title, height=7, width=len(message) + 5)
                self.update_working_directory()

            self.current_folder = self.fields[0].strip()

            message: str = f'\nCurrent directory: {self.current_folder}'
            self.dialog.msgbox(message, title='Updated', height=7, width=len(message) + 5)

        self.main_menu()

    def get_help(self) -> None:
        """ Get help from slackbuilds.org. """
        message: str = ("\nFor additional assistance, visit:\n\n"
                        f"SlackBuild Usage HOWTO: {self.color['blue']}https://www.slackbuilds.org/howto/"
                        f"{self.color['restore']}\n"
                        f"Frequently Asked Questions: {self.color['blue']}https://www.slackbuilds.org/faq/"
                        f"{self.color['restore']}\n"
                        f"Submission Guidelines: {self.color['blue']}http://www.slackbuilds.org/guidelines/"
                        f"{self.color['restore']}\n"
                        f"SlackBuild Script Templates: {self.color['blue']}https://slackbuilds.org/templates/"
                        f"{self.color['restore']}")

        self.dialog.msgbox(message, title="Help", height=12, width=68)
        self.main_menu()

    def about(self) -> None:
        """ About the sbo-create tool. """
        message: str = (
            f"\n{self.color['green']}{self.color['bold']}"
            f"SlackBuild Create Tool{self.color['restore']}\n\n"
            "A tool that creates easy, fast and safe SlackBuilds files scripts.\n"
            f"Version: {__version__}\n\n"
            f"Homepage: {self.color['blue']}https://gitlab.com/dslackw/"
            f"sbo-create{self.color['restore']}\n"
            "Copyright © 2015-2023 Dimitris Zlatanidis\n"
            "Email: dslackw@gmail.com\n\n"
            "Slackware ® is a Registered Trademark of Patrick Volkerding.\n"
            "Linux is a Registered Trademark of Linus Torvalds."
        )

        self.dialog.msgbox(message, title="About", height=17, width=70)
        self.main_menu()

    @staticmethod
    def clear_and_exit() -> None:
        os.system('clear')
        raise SystemExit(0)

    def read_info_file(self) -> None:
        """ Read data from <prgnam>.info file if exist. """
        info_file: Path = Path(self.current_folder, f'{self.prg_name}.info')
        if info_file.is_file():
            with open(info_file, 'r') as info:

                info_file: list = info.read().splitlines()

                self.version: str = self.info_find_element(self.info_text[1], info_file)
                self.homepage: str = self.info_find_element(self.info_text[2], info_file)

                self.download_x86: str = self.find_elements(self.info_text[3], self.info_text[4], info_file)
                if not self.md5sum_x86:
                    self.md5sum_x86: str = self.find_elements(self.info_text[4], self.info_text[5], info_file)

                self.download_x86_64: str = self.find_elements(self.info_text[5], self.info_text[6], info_file)
                if not self.md5sum_x86_64:
                    self.md5sum_x86_64: str = self.find_elements(self.info_text[6], self.info_text[7], info_file)

                self.requires: str = self.info_find_element(self.info_text[7], info_file)
                self.maintainer: str = self.info_find_element(self.info_text[8], info_file)
                self.email: str = self.info_find_element(self.info_text[9], info_file)

    def read_slack_desc_file(self) -> None:
        self.slack_desc_file_data: list = [''] * 10
        self.slack_desc_user_text: list = []
        slack_desc: Path = Path(self.current_folder, 'slack-desc')

        if slack_desc.is_file():
            self.slack_desc_file_data: list = []  # Reset data before read
            with open(slack_desc, 'r') as desc:
                for count, line in enumerate(desc):

                    if 7 < count < 19:
                        line = line[len(self.prg_name) + 1:].rstrip()
                        self.slack_desc_file_data.append(line)

                        if line:
                            self.slack_desc_user_text.append(line)

    def read_desktop_file(self) -> None:
        """ Read data from <prgnam>.desktop file if exist. """
        desktop_file: Path = Path(self.current_folder, f'{self.prg_name}.desktop')
        if desktop_file.is_file():
            with open(desktop_file, 'r') as f:
                dsk: list = f.read().splitlines()

                self.desktop_comment: str = dsk[2].split('=')[1].strip()
                self.desktop_exec: str = dsk[3].split('=')[1].strip()
                self.desktop_icon: str = dsk[4].split('=')[1].strip()
                self.desktop_terminal: str = dsk[5].split('=')[1].strip()
                self.desktop_type: str = dsk[6].split('=')[1].strip()
                self.desktop_categories: str = dsk[7].split('=')[1].strip()
                self.desktop_generic_name: str = dsk[8].split('=')[1].strip()

    def read_maintainer_file(self) -> None:
        """ Initialization maintainer data. """
        if self.maintainer_config.is_file():
            with open(self.maintainer_config, 'r') as f:
                lines: list = f.read().splitlines()

                if len(lines) == 6:

                    if '=' in lines[0]:
                        self.maintainer: str = lines[0].split('=')[-1].strip()

                    if '=' in lines[1]:
                        self.email: str = lines[1].split('=')[-1].strip()

                    if '=' in lines[2]:
                        self.where_you_live: str = lines[2].split('=')[-1].strip()

                    if '=' in lines[3]:
                        self.editor: str = lines[3].split('=')[-1].strip()

                    if '=' in lines[4]:
                        self.editor_options: str = lines[4].split('=')[-1].strip()

                    if '=' in lines[5]:
                        self.sbo_repo_version: str = lines[5].split('=')[-1].strip()

                else:
                    message: str = f"\nThe {self.config_file} seems it's not correct."
                    self.dialog.msgbox(message, title=self.error_title, height=7, width=len(message) + 5)

    def download(self, link: str) -> None:
        """ Wget downloader. """
        file: str = link.split("/")[-1]

        yesno: str = self.dialog.yesno(
            f"\n{self.color['blue']}{file}{self.color['restore']}\n\n"
            f"Do you want to download the file?", title='Download', height=9, width=40 + len(file)
        )

        if yesno == 'ok':
            self.dialog.infobox('\nDownloading, please wait...', width=32, height=5)
            time.sleep(1)
            output: int = subprocess.call(f'wget --continue {link}', shell=True,
                                          stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

            if output > 0:
                self.dialog.msgbox(f"\nDownloading '{file}' {self.color['red']}FAILED!{self.color['restore']}",
                                   title=self.error_title, height=7, width=42 + len(self.prg_name))
            else:
                self.dialog.msgbox(f"\nDownloading file '{file}' finished!", title="Done",
                                   height=7, width=35 + len(file))

    def is_package_installed(self) -> None:
        var_log_packages: Path = Path('/var/log/packages/')
        packages: list = [pkg.name for pkg in var_log_packages.iterdir()]

        for package in packages:
            name = '-'.join(package.split('-')[:-3])
            if name == self.prg_name:
                yesno: str = self.dialog.yesno(
                    f"{self.color['red']}WARNING!{self.color['restore']}"
                    f" There is installed package with the name '{self.prg_name}'.\n"
                    '\nDo you want to continue?', height=8, width=60 + len(self.prg_name)
                )
                if yesno == 'cancel':
                    self.clear_and_exit()

    def dialog_mixedform(self, comments: str, title: str, elements: list, height: int, width) -> None:
        """ Dialog.mixedform(text, elements, height=0, width=0, form_height=0,
        **kwargs)
        Display a form consisting of labels and fields. """
        self.code, self.fields = self.dialog.mixedform(text=comments, title=title, elements=elements,
                                                       height=height, width=width, help_button=True)

        if self.code == 'help':
            self.get_help()

    def edit_file(self, file: Path) -> None:
        """ Editor handler. """
        if self.editor:
            subprocess.call(f'{self.editor} {self.editor_options} {file}', shell=True)

    def choose_for_write(self, file: Path) -> None:
        if self.code == self.dialog.OK:
            message: str = f"\nThe file '{str(file).split('/')[-1]}' is created."
            if file.is_file():
                message: str = f"\nThe file '{str(file).split('/')[-1]}' modified."

            if file.suffix == '.info':
                self.write_info(file)
            else:
                self.write_file(file)

            self.dialog.msgbox(message, height=7, title="Done", width=len(message) + 5)
            self.main_menu()

        elif self.code in [self.dialog.CANCEL, self.dialog.ESC]:
            self.main_menu()

    def import_user_text_from_slack_desc_file(self) -> None:
        """ Imports only the user entered text from slack-desc file. """
        yesno = self.dialog.yesno('Import description from the <slack-desc> file?', height=7, width=55)

        if yesno == 'ok':
            for desc in self.slack_desc_file_data[1:]:
                if desc and not desc.startswith((' Homepage:', ' homepage:')):
                    self.data.append(desc)

            # Removes the spaces at the beginning
            self.data: list = list(map(str.lstrip, self.data))

    def slack_desc_handy_ruler_comments(self, align: int) -> None:
        handy_ruler: int = len(self.prg_name) + align
        self.slack_desc_comments: str = (
            "# HOW TO EDIT THIS FILE:\n"
            "# The \"handy ruler\" below makes it easier to edit a package description.\n"
            "# Line up the first '|' above the ':' following the base package name, and\n"
            "# the '|' on the right side marks the last column you can put a character in.\n"
            "# You must make exactly 11 lines for the formatting to be correct.  It's also\n"
            "# customary to leave one space after the ':' except on otherwise blank lines.\n\n"
            f"{' ':>{handy_ruler}}|-----handy-ruler------------------------------------------------------|")

    def fix_quotation_mark(self) -> None:
        """ Autocorrect the quotation mark "" in the .info file. """
        for i, f in enumerate(self.fields):
            f: str = f.rstrip()

            if not f.startswith('"'):
                self.fields[i]: str = f'"{f}'

            if not f.endswith('"'):
                self.fields[i]: str = f'{self.fields[i]}"'

            if f == '' or f == '"':
                self.fields[i]: str = '""'

    @staticmethod
    def find_elements(start: str, stop: str, info_file: list) -> str:
        """ Find unknown elements between two elements in a list.
            Example:
                start: DOWNLOAD=a
                                b
                                c
                stop:  MD5SUM=d
                              e
                              f
                return:
                      a b c
        """
        begin, end, = 0, 0
        elements: list = []

        for i, info in enumerate(info_file):
            if info.startswith(start):
                begin: int = i
            if info.startswith(stop):
                end: int = i

        text: str = info_file[begin:end]

        for txt in text:
            txt: str = txt.replace('"', '')
            if start in txt:
                txt: str = txt.replace(start, '')
            elements.append(txt.strip())

        return ' '.join(elements)

    @staticmethod
    def info_find_element(tag, info_file: list):
        """ Find an element in a list. """
        for info in info_file:
            if info.startswith(tag):
                return info.split('=')[1].replace('"', '').strip()

    def checksum(self, md5sums: str) -> None:
        for source, md5 in zip(self.sources, md5sums.split()):
            if md5 != self.source_check_sum(source):
                message: str = f"\nMD5SUM check for {source} {self.color['red']}FAILED!{self.color['restore']}"
                self.dialog.msgbox(message, title=self.error_title, height=7,
                                   width=len(message) + 5)

    def source_check_sum(self, source: str) -> str:
        """ md5sum sources. """
        file: Path = Path(self.current_folder, source)
        if file.is_file():
            with open(file, 'rb') as f:
                data: bytes = f.read()
                return hashlib.md5(data).hexdigest()
        else:
            message: str = f"\nFile '{source}' not found."
            self.dialog.msgbox(message, title=self.error_title, height=7, width=len(message) + 5)
            self.main_menu()

    def write_info(self, file: Path) -> None:
        with open(file, 'w') as f:
            for line in self.data:
                if line.startswith(self.info_text[3]):
                    self.write_the_info_line(f, line, 3)

                elif line.startswith(self.info_text[4]):
                    self.write_the_info_line(f, line, 4)

                elif line.startswith(self.info_text[5]):
                    self.write_the_info_line(f, line, 5)

                elif line.startswith(self.info_text[6]):
                    self.write_the_info_line(f, line, 6)

                else:
                    f.write(f'{line}\n')

    def write_the_info_line(self, f, line: str, tag: int) -> None:
        """ Do the dirty job for the info file. """
        for i, ln in enumerate(line.split(), start=1):
            if i > 1:
                ln: str = f'{" " * (len(self.info_text[tag]) + 1)}{ln}'
            f.write(f'{ln}\n')

    def write_file(self, file: Path) -> None:
        with open(file, 'w') as f:
            for line in self.data:
                # Remove trailing whitespaces
                line: str = line.rstrip()
                f.write(f'{line}\n')

            # An empty line on the EOF
            if file.name == 'README':
                f.write('\n')
