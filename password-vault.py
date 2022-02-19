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
    def popUp(text,previous_txt=""):
        answer=simpledialog.askstring("input string",prompt=text,initialvalue=str(previous_txt))
        return answer

    window2=Toplevel(window)
    window2.protocol("WM_DELETE_WINDOW",on_closing)
    
    window2.title("PASSWORD MANAGER")
    def hashPassword(input):
        # hash=hashlib.sha256(input)
        # hash=hash.hexdigest()
        return hashlib.sha256(input).hexdigest()

    def firstScreen():
        for widget in window2.winfo_children():
            widget.destroy()
        window2.geometry("250x150")

        lbl=ttk.Label(window2,text="Create Master Password")
        lbl.config(anchor=CENTER)
        lbl.pack()

        Mstr_pass_txt=ttk.Entry(window2,width=20,show="*")
        Mstr_pass_txt.pack()
        Mstr_pass_txt.focus()

        lbl1=ttk.Label(window2,text="Confirm Master Password")
        lbl1.pack() 
        
        Mstr_pass_txt2=ttk.Entry(window2,width=20,show="*")
        Mstr_pass_txt2.pack()
        
        
        lbl2=ttk.Label(window2,text="")
        lbl2.pack()

        def savePassword():
            if Mstr_pass_txt.get()==Mstr_pass_txt2.get() :
                sql="DELETE FROM masterpassword WHERE id=1"
                cursor.execute(sql)

                hashed_pass=hashPassword(Mstr_pass_txt.get().encode('utf-8'))
                key=str(uuid.uuid4().hex)
                
                recoverykey=hashPassword(key.encode('utf-8'))
                global encryptionkey 
                encryptionkey= base64.urlsafe_b64encode(kdf.derive("PremWagh2210".encode('utf-8')))
                
                insert_pass="""INSERT INTO masterpassword(password,recoverykey)
                VALUES(?,?)"""
                cursor.execute(insert_pass,((hashed_pass),(recoverykey)))
                db.commit()
                recoveryScreen(key)
            else:
                Mstr_pass_txt2.delete(0,'end')
                lbl2.config(text="TRY AGAIN !")



        btn=ttk.Button(window2,text="SAVE",command=savePassword)
        btn.pack(pady=10)
