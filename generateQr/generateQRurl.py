import qrcode
import os

url= "http://127.0.0.1:5500/generateQr/index.html"

telegram_link = f"{url}"

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(telegram_link)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("telegram_qr.png")

print("✅ QR code generated successfully: telegram_qr.png")
os.system("xdg-open telegram_qr.png")
