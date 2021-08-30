#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#Opening of imap.py and cykl moduls
from imap import *
from cykl import *

#Opening of library
import imaplib
import email
import getpass
import time



if __name__ == '__main__':
    #Input of credentials
    try:
        login, adres = input("Write your e-mail: ").split("@")
    except:
        print("Niepoprawny mail!")
        exit(0)
    haslo = getpass.getpass("Write your password: ")
    print("\n")
    mail = login + "@" + adres

    #Choosing of imap: gmail or other
    imap_adres=gmail(adres)

    #Getting connection with imap
    imap = connect(imap_adres, mail, haslo)

    cykl(imap)

    # close the connection and logout
    imap.close()
    imap.logout()
    app.run(debug=True)