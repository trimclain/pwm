#!/usr/bin/env python3

from scripts import encryptor, decryptor
from getpass import getpass
from os import listdir, remove, mkdir, system
from os.path import join, isfile, isdir
from sys import path
from time import sleep

DELAY = 0.1
PATH = join(path[0], 'db')
ACCPATH = join(PATH, 'accs')
# If folders don't exist, create them
if not isdir(PATH):
    mkdir(PATH)
if not isdir(ACCPATH):
    mkdir(ACCPATH)

# --- Functions ---
def welcome() -> None:
    print('\n' + '\n' + '*'*45)
    print('Commands:')
    print('exit — quit the program')
    print('add — add new account data')
    print('get — get existing account data')
    print('ls — show the list of accounts')
    print('rm — delete existing account data')
    print('clear — clear the screen')
    print('*'*45)

def verify_passphrase(passphrase: str) -> bool:
    with open(join(PATH, '.passphrase'), 'r') as f:
        data = f.read()
    if passphrase == data:
        return True
    return False

def passphrase_exists() -> bool:
    if isfile(join(PATH, '.passphrase')):
        return True
    return False

def create_passphrase() -> None:
    passphrase = input('Create your PWM password: ')
    with open(join(PATH, '.passphrase'), 'w') as f:
        f.write(passphrase)


if __name__ == '__main__':
    if passphrase_exists():
        passphrase = getpass('Enter your PWM password: ')
        if verify_passphrase(passphrase):

            # Program
            welcome()
            while True:
                input_ = input('\n' + ': ')

                if input_ == 'exit' or input_ == 'quit' or input_ == 'q':
                    _ = system('clear')
                    break

                elif input_ == 'add':
                    # Get the data
                    accname = input('Name of the account: ')
                    acclogin = input('Login: ')
                    accpassw = input('Password: ')

                    # Create the message
                    data = acclogin + ' ' + accpassw

                    # Save the data
                    outfile = join(ACCPATH, accname + '.dat')
                    token = encryptor.encrypt(data, passphrase)
                    with open(outfile, 'wb') as file:
                        file.write(token)
                    print('Data saved successfully.')
                    sleep(DELAY)

                elif input_ == 'get':
                    # Get the name
                    accname = input('Name of the account: ')
                    infile = join(ACCPATH, accname + '.dat')

                    try:
                        # Access the data
                        with open(infile, 'rb') as file:
                            token = file.read()
                        data = decryptor.decrypt(token, passphrase)
                        acclogin = data.split(' ')[0]
                        accpassw = data.split(' ')[1]

                        # Print the data
                        print('\n' + 'Your ' + accname + ' data:')
                        print('Login: ' + acclogin)
                        print('Password: ' + accpassw)
                        sleep(DELAY)

                    except FileNotFoundError:
                        print('There\'s no such account in the database.')
                        sleep(DELAY)

                elif input_ == 'ls':
                    files = listdir(ACCPATH)
                    filenames = [file.split('.')[0] for file in files]
                    if filenames:
                        print('\n' + 'List of accounts:')
                        for pos, file in enumerate(filenames):
                            print(f'{pos+1}: {file}')
                    else:
                        print('List of accounts is empty.')
                    sleep(DELAY)

                elif input_ == 'rm':
                    accname = input('Name of the website to delete: ')
                    filepath = join(ACCPATH, accname + '.dat')
                    remove(filepath)
                    print('Account successfully deleted.')
                    sleep(DELAY)

                elif input_ == 'clear':
                    _ = system('clear')
                    welcome()

                else:
                    print('Unknown Command')
                    sleep(DELAY)
        else:
            print('Wrong Password.')
            print('Reastart pwm to try again.')
            sleep(DELAY)

    else:
        create_passphrase()
        print('PWM password created successfully.')
        print('Restart pwm.')
