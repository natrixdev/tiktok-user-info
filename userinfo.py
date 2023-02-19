import requests
import tkinter as tk
from io import BytesIO
from urllib.request import urlopen
from json import JSONDecodeError
from rich.console import Console
from rich.table import Table

# Create Tkinter window
window = tk.Tk()
window.geometry("400x400")

# Create header label
header_label = tk.Label(text="TikTok User Info", font=("Arial", 18))
header_label.pack(pady=10)

# Create input label and entry field
input_label = tk.Label(text="Enter TikTok username:")
input_label.pack(pady=10)
input_entry = tk.Entry(width=30)
input_entry.pack()

# Create function to retrieve and display user info
def get_user_info():
    # Get username from input field
    username = input_entry.get()

    # Make request to TikTok API to get user info
    url = f"https://www.tiktok.com/node/share/user/@{username}"
    try:
        response = requests.get(url).json()
    except JSONDecodeError:
        console = Console()
        console.print("Invalid username. Please enter a valid username.")
        return

    # Extract relevant user info from response
    user_info = response['userInfo']

    username = user_info['uniqueId']
    avatar_url = user_info['avatarThumb']
    num_videos = user_info['videoCount']
    num_followers = user_info['followerCount']
    num_following = user_info['followingCount']
    is_private = user_info['isSecret']
    is_verified = user_info['verified']

    # Create table to display user info
    table = Table(show_header=False, show_lines=True)
    table.add_column(justify="right")
    table.add_column()
    table.add_row("Username:", username)

    # Download and display user avatar
    response = urlopen(avatar_url)
    img_data = response.read()
    img = tk.PhotoImage(data=img_data)
    avatar_label = tk.Label(image=img)
    avatar_label.image = img
    table.add_row("Avatar:", avatar_label)

    table.add_row("Number of videos:", str(num_videos))
    table.add_row("Number of followers:", str(num_followers))
    table.add_row("Number of following:", str(num_following))
    table.add_row("Private account:", "Yes" if is_private else "No")
    table.add_row("Verified account:", "Yes" if is_verified else "No")

    # Display table
    console = Console()
    console.print(table)

# Create "Search user" button
search_button = tk.Button(text="Search user", command=get_user_info)
search_button.pack(pady=10)

# Run Tkinter window
window.mainloop()
