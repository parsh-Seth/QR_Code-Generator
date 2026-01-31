import requests

BASE = "http://127.0.0.1:5000/"
data = str(input("Enter a String to generate QRcode for: "))


r = requests.get(f"{BASE}gen/{data}", timeout=10)

if r.ok:  # True for any 2xx
    with open("qrcode.png", "wb") as f:
        f.write(r.content)
    print("File saved")
else:
    print("Error:", r.status_code, r.text[:200])