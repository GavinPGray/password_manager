import sqlite3
import bcrypt
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import pwinput


class PasswordManager:
    def __init__(self, db_name='password_manager.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.current_user = None
        self.fernet = None

    def db_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print('Connection to database is successful')
        except sqlite3.Error as e:
            print(f'Error connecting to database: {e}')
            raise

    def db_close(self):
        if self.conn:
            self.conn.close()
            print('Connection to database is closed')

    def register_user(self, username, master_password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(master_password.encode('utf-8'), salt)

        # derive key from master password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

        # Generate a Fernet key and encrypt it
        fernet_key = Fernet.generate_key()
        f = Fernet(key)
        encrypted_key = f.encrypt(fernet_key)

        try:
            self.cursor.execute('''
                INSERT INTO users(username, hashed_password, salt, encrypted_key)
                VALUES(?, ?, ?, ?)
            ''', (username, hashed_password, salt, encrypted_key))
            self.conn.commit()
            print('User registered successfully')
        except sqlite3.IntegrityError:
            print('Username already exists')

    def login(self):
        while True:
            username = input('Login: ')
            master_password = pwinput.pwinput('Enter your password: ')

            self.cursor.execute('''
                SELECT id, hashed_password, salt, encrypted_key FROM users WHERE username = ?
            ''', (username,))
            user = self.cursor.fetchone()

            if user and bcrypt.checkpw(master_password.encode('utf-8'), user[1]):
                self.current_user = user[0]
                salt = user[2]
                encrypted_key = user[3]

                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=salt,
                    iterations=100000,
                    backend=default_backend()
                )
                derived_key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
                f = Fernet(derived_key)
                decrypted_key = f.decrypt(encrypted_key)

                self.fernet = Fernet(decrypted_key)

                print('Login successful')
                break
            else:
                print('Invalid username or password please try again')

    def add_password(self, website, username, password):
        if not self.current_user:
            print('You need to login first')
            input('Press Enter to continue')
            return
        encrypted_password = self.fernet.encrypt(password.encode())
        self.cursor.execute('''
            INSERT INTO passwords(user_id, website, username, encrypted_password)
            VALUES(?, ?, ?, ?)
        ''', (self.current_user, website, username, encrypted_password))
        self.conn.commit()
        print('Password added successfully')
        input('Press Enter to continue')

    def get_available_websites(self):
        self.cursor.execute('''
            SELECT website FROM passwords WHERE user_id = ?
        ''', (self.current_user,))
        websites = self.cursor.fetchall()

        if not websites:
            print('No websites available')
            input('Press Enter to continue')
            return None
        else:
            print('Select a website from the list below:')
            for i, website in enumerate(websites):
                print(f'{i + 1}. {website[0]}')
            try:
                choice = int(input('Enter the number of the website: ')) - 1
                if choice < 0 or choice >= len(websites):
                    print('Invalid choice')
                    input('Press Enter to continue')
                    return None
                return websites[choice][0]
            except ValueError:
                print('Invalid choice. Please enter a number')
                input('Press Enter to continue')
                return None

    def get_password(self, website):

        self.cursor.execute('''
            SELECT username, encrypted_password FROM passwords
            WHERE user_id = ? AND website = ?
        ''', (self.current_user, website))
        result = self.cursor.fetchone()
        print(self.current_user, website)
        if result is None:
            print(f'Password not found for {website}')
            input('Press Enter to continue')
        else:
            decrypted_password = self.fernet.decrypt(result[1]).decode()
            print(f"username: {result[0]}, password: {decrypted_password}")
            input('Press Enter to continue')

    def edit_password(self, website, password):
        if not self.current_user:
            print('You need to login first')
            input('Press Enter to continue')
            return
        encrypted_password = self.fernet.encrypt(password.encode())
        self.cursor.execute('''
            UPDATE passwords SET encrypted_password = ?
            WHERE user_id = ? AND website = ?
        ''', (encrypted_password, self.current_user, website))
        self.conn.commit()
        print('Password updated successfully')
        input('Press Enter to continue')

    def logout(self):
        self.current_user = None
        self.fernet = None
        print('Logged out successfully')
        input('Press Enter to continue')


