from array import array
from ctypes import alignment
import random
import sqlite3 
import hashlib
from sqlite3.dbapi2 import Cursor
from tkinter import *
from tkinter import simpledialog
from tkinter.font import Font
from functools import partial
import uuid
import pyperclip
import base64
import os
from tkinter import ttk
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
encryptionkey=0
def openVault():
    def on_closing():
        opnvault_btn['state']=NORMAL
        window2.destroy()
 
    backend=default_backend()
    salt=b'2444'
    kdf=PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    def encrypt(message:bytes,key:bytes)-> bytes:
        return Fernet(key).encrypt(message)

    def decrypt(message:bytes,token:bytes)-> bytes:
        return Fernet(token).decrypt(message)

    with sqlite3.connect("password-vault.db") as db:
        cursor=db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS masterpassword( 
    id INTEGER PRIMARY KEY,
    password TEXT NOT NULL,
    recoverykey TEXT NOT NULL);
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vault(
    id INTEGER PRIMARY KEY,
    ACCOUNT TEXT NOT NULL,
    USERNAME TEXT NOT NULL,
    PASSWORD TEXT NOT NULL);
    """)