import sqlite3
from colorama import Fore, Style, init
import hashlib
import getpass
from cryptography.fernet import Fernet
import os.path
import win32console, win32gui, win32con
import win32api
import sys
import time
import ctypes
from datetime import datetime

try:
    ctypes.windll.kernel32.SetConsoleTitleW("Vault")
    init(convert=True)
    hwnd = win32console.GetConsoleWindow()
    if hwnd:
        hMenu = win32gui.GetSystemMenu(hwnd, 0)
        if hMenu:
            win32gui.DeleteMenu(hMenu, win32con.SC_CLOSE, win32con.MF_BYCOMMAND) #disable the exit button on the console window
    conn = sqlite3.connect('password.db') #connect to the database named password. It will create one if it does not already exist
    c = conn.cursor() #initialize the cursor to manipulate the database

    print(Fore.LIGHTBLACK_EX + "==============================================================================================            ")
    print("|\????????????????????????????????????????????????????????????????????????????????????????????\           ")
    print("| \????????????????????????????????????????????????????????????????????????????????????????????\          ")
    print("|  \????????????????????????????????????????????????????????????????????????????????????????????\         ")
    print("\   \????????????????????????????????????????????????????????????????????????????????????????????\        ")
    print(" \   \?????????????????" + Style.RESET_ALL + Fore.LIGHTBLUE_EX + " Password Manager" + Style.RESET_ALL + Fore.LIGHTBLACK_EX + " ?????????????????????????????????????????????????????????\       ")
    print("  \   \??????????????????????????? " + Style.RESET_ALL + Fore.LIGHTBLUE_EX + "-Dedicated to all those who keep forgetting their passwords." + Style.RESET_ALL + Fore.LIGHTBLACK_EX + "????\      ")
    print("   \   \????????????????????????????????????????????????????????????????????????????????????????????\     ")
    print("    \   \?????????????????????????????????????????????????????????????????? " + Style.RESET_ALL + Fore.YELLOW + "Made By :-" + Style.RESET_ALL + Fore.LIGHTBLACK_EX + " ??????????????\    ")
    print("     \   \???????????????????????????????????????????????????????????????????? " + Style.RESET_ALL + Fore.YELLOW + "Debjeet Das " + Style.RESET_ALL + Fore.LIGHTBLACK_EX + "???????????\   ")
    print("      \	  \????????????????????????????????????????????????????????????????????????????????????????????\  ")
    print("       \   ============================================================================================== ")
    print("        \  |											         |")
    print("         \ |											         |")
    print("          \|=============================================================================================|" + Style.RESET_ALL)
    def set_exit_handler(func):
        win32api.SetConsoleCtrlHandler(func, True)

    def on_exit(sig, func=None): #secure the database if the user closes the application abruptly
        print(Fore.LIGHTRED_EX + "\nPlease try to avoid closing abrubtly unless absolutely necessary.(Use the quit option provided)" + Style.RESET_ALL)
        unhide()
        decrypt_now()
        encrypt_now()
        hide()
        time.sleep(5)

    set_exit_handler(on_exit)
    
    def quit_now(): #function to handle the quit option
        unhide()
        decrypt_now()
        encrypt_now()
        hide()
        exit()

    def hide(): #function to hide the database and the key to prevent from accidental deletion
        if os.path.exists("password.db"):
            os.system('cmd /c "attrib +s +h password.db"')
        if os.path.exists("key.key"):
            os.system('cmd /c "attrib +s +h key.key"')
            
    def unhide(): #function to unhide database and key before use
        if os.path.exists("password.db"):
            os.system('cmd /c "attrib -s -h password.db"')
        if os.path.exists("key.key"):
            os.system('cmd /c "attrib -s -h key.key"')
            
    def write_key():
            """
            Generates a key and save it into a file
            """
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)

    def load_key():
            """
            Loads the key from the current directory named `key.key`
            """
            return open("key.key", "rb").read()

    def encrypt(filename, key):
            """
            Given a filename (str) and key (bytes), it encrypts the file and write it
            """
            f = Fernet(key)
            with open(filename, "rb") as file:
                # read all file data
                file_data = file.read()
            # encrypt data
            encrypted_data = f.encrypt(file_data)
            # write the encrypted file
            with open(filename, "wb") as file:
                file.write(encrypted_data)

    def decrypt(filename, key):
            """
            Given a filename (str) and key (bytes), it decrypts the file and write it
            """
            f = Fernet(key)
            with open(filename, "rb") as file:
                # read the encrypted data
                encrypted_data = file.read()
            # decrypt data
            decrypted_data = f.decrypt(encrypted_data)
            # write the original file
            with open(filename, "wb") as file:
                file.write(decrypted_data)

    def authorize(): #function to ask user to set a username and password which will be required to access the application
        try:
            print(Fore.CYAN + "\nSet your username and password(you would use this to log in later on.Without this you would not be able to access the password manager)" + Style.RESET_ALL)
            print(Fore.RED + "\nPlease remember just this password.If you forget this, even the person who made this software cannot recover it.And !!SET A STRONG PASSWORD!!" + Style.RESET_ALL)
            pass_website = "root"
            print(Fore.LIGHTRED_EX + "\n[=]" + Style.RESET_ALL + "Enter username: ")
            pass_username = getpass.getpass(">>> ")
            message = pass_username.encode()
            hash_username = hashlib.blake2b(message).hexdigest()
            print(Fore.LIGHTRED_EX + "[=]" + Style.RESET_ALL + "Enter password: ")
            pass_password = getpass.getpass(">>> ")
            message = pass_password.encode()
            hash_password = hashlib.blake2b(message).hexdigest() #store the username and password in hashed form
            if pass_password == '' or pass_username == '':
                    print(Fore.RED + "An input field is empty.Please fill up everything correctly.\n" + Style.RESET_ALL)
                    authorize()
            c.execute("INSERT INTO password (website, username, password) VALUES (?, ?, ?)", (pass_website, hash_username, hash_password)) #sqlite3 command to save the username and password for future use
            conn.commit()
            print(Fore.LIGHTGREEN_EX + "[+] Password successfully added.\n" + Style.RESET_ALL)
            main()
        except KeyboardInterrupt: #catch if keyboard interrupt is pressed and prevent it.
            print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
            authorize()
            
    def create_table(): #function to create a table inside the database
        try:
            c.execute('CREATE TABLE IF NOT EXISTS password(website TEXT, username TEXT, password TEXT, date TEXT, time TEXT)')
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
            main()
            
    def password_entry(): #function to store new password
            try:
                    print(Fore.LIGHTCYAN_EX + "\n[.]" + Style.RESET_ALL + "Enter the website name")
                    print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                    website_name = input()
                    if website_name == '':
                            print(Fore.RED + "You did not enter website name.Returning to start Menu\n" + Style.RESET_ALL)
                            run()
                    if website_name == 'root':
                            print(Fore.LIGHTRED_EX + "Sorry. You cannot enter 'root' as website.It has restricted access.\n" + Style.RESET_ALL)
                            password_entry()
                    c.execute('SELECT website FROM password')
                    data = c.fetchall()
                    for i in data: #checks if website name already exists in database.
                            if website_name == i[0]:
                                    print(Fore.LIGHTBLACK_EX + "[!!] Website entered already exists in database\n" + Style.RESET_ALL)
                                    run()
                    print(Fore.LIGHTCYAN_EX + "[.]" + Style.RESET_ALL + "Enter the username")
                    print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                    user_name = input()
                    if user_name == '':
                        print(Fore.RED + "No username entered.Returning to start Menu\n" + Style.RESET_ALL)
                        run()
                    print(Fore.LIGHTCYAN_EX + "[.]" + Style.RESET_ALL + "Enter the password")
                    print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                    pass_word = input()
                    if pass_word == '':
                            print(Fore.RED + "No password entered.Returning to start Menu\n" + Style.RESET_ALL)
                            run()
                    time_date = datetime.now()
                    insert_date = time_date.strftime("%B %d ,%Y")
                    insert_time = time_date.strftime("%H Hours %M Minutes %S Seconds")
                    c.execute("INSERT INTO password (website, username, password, date, time) VALUES (?, ?, ?, ?, ?)", (website_name, user_name, pass_word, insert_date, insert_time))
                    conn.commit()
                    print(Fore.LIGHTGREEN_EX + "\n[+] Password Successfully stored\n" + Style.RESET_ALL)
            except KeyboardInterrupt:
                    print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
                    run()
                
    def read_from_db(): #function to read information about previously stored password
            try:
                    print(Fore.LIGHTMAGENTA_EX + "[.]" + Style.RESET_ALL + "Enter the website name for which password is to be extracted")
                    print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                    read_website = input()
                    if read_website == '':
                            print(Fore.RED + "You did not enter a website name.Returning to start Menu\n" + Style.RESET_ALL)
                            run()
                    if read_website == 'root':
                            print(Fore.LIGHTRED_EX + "Sorry.Not able to display anything related to root.Restricted Acess." + Style.RESET_ALL)
                            read_from_db()
                    c.execute('SELECT * FROM password WHERE website=?', (read_website,))
                    data = c.fetchone()
                    print(Fore.LIGHTMAGENTA_EX + "\n==============================================================================================================" + Style.RESET_ALL)
                    print(Fore.GREEN + "Website = " +Style.RESET_ALL + data[0])
                    print(Fore.YELLOW + "Username = " +Style.RESET_ALL + data[1])
                    print(Fore.CYAN + "Password = " +Style.RESET_ALL + data[2])
                    print(Fore.LIGHTGREEN_EX + "\nPassword Added on" + Style.RESET_ALL)
                    print(Fore.LIGHTYELLOW_EX + "Date = " + Style.RESET_ALL + data[3])
                    print(Fore.LIGHTBLUE_EX + "Time = " + Style.RESET_ALL + data[4])
                    print(Fore.LIGHTMAGENTA_EX + "==============================================================================================================" + Style.RESET_ALL)
            except TypeError: #if a query does not exist in database, it throws a TypeError error
                    print(Fore.LIGHTBLACK_EX + "\n[-] You have Never stored any information related to this website\n" + Style.RESET_ALL)
            except KeyboardInterrupt:
                    print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
                    run()
                    
    def print_all(): #function to list all the websites for which passwords have already been saved.
            try:
                    count = 0
                    c.execute('SELECT website FROM password')
                    data = c.fetchall()
                    for i in data:
                            count += 1
                            if i[0] == 'root':
                                    continue
                            print("\n" + i[0])
                    if count == 1:
                            print(Fore.LIGHTBLACK_EX + "There are no passwords currently in database." + Style.RESET_ALL)
                    else:
                            print(Fore.LIGHTGREEN_EX + "\n[*] These are All the websites that you have stored." + Style.RESET_ALL)
            except KeyboardInterrupt:
                    print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
                    run()
                    
    def update(): #function to update the username or password of a previously stored one
            try:
                    print(Fore.LIGHTBLUE_EX + "[.]" + Style.RESET_ALL + "Enter website for which username/password is to be updated.")
                    print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                    new_website = input()
                    if new_website == '':
                            print(Fore.RED + "You did not enter a website name.Returning to start Menu\n" + Style.RESET_ALL)
                            run()
                    if new_website == 'root':
                            print(Fore.RED + "Cannot update root username or password from here.Restricted access." + Style.RESET_ALL)
                            update()
                    track = 0
                    c.execute('SELECT website FROM password')
                    data = c.fetchall()
                    for i in data:
                            if new_website == i[0]:
                                    print(Fore.LIGHTBLUE_EX + "[.]" + Style.RESET_ALL + "Do you want to update username or password?")
                                    print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                                    choice = input()
                                    if choice == '':
                                            print(Fore.RED + "How is an empty space your choice?Please enter !!YOUR!! choice.\n" + Style.RESET_ALL)
                                            update()
                                    if choice == 'username':
                                            print(Fore.LIGHTBLUE_EX + "[.]" + Style.RESET_ALL + "Enter new username")
                                            print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                                            new_username = input()
                                            if new_username == '':
                                                    print(Fore.RED + "No username entered.Returning to start Menu\n" + Style.RESET_ALL)
                                                    run()
                                            c.execute('UPDATE password SET username=? WHERE website=?', (new_username, new_website,))
                                    elif choice == 'password':
                                            print(Fore.LIGHTBLUE_EX + "[.]" + Style.RESET_ALL + "Enter new password")
                                            print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                                            new_password = input()
                                            if new_password == '':
                                                    print(Fore.RED + "No password entered.Returning to start Menu\n" + Style.RESET_ALL)
                                                    run()
                                            c.execute('UPDATE password SET password=? WHERE website=?', (new_password, new_website,)) #sqlite3 command to update data in database
                                    else:
                                            print(Fore.LIGHTBLACK_EX + "[*]Wrong Choice entered.Please choose 'username' or 'password' only.\n" + Style.RESET_ALL)
                                    conn.commit()
                                    print(Fore.LIGHTGREEN_EX + "[+]" + choice + " successfully updated." + Style.RESET_ALL)
                                    track += 1
                                    break
                    if track == 0:
                            print(Fore.LIGHTBLACK_EX + "\nWebsite name entered does not even exist in database.\n" + Style.RESET_ALL)
                            run()
            except KeyboardInterrupt:
                    print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
                    run()
                    
    def delete(): #function to delete a website and its related username and password from the database.
            try:
                    print(Fore.LIGHTRED_EX + "[-]" + Style.RESET_ALL + Fore.LIGHTYELLOW_EX + " This would delete the username and password related to the website you enter.Continue(y/n)?" + Style.RESET_ALL)
                    choiceyesorno = input(">>> ")
                    if choiceyesorno == 'y':
                        print(Fore.CYAN + "[?]" + Style.RESET_ALL + " Enter Your username: ")
                        old_username = getpass.getpass(">>> ")
                        message0 = old_username.encode()
                        hash_old_username = hashlib.blake2b(message0).hexdigest()
                        print(Fore.CYAN + "[?]" + Style.RESET_ALL + " Enter Your password: ")
                        old_password = getpass.getpass(">>> ")
                        message1 = old_password.encode()
                        hash_old_password = hashlib.blake2b(message1).hexdigest()
                        if old_username == '' or old_password == '':
                                print(Fore.RED + "No username or password entered.Returning to start Menu." + Style.RESET_ALL)
                                run()
                        c.execute("SELECT * FROM password WHERE website='root'")
                        data = c.fetchone()
                        if hash_old_username == data[1] and hash_old_password == data[2]:
                            print(Fore.LIGHTGREEN_EX + "[<>] Access Granted!" + Style.RESET_ALL)
                            print(Fore.LIGHTRED_EX + "[.]" + Style.RESET_ALL + "Enter website for which username and password is to be deleted")
                            print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                            delete_username = input()
                            track_delete = 0
                            if delete_username == '':
                                    print(Fore.RED + "No website name entered.Returning to start Menu\n" + Style.RESET_ALL)
                                    run()
                            if delete_username == 'root':
                                    print(Fore.RED + "Cannot delete root username or password from here.Restricted Access." + Style.RESET_ALL)
                                    delete()
                            c.execute('SELECT website FROM password')
                            data = c.fetchall()
                            for i in data:
                                    if delete_username == i[0]:
                                            c.execute('DELETE FROM password WHERE website=?', (delete_username,))
                                            conn.commit()
                                            print(Fore.LIGHTGREEN_EX + "\n[+]" + delete_username + " username and password successfully deleted." + Style.RESET_ALL)
                                            track_delete += 1
                                            break
                            if track_delete == 0:
                                    print(Fore.LIGHTBLACK_EX + "\nWebsite name entered does not even exist in database.\n" + Style.RESET_ALL)
                                    run()
                        else:
                            print(Fore.RED + "Wrong username or password entered.Unable to update." + Style.RESET_ALL)
                            main()
                    elif choiceyesorno == 'n':
                        run()
                    else:
                        print(Fore.RED + "[*] Wrong choice entered.Please enter y or n only." + Style.RESET_ALL)
                        run()
            except KeyboardInterrupt:
                    print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
                    run()
                    
    def update_root(): #function to update root username or password.(the one that is required to acess the application)
        try:
            print(Fore.LIGHTRED_EX + "\n[*]" + Style.RESET_ALL + Fore.LIGHTYELLOW_EX + "This would change your root username or password.Continue?(y/n)" + Style.RESET_ALL)
            yesorno = input(">>> ")
            if yesorno == '':
                    print(Fore.RED + "How can Your Choice be Blank?Please try again." + Style.RESET_ALL)
                    update_root()
            if yesorno == 'y':
                    print(Fore.LIGHTCYAN_EX + "[?]" + Style.RESET_ALL + " Enter old username: ")
                    old_username = getpass.getpass(">>> ")
                    message0 = old_username.encode()
                    hash_old_username = hashlib.blake2b(message0).hexdigest()
                    print(Fore.LIGHTCYAN_EX + "[?]" + Style.RESET_ALL + " Enter old password: ")
                    old_password = getpass.getpass(">>> ")
                    message1 = old_password.encode()
                    hash_old_password = hashlib.blake2b(message1).hexdigest()
                    if old_username == '' or old_password == '':
                            print(Fore.RED + "No username or password entered.Returning to Start." + Style.RESET_ALL)
                            main()
                    c.execute("SELECT * FROM password WHERE website='root'")
                    data = c.fetchone()
                    if hash_old_username == data[1] and hash_old_password == data[2]:
                            print(Fore.LIGHTGREEN_EX + "[<>] Access Granted!" + Style.RESET_ALL)
                            print(Fore.LIGHTBLUE_EX + "[.]" + Style.RESET_ALL + "Do you want to update root username or password?")
                            print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                            choice = input()
                            if choice == '':
                                    print(Fore.RED + "How is an empty space your choice?Please enter !!YOUR!! choice.\n" + Style.RESET_ALL)
                                    update_root()
                            if choice == 'username':
                                    print(Fore.LIGHTBLUE_EX + "[.]" + Style.RESET_ALL + "Enter new username")
                                    new_username = getpass.getpass(">>> ")
                                    message3 = new_username.encode()
                                    hash_new_username = hashlib.blake2b(message3).hexdigest()
                                    if hash_new_username == data[1]:
                                        print(Fore.LIGHTWHITE_EX + "-------------------The old username cannot be the new username.-------------------" + Style.RESET_ALL)
                                        run()
                                    if new_username == '':
                                            print(Fore.RED + "No username entered.It is absolutely necessary to enter one at this point.\n" + Style.RESET_ALL)
                                            update_root()
                                    c.execute("UPDATE password SET username=? WHERE website='root'", (hash_new_username,))
                            elif choice == 'password':
                                    print(Fore.LIGHTBLUE_EX + "[.]" + Style.RESET_ALL + "Enter new password")
                                    new_password = getpass.getpass(">>> ")
                                    message4 = new_password.encode()
                                    hash_new_password = hashlib.blake2b(message4).hexdigest()
                                    if hash_new_password == data[2]:
                                        print(Fore.LIGHTWHITE_EX + "-------------------The old password cannot be the new password.-------------------" + Style.RESET_ALL)
                                        run()
                                    if new_password == '':
                                            print(Fore.RED + "No password entered.It is absolutely necessary to enter one at this point.\n" + Style.RESET_ALL)
                                            update_root()
                                    c.execute("UPDATE password SET password=? WHERE website='root'", (hash_new_password,))
                            else:
                                    print(Fore.LIGHTBLACK_EX + "[*]Wrong Choice entered.Please choose 'username' or 'password' only.\n" + Style.RESET_ALL)
                            conn.commit()
                            print(Fore.LIGHTGREEN_EX + "[+]" + choice + " for root successfully updated." + Style.RESET_ALL)
                            main()
                    else:
                            print(Fore.RED + "Wrong username or password entered.Unable to update." + Style.RESET_ALL)
                            main()
            elif yesorno == 'n':
                    run()
            else:
                    print(Fore.LIGHTRED_EX + "I don't think the option you selected was listed.Please try again." +Style.RESET_ALL)
                    update_root()
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
            main()
            
    def delete_table(): #this would delete your entire password records
        try:
            print(Fore.LIGHTYELLOW_EX + "\n[-]" + Style.RESET_ALL + Fore.LIGHTBLACK_EX + "This would delete your password record.Continue?(y/n)" + Style.RESET_ALL)
            yesorno = input(">>> ")
            if yesorno == '':
                    print(Fore.RED + "How can Your Choice be Blank?Please try again." + Style.RESET_ALL)
                    delete_root()
            if yesorno == 'y':
                    print(Fore.RED + "[?]" + Style.RESET_ALL + " Enter your username: ")
                    old_username = getpass.getpass(">>> ")
                    message = old_username.encode()
                    hash_old_username = hashlib.blake2b(message).hexdigest()
                    print(Fore.RED + "[?]" + Style.RESET_ALL + " Enter your password: ")
                    old_password = getpass.getpass(">>> ")
                    message1 = old_password.encode()
                    hash_old_password = hashlib.blake2b(message1).hexdigest()
                    if old_username == '' or old_password == '':
                            print(Fore.RED + "No username or password entered.Sensitive data is being modified.Please do enter the correct information." + Style.RESET_ALL)
                            main()
                    c.execute("SELECT * FROM password WHERE website='root'")
                    data = c.fetchone()
                    if hash_old_username == data[1] and hash_old_password == data[2]:
                            print(Fore.LIGHTGREEN_EX + "[<>] Access Granted!" + Style.RESET_ALL)
                            c.execute("DELETE FROM password")
                            conn.commit()
                            print(Fore.GREEN + "Database successfully deleted." + Style.RESET_ALL)
                            main()
                    else:
                            print(Fore.RED + "Wrong username or password entered.Unable to delete." + Style.RESET_ALL)
                            main()
            elif yesorno == 'n':
                    run()
            else:
                    print(Fore.LIGHTRED_EX + "I don't think the option you selected was listed.Please try again." +Style.RESET_ALL)
                    delete_root()
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
            main()

    def encrypt_now(): #this checks if files exist and encrypt it accordingly
        try:
            if os.path.exists("key.key"):
                    key = load_key()
                    file = "password.db"
                    encrypt(file, key)
            else:
                    write_key()
                    key = load_key()
                    file = "password.db"
                    encrypt(file, key)
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
            main()
            
    def decrypt_now(): #checks if file is encrypted or decrypted and decrypts accordingly
            try:
                    if os.path.exists("key.key") and os.path.exists("password.db"):
                            key = load_key()
                            file = "password.db"
                            decrypt(file, key)
            except KeyboardInterrupt:
                print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
                main()
            except: #if the file is already decrypted, the decryrpt() function will throw an error, in which case this function will encrypt the file.
                    encrypt_now()

    def run(): #this function will take the user input and execute functions accordingly.
        try:
            while True:
                print("\n--> Enter " + Fore.CYAN + "insert" + Style.RESET_ALL + " to store a new password")
                print("--> Enter " + Fore.GREEN + "list" + Style.RESET_ALL + " to all websites which you have previously entered")
                print("--> Enter " + Fore.YELLOW + "read" + Style.RESET_ALL + " to see password and username of a particular website")
                print("--> Enter " + Fore.LIGHTBLUE_EX + "update" + Style.RESET_ALL + " to update username or password of a particular website")
                print("--> Enter " + Fore.LIGHTRED_EX + "delete" + Style.RESET_ALL + " to delete username and password of a particular website")
                print("--> Enter " + Fore.LIGHTCYAN_EX + "update root" + Style.RESET_ALL + " to update username or password of root account")
                print("--> Enter " + Fore.LIGHTBLACK_EX + "delete database" + Style.RESET_ALL + " to delete database(This would delete the entire password record)")
                print(Fore.RED + "\n--> Enter 'quit' to exit program." + Style.RESET_ALL)
                print("\n[-]Enter Your choice")
                print(Fore.LIGHTYELLOW_EX + ">>> ", end="" + Style.RESET_ALL)
                choice = input()
                if choice == '':
                        print(Fore.RED + "No input detected.How can your choice be an empty one?" + Style.RESET_ALL)
                        run()
                if choice == 'insert':
                        unhide()
                        decrypt_now()
                        password_entry()
                        encrypt_now()
                        hide()
                elif choice == 'list':
                        unhide()
                        decrypt_now()
                        print_all()
                        encrypt_now()
                        hide()
                elif choice == 'read':
                        unhide()
                        decrypt_now()
                        read_from_db()
                        encrypt_now()
                        hide()
                elif choice == 'update':
                        unhide()
                        decrypt_now()
                        update()
                        encrypt_now()
                        hide()
                elif choice == 'delete':
                        unhide()
                        decrypt_now()
                        delete()
                        encrypt_now()
                        hide()
                elif choice == 'update root':
                        unhide()
                        decrypt_now()
                        update_root()
                        encrypt_now()
                        hide()
                elif choice == 'delete database':
                        unhide()
                        decrypt_now()
                        delete_table()
                        encrypt_now()
                        hide()
                elif choice == 'quit':
                        quit_now()
                else:
                        print(Fore.RED + "\nWrong choice.Please choose only from the ones listed" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
            run()
        except NameError:
            exit()
            
    def main(): #main function to call all functions and validate username and password.
            try:
                unhide()
                decrypt_now()
                create_table()
                c.execute("SELECT * FROM password WHERE website='root'")
                data = c.fetchone()
                if data[0] == 'root':
                        print(Fore.RED + "\n[#]" + Style.RESET_ALL +  "Enter Your username and password to successfully log in.")
                        check_user = getpass.getpass("Enter Your Username: ")
                        message = check_user.encode()
                        hash_check_user = hashlib.blake2b(message).hexdigest()
                        check_pass = getpass.getpass("Enter Your Password: ")
                        message1 = check_pass.encode()
                        hash_check_pass = hashlib.blake2b(message1).hexdigest()
                        if check_user == '' or check_pass == '':
                                print(Fore.RED + "No username or password entered.Unable to log you in." + Style.RESET_ALL)
                                main()
                        if hash_check_user == data[1] and hash_check_pass == data[2]:
                                print(Fore.LIGHTGREEN_EX + "\nLOGGED IN SUCCESSFULLY\n" + Style.RESET_ALL)
                                encrypt_now()
                                hide()
                                print(Fore.RED + "Do not Forcefully close the program or leave a service running midway, or the security will be compromised.")
                                print("Also, Do not keep the database and key together or else anyone with the right program can decrypt it.!!YOU HAVE BEEN WARNED!!" + Style.RESET_ALL)
                                run()
                        else:
                                print(Fore.RED + "Wrong username or Password Entered.Unable to log you in.Please try again.\n" + Style.RESET_ALL)
                                main()
            except TypeError:
                    authorize()
            except KeyboardInterrupt:
                    print(Fore.LIGHTRED_EX + "\n[!!] Please do not try to forcefully close the script." + Style.RESET_ALL)
                    main()
            except sqlite3.DatabaseError:
                    main()
    main()
    c.close() #close the cursor
    conn.close() #close the connection to database.
except NameError:
    exit()
except KeyboardInterrupt:
    print(Fore.LIGHTRED_EX + "\n[!!]Please do not try to forcefully close the script." + Style.RESET_ALL)
    main()
