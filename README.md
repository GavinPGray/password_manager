This is a password manager created in python. It's my first actual python project. I originally came from JavaScript and started learning python for some project I have planned. 

The project works by allowing users to log in or register themselves first. Once you are registered you can log in and store passwords, retrieve passwords, and edit passwords. It uses bcrypt for encryption. When you store a password the password is hashed
and salted before being saved to a local SQLite database. This is used so that if someone was able to get a hold of your database it won't show the passwords in plain text. 

In order to use this you'll need to first run the command to create your database. Once created you'll be able to use this password manager in the command line. A cool feature is that you'd be able to store this on a flashdrive that only You'll have 
access to for added security. It also makes it a bit more portable for you since the database is local and it won't have to be stored on your physical machine. 
