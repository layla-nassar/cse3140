from Crypto.PublicKey import RSA

public_key_file = "/home/cse/Lab3/Solutions/e.key.pem" # encryption key
private_key_file = "/home/cse/Lab3/Solutions/d.key.pem" # decryption key

key = RSA.generate(1024)
public_key = key.publickey().export_key()
private_key = key.export_key()

with(open(public_key_file,"wb")) as f:
    f.write(public_key)
with(open(private_key_file,"wb")) as f:
    f.write(private_key)
