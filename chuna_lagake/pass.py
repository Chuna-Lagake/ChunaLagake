from passlib.hash import sha256_crypt

password = sha256_crypt.hash("password")

print(password)
print(sha256_crypt.verify("password",password))