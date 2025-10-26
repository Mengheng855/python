import qrcode
import os

telegram_username = "im_broken29"
message = "hello"
telegram_link = f"https://t.me/{telegram_username}?text={message.replace(' ', '%20')}"

qr = qrcode.QRCode(version=1, box_size=10, border=5)
qr.add_data(telegram_link)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("telegram_qr.png")

print("✅ QR code generated successfully: telegram_qr.png")
os.system("xdg-open telegram_qr.png")
