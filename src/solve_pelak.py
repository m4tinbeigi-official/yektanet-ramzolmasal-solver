#!/usr/bin/env python3
"""
حل مرحله دهم (فینال): دیوار به دیوار (pelak)
منطق ضرب‌المثل: «مرغ همسایه غازه!»
سرنخ‌ها:
  - پرامپت: «اینجا خونته. هرچی تو خونه‌ی خودت هست، به چشمت نمیاد.»
  - وضعیت (Charm): «همیشه شماره تلفنشو می‌چسبونه به شماره موبایلش و میشه رمزش.»
روش حل:
  ۱. خانه خودمان در دامنه https://256.yektanet.tech (پلاک ۲۵۶) قرار دارد.
  ۲. همسایه دیوار به دیوار ما پلاک ۲۵۴ در دامنه https://254.yektanet.tech است که تنها با ارسال هدر Referer از پلاک ۲۵۶ پاسخ می‌دهد.
  ۳. در پلاک ۲۵۴ تصویر ghaz.jpg قرار دارد که در انتهای آن یک فایل فشرده Zip مخفی شامل تصویر morgh.jpg پیوست شده است (مرغ داخل غاز همسایه!).
  ۴. کد پستی پلاک همسایه برابر با 3767481923 است.
  ۵. با جستجوی این کد پستی در گوگل، شرکت «غاز ایران» (مدیریت امیر طاهری در نسیم شهر) در سامانه جویشگر پیدا می‌شود:
     - تلفن: 02156573210 (بدون صفر و پیش شماره: 2156573210)
     - همراه: 09198584667 (بدون صفر: 9198584667)
  ۶. اتصال شماره تلفن به همراه: 21565732109198584667 رمز بازگشایی فایل زیپ است!
  ۷. با باز شدن فایل زیپ، تصویر morgh.jpg استخراج می‌شود که در بنر پایین آن نوشته شده:
     «رمز زیپ: 6ebd1e974a22»
  ۸. پرچم نهایی حاصل ترکیب رمز فایل زیپ و کد استخراج‌شده داخل تصویر مرغ است:
     YEK{21565732109198584667:6ebd1e974a22}
"""

import requests
import http.cookiejar

def solve_pelak(cookie_path="cookies.txt"):
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_path)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj

    zip_password = "21565732109198584667"
    secret_token = "6ebd1e974a22"
    flag = f"YEK{{{zip_password}:{secret_token}}}"

    print(f"Submitting Pelak Flag: {flag}")
    session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "pelak"})
    res = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}).json()
    print("Submit Result:", res)
    return flag

if __name__ == "__main__":
    solve_pelak()
