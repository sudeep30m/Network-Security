import time
import json
import socket
import random
from Crypto.PublicKey import RSA
from OpenSSL import crypto, SSL
from Crypto.Hash import SHA

# decrypt query using server's private key.
def decrypt(cipher):
    f2 = open('privateKey.pem','r')
    private_key = RSA.importKey(f2.read())
    f2.close()
    decrypted = private_key.decrypt(cipher)
    data = json.loads(decrypted)
    return data

# The UID server needs to verify the data(JSON format) and output whether it's true or not.
# Here it is simply outputting a random true or false
def verify(data):
    return bool(random.getrandbits(1))

# Create a certificate and sign it using server's private key.
def createCertificate(data, answer):

    query = json.dumps(data).encode('ascii')
    hashQuery = SHA.new(query).hexdigest()
    
    cert = {
        "hashQuery":hashQuery,
        "answer":answer
    }
    print("certificate is ", cert)
    certDump = json.dumps(cert).encode('ascii')
    hashCert = SHA.new(certDump).hexdigest()
    print(hashCert)
    f2 = open('privateKey.pem','r')
    private_key = RSA.importKey(f2.read())
    signature = private_key.encrypt(hashCert, 32)[0]
        
    responseDict = {
        "cert": cert,
        "signature": signature
    }
    f1 = open('publicKey.pem','r')
    public_key = RSA.importKey(f1.read())
    f1.close()
    # print(public_key.decrypt(signature))
    # print(responseDict)
    response = json.dumps(responseDict, encoding='latin1')
    return response


# Setting up a server
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
host = socket.gethostbyname('localhost')
port = 9999
serversocket.bind((host, port))
serversocket.listen(5)
print("Listening on port ",port)


while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()      
    print("Got a connection from %s" % str(addr))

    # recieve query from client.
    cipher = clientsocket.recv(4096)
    
    # Client encrypts data using server's public key. Decrypt using server's private key.     
    data = decrypt(cipher)
    
    # Verify the query. 
    ans = verify(data)

    # Create a certificate containing hash of the query, whether it is correct or not along with server's digital signature.
    response = createCertificate(data, ans)
    print(response)
    # Send the digitally signed certificate to client.
    clientsocket.send(response)
    clientsocket.close()



