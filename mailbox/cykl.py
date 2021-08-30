#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import imaplib


def cykl(imap):
    while True:
        imap.select("INBOX", readonly = True)

        #status, messages = imap.search(None, 'UnSeen')

        # total number of emails
        #literki, tablica = messages.split("'") #usunąć pierwsze: b'

        messages = int(messages[0])

        #Writing out 3 last unread e-mails
        wypisanie(messages, imap)

        #Delaying cykl for 5 minutes
        czas = 300 
        time.sleep(czas)
        print("\n If you want to end this program, press Ctr+C\n")


