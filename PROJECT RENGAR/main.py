import urllib.parse
import requests
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk  # To load and display images
import webbrowser
from tabulate import tabulate

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "SwjSeXMjOzgsf2oIIXrASD5fOP99sxJl"

def get_directions():
    orig = entry_start.get()
    dest = entry_dest.get()
    unit = unit_var.get().lower()

    if not orig or not dest:
        messagebox.showerror("Error", "Please enter both Starting Location and Destination.")
        return

    if unit not in ["miles", "kilometers", "mi", "km"]:
        messagebox.showwarning("Warning", "Invalid unit. Defaulting to miles.")
        unit = "miles"

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    json_data = requests.get(url).json()

    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        directions_text.delete(1.0, tk.END)
        directions_text.insert(tk.END, f"Directions from {orig} to {dest}\n", "heading")
        directions_text.insert(tk.END, f"Trip Duration: {json_data['route']['formattedTime']}\n", "info")
        distance = json_data['route']['distance']
        if unit in ["kilometers", "km"]:
            distance = distance * 1.61
            unit_str = "Kilometers"
        else:
            unit_str = "Miles"
        directions_text.insert(tk.END, f"Distance: {distance:.2f} {unit_str}\n", "info")
        directions_text.insert(tk.END, "=============================================\n", "separator")

        maneuvers = []
        for each in json_data["route"]["legs"][0]["maneuvers"]:
            narrative = each["narrative"]
            dist = each["distance"] * (1.61 if unit in ["kilometers", "km"] else 1)
            maneuvers.append([narrative, f"{dist:.2f} {unit_str}"])

        directions_text.insert(tk.END, tabulate(maneuvers, headers=["Instruction", "Distance"], tablefmt="grid"), "table")

        # Add link to open in MapQuest
        map_link = f"https://www.mapquest.com/directions/from/{orig.replace(' ', '+')}/to/{dest.replace(' ', '+')}"
        directions_text.insert(tk.END, f"\nOpen this route in MapQuest: {map_link}\n", "link")
        open_map_button.config(state=tk.NORMAL)
        open_map_button.map_link = map_link
    elif json_status == 402:
        messagebox.showerror("Error", "Invalid user inputs for one or both locations.")
    elif json_status == 611:
        messagebox.showerror("Error", "Missing an entry for one or both locations.")
    else:
        messagebox.showwarning("Warning", f"For Status Code: {json_status}; Refer to: https://developer.mapquest.com/documentation/directions-api/status-codes")

def open_map():
    webbrowser.open(open_map_button.map_link)

# Create the main window
root = tk.Tk()
root.title("AquaTech")
root.geometry("600x500")
root.configure(bg="#F7F7F7")

# Customize fonts and colors
title_font = ("Helvetica", 16, "bold")
label_font = ("Helvetica", 12)
button_font = ("Helvetica", 12, "bold")
entry_bg = "#EFEFEF"
button_bg = "#1E90FF"  # Change the buttons to Dodger Blue
button_fg = "white"
text_bg = "#FFFFFF"
text_fg = "#333333"

# Load and display the logo
logo_img = Image.open("C:/Users/james guanizo/copy-removebg-preview.png")
logo_img = logo_img.resize((60, 60), Image.LANCZOS)  # Resize the logo if needed
logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(root, image=logo_photo, bg=root["bg"])
logo_label.grid(row=0, column=0, columnspan=2, pady=(20, 5))

# Add "AquaTech" label below the logo
label_aquatech = tk.Label(root, text="AquaTech", font=("Helvetica", 20, "bold"), bg=root["bg"], fg="#2C3E50")
label_aquatech.grid(row=1, column=0, columnspan=2)

# Labels and entries for Starting Location and Destination
label_start = tk.Label(root, text="Starting Location:", font=label_font, bg=root["bg"])
label_start.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
entry_start = tk.Entry(root, width=40, bg=entry_bg, font=label_font)
entry_start.grid(row=2, column=1, padx=10, pady=10)

label_dest = tk.Label(root, text="Destination:", font=label_font, bg=root["bg"])
label_dest.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
entry_dest = tk.Entry(root, width=40, bg=entry_bg, font=label_font)
entry_dest.grid(row=3, column=1, padx=10, pady=10)

# Dropdown for unit selection
label_unit = tk.Label(root, text="Preferred Unit:", font=label_font, bg=root["bg"])
label_unit.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
unit_var = tk.StringVar(value="miles")
unit_dropdown = ttk.Combobox(root, textvariable=unit_var, values=["miles", "kilometers"], state="readonly", font=label_font)
unit_dropdown.grid(row=4, column=1, padx=10, pady=10)

# Button to get directions
button_get_directions = tk.Button(root, text="Get Directions", command=get_directions, font=button_font, bg=button_bg, fg=button_fg)
button_get_directions.grid(row=5, column=0, columnspan=2, pady=20)

# Text widget to display directions
directions_text = tk.Text(root, wrap=tk.WORD, width=60, height=10, bg=text_bg, fg=text_fg, font=label_font)
directions_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Define custom tags for text formatting
directions_text.tag_config("heading", font=("Helvetica", 14, "bold"), foreground="#2C3E50")
directions_text.tag_config("info", font=("Helvetica", 12), foreground="#2980B9")
directions_text.tag_config("separator", font=("Helvetica", 12), foreground="#BDC3C7")
directions_text.tag_config("link", font=("Helvetica", 12, "underline"), foreground="#27AE60")
directions_text.tag_config("table", font=("Courier", 10))

# Button to open map link
open_map_button = tk.Button(root, text="Open Map in Browser", command=open_map, state=tk.DISABLED, font=button_font, bg=button_bg, fg=button_fg)
open_map_button.grid(row=7, column=0, columnspan=2, pady=10)

# Start the main loop
root.mainloop()
