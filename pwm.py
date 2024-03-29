#!/usr/bin/env python3

from scripts import encryptor, decryptor
from getpass import getpass
from os import listdir, remove, mkdir, system
from os.path import join, isfile, isdir
from shutil import rmtree
from sys import path
from time import sleep

# In case I want to add a delay between commands to make it seem like it's working :)
DELAY = 0
PATH = join(path[0], "db")
ACCPATH = join(PATH, "accs")

# If necessary folders don't exist, create them
if not isdir(PATH):
    mkdir(PATH)
if not isdir(ACCPATH):
    mkdir(ACCPATH)


# --- Functions ---
def welcome() -> None:
    """Print the header"""
    print("\n" + "\n" + "*" * 45)
    print("Commands:")
    print("exit | q     — quit the program")
    print("add  | a     — add new account data")
    print("read | r     — get existing account data")
    print("ls   | l     — show the list of accounts")
    print("rm   | d     — delete existing account data")
    print("clear        — clear the screen")
    print("reset        — reset PWM password")
    print("*" * 45)


def verify_passphrase(passphrase: str) -> bool:
    """Verify PWM Password"""
    with open(join(PATH, ".passphrase"), "r") as f:
        data = f.read()
    return passphrase == data


def passphrase_exists() -> bool:
    """Check if PWM Password"""
    return isfile(join(PATH, ".passphrase"))


def create_passphrase() -> None:
    """Create new PWM Password"""
    passphrase = input("Create your PWM password: ")
    with open(join(PATH, ".passphrase"), "w") as f:
        f.write(passphrase)


def delete_passphrase() -> None:
    """Delete PWM Password and all data from db/accs folder"""
    remove(join(PATH, ".passphrase"))
    rmtree(ACCPATH)
    print("Password reset successfully. Restart PWM to create a new password.")


def get_list_of_filenames() -> list:
    """Get the list of files in db/accs folder without .dat extension"""
    # Get the list of files
    files = listdir(ACCPATH)
    # Return a sorted list of filenames without extension
    return sorted([file.split(".")[0] for file in files])


def check_accname_for_matches_and_perform_action(
    accname: str, action, filenames: list, passphrase=""
) -> None:
    """
    This function does main work for rm and read commands. It's main purpose is to suggest
    to user the account names to read from or delete based on what the input is closest to.
    Example: Input: 'Am' => Suggestion 'Amazon'
    """
    match_found = False
    # Check if accountname exists in filenames
    for name in filenames:
        # If it fully matches
        if accname == name:
            match_found = True
            # passphrase is needed for print_account_data action
            action(accname) if not passphrase else action(accname, passphrase)
            break
        # If it matches partially, suggest the one match
        elif accname in name:
            answer = input(f"Did you mean {name}? ")
            # Yes or Enter confirms it
            if answer.lower() in ["yes", "y", "ye", "\n"]:
                match_found = True
                action(name) if not passphrase else action(name, passphrase)
                break
    if not match_found:
        print("Try again or enter a new command.")


def add_account(accname: str, acclogin: str, accpassw: str, passphrase: str) -> None:
    """I chose good function names so it's pretty clear that this function adds an acc to db"""
    # Create the message
    data = acclogin + " " + accpassw

    # Save the data
    outfile = join(ACCPATH, accname + ".dat")
    token = encryptor.encrypt(data, passphrase)
    with open(outfile, "wb") as file:
        file.write(token)
    print("Data saved successfully.")


def print_account_data(accname: str, passphrase: str) -> None:
    """Read login and password for the given account in the database"""
    infile = join(ACCPATH, accname + ".dat")

    try:
        # Access the data
        with open(infile, "rb") as file:
            token = file.read()
        data = decryptor.decrypt(token, passphrase)
        acclogin = data.split(" ")[0]
        accpassw = data.split(" ")[1]

        # Print the data
        print("\n" + "Your " + accname + " data:")
        print("Login: " + acclogin)
        print("Password: " + accpassw)

    except FileNotFoundError:
        print("There's no such account in the database.")


def delete_account(accname: str) -> None:
    """Deletes an account from the database"""
    filepath = join(ACCPATH, accname + ".dat")
    remove(filepath)
    print("Account successfully deleted.")


def main():
    if not passphrase_exists():
        create_passphrase()
        print("PWM password created successfully.")
        print("Restart PWM.")
        return

    passphrase = getpass("Enter your PWM password: ")

    if not verify_passphrase(passphrase):
        print("Wrong Password.")
        print("Restart PWM to try again.")
        sleep(DELAY)
        return

    # Actual Program
    welcome()
    while True:
        input_ = input("\n" + ": ")

        if input_ in ["exit", "q"]:
            _ = system("clear")
            break

        elif input_ in ["add", "a"]:
            # Get the data
            accname = input("Name of the account: ")
            acclogin = input("Login: ")
            accpassw = input("Password: ")
            add_account(accname, acclogin, accpassw, passphrase)
            sleep(DELAY)

        elif input_ in ["read", "r"]:
            # Get the name
            accname = input("Name of the account: ")
            filenames = get_list_of_filenames()
            check_accname_for_matches_and_perform_action(
                accname, print_account_data, filenames, passphrase
            )
            sleep(DELAY)

        elif input_ in ["ls", "l"]:
            filenames = get_list_of_filenames()
            if not filenames:
                print("List of accounts is empty.")
                continue
            print("\n" + "List of accounts:")
            for pos, file in enumerate(filenames):
                print(f"{pos+1}: {file}")
            sleep(DELAY)

        elif input_ in ["rm", "d"]:
            filenames = get_list_of_filenames()
            # Check if there are any files
            if not filenames:
                print("List of accounts is empty.")
                continue
            accname = input("Name of the account to delete: ")
            # If '*' is given, delete whole database
            if accname == "*":
                answer = input("Are you sure you want to delete all accounts? ")
                # Only yes confirms since consequenses are more serious
                if answer.lower() == "yes":
                    rmtree(ACCPATH)
                    mkdir(ACCPATH)
                    print("All accounts have been successfully deleted.")
                elif answer.lower() in ["no", "n"]:
                    pass
                else:
                    print(
                        "To confirm deletion of all accounts",
                        'you need to type in "yes"',
                    )
            else:
                check_accname_for_matches_and_perform_action(
                    accname, delete_account, filenames
                )
            sleep(DELAY)

        elif input_ == "clear":
            _ = system("clear")
            welcome()

        elif input_ == "reset":
            answer = input(
                "WARNING: All accounts will be deleted. Do you want to continue? "
            )
            if answer.lower() == "yes":
                delete_passphrase()
                break
            elif answer.lower() in ["no", "n"]:
                pass
            else:
                print(
                    "To confirm password reset",
                    'you need to type in "yes"',
                )

        else:
            print("Unknown Command")
            sleep(DELAY)


if __name__ == "__main__":
    main()
