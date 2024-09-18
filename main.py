import db_setup
from db_commands import PasswordManager
import os
import pwinput
import sqlite3
import random
import string
import pyperclip


# create function to generate random password
def generate_password(length=16):
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    return password


# options function to clean up main menu. we will move out of main.py later
def options():
    input('''What else would you like to do today?: 
                    [1] Retrieve password
                    [2] Store password
                    [3] Logout''')
    choice = input('')
    return choice


# main menu function to clean up main function. we will move out of main.py later
def main_menu(pm):
    # have to wrap in a loop in order to keep command line running after commands.
    while True:
        print('-------------------------------------------')
        print('''Welcome back! What would you like to do today?:
                [1] Retrieve password
                [2] Store password
                [3] Edit password
                [4] Logout''')
        choice = input('')
        if choice == '1':
            print('-------------------------------------------')
            print('Awesome! Let\'s get started.')
            #pm.get_password(website=input('What website are we logging into today: '))
            print('What website are we logging into today?')
            website = pm.get_available_websites()
            if website is not None:
                pm.get_password(website=website)
            else:
                print('No website selected or available.')
            print('''Is there anything else you need today?: y/n ''')
            if input('').lower() != 'y':
                pm.logout()
                break
            continue
        elif choice == '2':
            print('-------------------------------------------')
            print('Awesome! Let\'s get started.')
            pm.add_password(website=input('Which website is this password for: '),
                            username=input('What is your username: '),
                            password=pwinput.pwinput(prompt='Enter your password: '))
            print('''Is there anything else you need today?: y/n ''')
            if input('').lower() != 'y':
                pm.logout()
                break
        elif choice == '3':
            print('-------------------------------------------')
            print('Awesome! Let\'s get started.')
            pm.edit_password(website=input('Which website is this password for: '),
                             password=pwinput.pwinput(prompt='Enter your password: '))
            print('''Is there anything else you need today?: y/n ''')
            if input('').lower() != 'y':
                pm.logout()
                break
        elif choice == '4':
            pm.logout()
            break
        else:
            print("Invalid option, please try again.")
            continue


def main():
    # Get path to the database
    script_dir = os.path.dirname(__file__)
    db_path = os.path.join(script_dir, 'password_manager.db')
    pm = PasswordManager(db_name=db_path)
    pm.db_connection()

    # Generate a secure password for the user and save to variable
    secure_password = generate_password()

    print('---------------------------------------------')
    print('-Hello and welcome to your password manager!-')
    print('---------------------------------------------')
    print('''Please log in or create an account: 
            [1] Login
            [2] Register User''')
    choice = input('')
    if choice == '1':
        print('-------------------------------------------')
        pm.login()
        main_menu(pm)
    elif choice == '2':
        print('-------------------------------------------')
        print('Awesome! Let\'s get started.')
        pm.register_user(username=input('Please enter your unique username: '),
                         master_password=input('Please enter your master password: '))
        while True:
            print('-------------------------------------------')
            pm.login()
            main_menu(pm)
    else:
        print('Invalid choice. Please try again.')

    pm.db_close()


if __name__ == '__main__':
    main()
