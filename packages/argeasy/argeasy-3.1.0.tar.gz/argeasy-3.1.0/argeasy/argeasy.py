import sys
from typing import Union

from . import exceptions
from .arguments import Arguments

_ACTIONS = (
    'store_true',
    'store_false',
    'append',
    'default'
)


class ArgEasy(object):
    def __init__(self, name: str = None, description: str = None,
                 version: str = '1.0.0', usage: str = None) -> None:
        """Create a new instance of ArgEasy.

        :param name: Application name, defaults to None
        :type name: str, optional
        :param description: Application description, defaults to None
        :type description: str, optional
        :param version: Application version, defaults to "1.0.0"
        :type version: str, optional
        :param usage: Application usage format, defaults to none
        :type usage: str, optional
        """

        self._commands = {}
        self._parsed = Arguments()

        self._project_name = name
        self._description = description
        self._version = version

        if not usage:
            usage = f'{name} [--version] [--help] <command> <args>'

        self._usage = usage

        self.add_flag('--help', 'Show program help message', action='store_true')
        self.add_flag('--version', 'Show program version', action='store_true')

    def _help(self) -> None:
        print(f'{self._project_name} ({self._version})')
        print(f'usage: {self._usage}\n')

        if self._description:
            print(self._description)

        print(f'\nCommands and flags help:')

        for cmd, info in self._commands.items():
            print(f'    \033[1m{cmd}\033[m: \033[33m{info["help"]}\033[m')

        sys.exit(0)

    def _show_version(self) -> None:
        print(f'{self._project_name} (\033[33m{self._version}\033[m)')
        sys.exit(0)

    def _invalid_use_msg(self, cmd: str) -> None:
        print(f'\033[31minvalid use from {repr(cmd)} command\033[m')
        print(f'\033[33muse \'--help\' flag to see all commands\033[m')
        sys.exit(1)

    def add_argument(self, name: str, help: str, action: str = 'default',
                     max_append: Union[str, int] = '*') -> None:
        """Adds a new argument.

        The available actions are:
        `default` (returns the next argument as value),
        `store_true`, `store_false`, and `append`.

        :param name: Argument name
        :type name: str
        :param help: Argument help message
        :type help: str
        :param action: Action to be taken if argument is
        available, defaults to 'default'
        :type action: str, optional
        :param max_append: If the action is "append", this
        parameter defines the maximum number of elements, defaults to '*'
        :type max_append: Union[str, int], optional
        :raises exceptions.InvalidActionError: Raised if inexistent action
        """

        if action not in _ACTIONS:
            raise exceptions.InvalidActionError(f'Action {repr(action)} invalid')

        self._commands[name] = {
            'help': help,
            'action': action,
            'max_append': max_append
        }

        name = name.replace('-', '_')
        setattr(self._parsed, name, None)

    def add_flag(self, name: str, help: str, action: str = 'default',
                 max_append: Union[str, int] = '*') -> None:
        """Adds a new flag. The flag name can have
        one or two hyphens.

        The available actions are:
        `default` (returns the next argument as value),
        `store_true`, `store_false`, and `append`.

        :param name: Flag name
        :type name: str
        :param help: Flag help message
        :type help: str
        :param action: Action to be taken if flag is
        available, defaults to 'default'
        :type action: str, optional
        :param max_append: If the action is "append", this
        parameter defines the maximum number of elements, defaults to '*'
        :type max_append: Union[str, int], optional
        :raises exceptions.InvalidActionError: Raised if inexistent action
        """

        if action not in _ACTIONS:
            raise exceptions.InvalidActionError(f'Action {repr(action)} invalid')

        self._commands[name] = {
            'help': help,
            'action': action,
            'max_append': max_append
        }

        name = name.strip('-')
        name = name.replace('-', '_')

        setattr(self._parsed, name, None)

    def _parse_cmd(self, cmd: str, params: list) -> list:
        cmd_action = self._commands[cmd]['action']

        if cmd_action == 'store_true':
            param = True
        elif cmd_action == 'store_false':
            param = False
        elif cmd_action == 'default':
            try:
                param = params[0]
            except IndexError:
                self._invalid_use_msg(cmd)

            if param.startswith('-') or len(params) > 1:
                self._invalid_use_msg(cmd)
        elif cmd_action == 'append':
            max_append = self._commands[cmd]['max_append']

            if max_append == '*':
                param = params
            else:
                if len(params) > max_append:
                    print(f'\033[31mcommand {repr(cmd)} supports up to {max_append} elements\033[m')
                    print('\033[33muse \'--help\' flag to see all commands\033[m')
                    sys.exit(1)

                param = params[0:max_append - 1]

        cmd = cmd.strip('-')
        cmd = cmd.replace('-', '_')
        setattr(self._parsed, cmd, param)

    def parse(self) -> None:
        cli_args = sys.argv[1:]

        if not cli_args:
            self._help()
            sys.exit(1)

        recognized_cmd = []
        commands = {}

        for index, cmd in enumerate(cli_args):
            if cmd in self._commands:
                recognized_cmd.append(index)
            elif cmd not in self._commands and cmd.startswith('-'):
                print(f'\033[31mflag {repr(cmd)} unrecognized\033[m')
                print(f'\033[33muse "--help" flag to see all commands\033[m')
                sys.exit(1)

        recognized_cmd.append(len(cli_args))

        for i, cmd_index in enumerate(recognized_cmd):
            if (i + 1) > (len(recognized_cmd) - 1):
                break

            next_cmd_i = recognized_cmd[i + 1]
            cmd_params = cli_args[cmd_index + 1:next_cmd_i]
            cmd_name = cli_args[cmd_index]
            commands[cmd_name] = cmd_params

        for cmd, params in commands.items():
            self._parse_cmd(cmd, params)

        if self._parsed.help:
            self._help()
        elif self._parsed.version:
            self._show_version()

        return self._parsed
