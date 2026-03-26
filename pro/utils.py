def encrypt_password(password, key):
    result = ""

    for char in password:
        result += chr((ord(char) + key) % 256)

    return ''.join([chr((ord(c)+key)%256) for c in password])


def decrypt_password(password, key):
    result = ""

    for char in password:
        result += chr((ord(char) - key) % 256)

    return ''.join([chr((ord(c)-key)%256) for c in password])