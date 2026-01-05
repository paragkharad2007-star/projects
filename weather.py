import tkinter as tk
from tkinter import messagebox
import requests

# ---------------- CONFIG ----------------
API_KEY = "bc23d0eee18ed09fa1a62c4d70ccf137"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ---------------- FUNCTION ----------------
def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return

    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if data.get("cod") != 200:
            messagebox.showerror("Error", "City not found")
            return

        temperature = data["main"]["temp"]
        condition = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        output = (
            f"City: {city.title()}\n\n"
            f"🌡 Temperature: {temperature} °C\n"
            f"☁ Condition: {condition}\n"
            f"💧 Humidity: {humidity}%\n"
            f"🌬 Wind Speed: {wind_speed} m/s"
        )

        result_label.config(text=output)

    except requests.exceptions.RequestException:
        messagebox.showerror("Network Error", "Unable to fetch weather data")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Weather App")
root.geometry("420x420")
root.resizable(False, False)

# Title
title = tk.Label(
    root,
    text="Weather App",
    font=("Arial", 20, "bold")
)
title.pack(pady=15)

# Input
city_entry = tk.Entry(
    root,
    font=("Arial", 14),
    justify="center"
)
city_entry.pack(pady=10)
city_entry.focus()

# Button
get_btn = tk.Button(
    root,
    text="Get Weather",
    font=("Arial", 12, "bold"),
    width=15,
    command=get_weather
)
get_btn.pack(pady=10)

# Result
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 12),
    justify="left"
)
result_label.pack(pady=20)

root.mainloop()
