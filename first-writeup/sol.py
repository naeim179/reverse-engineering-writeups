from Crypto.Cipher import AES

def solve():
    key = b"shadowpass123456"

    with open("f1.png.enc", "rb") as f:
        data = f.read()

    iv = data[:16]
    encrypted_payload = data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_payload)

    png_header = b"\x89PNG\r\n\x1a\n"
    start = decrypted.find(png_header)

    if start != -1:
        with open("flag.png", "wb") as f:
            f.write(decrypted[start:])
        print("[+] Success! Flag saved as flag.png")
    else:
        print("[-] PNG header not found.")

if __name__ == "__main__":
    solve()