import gettext
import os
import platform
import subprocess

import click


def get_current_language_windows():
    process = subprocess.Popen(['powershell', '-Command', '(Get-Culture).Name'], stdout=subprocess.PIPE)
    output, error = process.communicate()
    language = output.decode('utf-8').strip()
    return language


def get_current_language_macos():
    process = subprocess.Popen(['defaults', 'read', 'NSGlobalDomain', 'AppleLocale'], stdout=subprocess.PIPE)
    output, error = process.communicate()
    language = output.decode('utf-8').strip()
    return language


def get_current_language_linux():
    language = os.environ.get('LANG')
    return language


def get_current_language():
    if platform.system() == 'Windows':
        current_language = get_current_language_windows()
    elif platform.system() == 'Darwin':
        current_language = get_current_language_macos()
    else:
        current_language = get_current_language_linux()
    return current_language


if not os.path.exists('translations/zh_CN/LC_MESSAGES/messages.mo'):
    print('Translation file not found')


localedir = 'translations'
domain = 'messages'


# @click.group()
def set_language(language):
    t = gettext.translation(domain, localedir, languages=[language])
    t.install()


@click.group()
def cli():
    print()


@click.command()
@click.argument('name')
@click.option('--greeting', default='Hello', help='The greeting to use')
def greet(name, greeting):
    """Greet someone with a message"""
    message = f'{greeting}, {name}!'
    click.echo(message)


if __name__ == '__main__':
    # set_language(get_current_language())
    # cli()
    greet()
