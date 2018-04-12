#!/usr/bin/env python

import json
import socket

from Crypto.PublicKey import RSA


# def createDict(uid, key, value):
#   return {
#     "uid":uid,
#     key:value
#   }

def encrypt(uid, key ,value):
  data = {
    "uid":uid,
    key:value
  }
  print((data))
  f1 = open('publicKey.pem','r')
  public_key = RSA.importKey(f1.read())
  f1.close()

  message = json.dumps(data).encode('ascii')
  # print(type(message))
  cipher = public_key.encrypt(message, 32)[0]
  print("Encryption done")
  print(type(cipher))
  return cipher

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# get local machine name
host = socket.gethostbyname('localhost')
port = 9999

# connection to hostname on the port.
s.connect((host, port))                               

uid = '509101022367'
key = 'dob'
value = '30-05-1997'

cipher = encrypt(uid,key,value)
# print((cipher))
# s.connect((host, port))                               
s.send(cipher)
f1 = open('publicKey.pem','r')
public_key = RSA.importKey(f1.read())
f1.close()

finalCert = s.recv(4096)
# finalAns = public_key.decrypt(finalCipher)

data = json.loads(finalCert, encoding='latin1')
print(data)

s.close()



