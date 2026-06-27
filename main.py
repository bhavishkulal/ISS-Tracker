import os
import requests
from datetime import datetime
import smtplib

my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("EMAIL_PASSWORD")
to_email = os.environ.get("TO_EMAIL")
pavanbro_email = os.environ.get("PAVAN_EMAIL")

MY_LAT = 13.117661
MY_LONG = 77.633218


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True
    return False

if is_iss_overhead() and is_night():
    print("ISS is overhead and it's night! Sending notifications...")
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=to_email,
            msg="Subject:Look Up!!!\n\nThe ISS is above you in the sky."
        )
        connection.sendmail(
            from_addr=my_email,
            to_addrs=pavanbro_email,
            msg="Subject:Look Up!!!\n\nThe ISS is above you in the sky."
        )
else:
    print("ISS is not overhead or it's daytime.")
