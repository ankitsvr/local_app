from cryptography.fernet import Fernet

key=Fernet.generate_key()
f=Fernet(key)
token=f.encrypt("Arelly secret message  not for preying eyes ")
print token
output=f.decrypt(token)
print output