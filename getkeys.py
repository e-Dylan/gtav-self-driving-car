import win32api as wapi
import time

key_list = ["\b"]
for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ 123456789,.'$/\\":
    key_list.append(char)

def keycheck():
    keys = []
    for key in key_list:
        if wapi.GetAsyncKeyState(ord(key)):
            keys.append(key)
    return keys