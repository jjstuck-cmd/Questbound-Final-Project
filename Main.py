import tkinter as tk
from PIL import Image, ImageTk
import random

# Global variables
inventory = []
health = 100
event_message = ""
inventory_open = False

# Paths to gem images
gems = {
    "Diamond": r"C:\Users\Jacob\Desktop\Final Project\Gems\Diamond.png",
    "Emerald": r"C:\Users\Jacob\Desktop\Final Project\Gems\Emrald .png",
    "Orange Gem": r"C:\Users\Jacob\Desktop\Final Project\Gems\Orange Gem.png",
    "Ruby": r"C:\Users\Jacob\Desktop\Final Project\Gems\Ruby.png",
    "Sapphire": r"C:\Users\Jacob\Desktop\Final Project\Gems\Sapire.png",
    "Spark Gem": r"C:\Users\Jacob\Desktop\Final Project\Gems\Spark Gem.png",
    "Sword Gem": r"C:\Users\Jacob\Desktop\Final Project\Gems\Sword Gem.png",
    "Blood Gem": r"C:\Users\Jacob\Desktop\Final Project\Gems\Blood Gem.png",
}

# Functions
def update_status():
    """Update the player's health and event message in the GUI."""
    health_label.config(text=f"Health: {health}")
    event_label.config(text=event_message)

def update_background(image_path):
    """Update the background image."""
    bg_image = ImageTk.PhotoImage(Image.open(image_path).resize((800, 400)))
    canvas.itemconfig(background, image=bg_image)
    canvas.image = bg_image  # Prevent garbage collection

def random_forest_event():
    """Generate a random event in the forest."""
    global health, event_message
    events = [
        "You found berries and restored 10 health!", 
        "A wolf attacked you! Lost 15 health.", 
        "You found a magical herb! It glows faintly and was added to your inventory."
    ]
    event = random.choice(events)
    if "berries" in event:
        health += 10
    elif "wolf" in event:
        health -= 15
    elif "herb" in event:
        inventory.append("herb")
        update_inventory_display()
    event_message = event
    update_status()

def fight_mob():
    """Simulate a fight with a mob."""
    global health, event_message
    mob_health = 20
    while mob_health > 0 and health > 0:
        mob_health -= 10
        health -= 5
        if mob_health <= 0:
            event_message = "You defeated the mob!"
            break
        if health <= 0:
            event_message = "You were defeated by the mob!"
            break
        update_status()
    check_game_over()

def search_cave():
    """Search for treasure in the cave or fight a mob."""
    global event_message
    if random.random() < 0.3:  # 30% chance to find a gem
        found_gem = random.choice(list(gems.keys()))
        inventory.append(found_gem)
        update_inventory_display()
        event_message = f"You found a {found_gem}!"
    else:
        event_message = "A mob appeared! Prepare to fight!"
        fight_mob()
    update_status()

def forest_path():
    """Handle forest path logic."""
    update_background(r"C:\Users\Jacob\Desktop\Final Project\Images\forest.png")
    random_forest_event()
    check_game_over()

def cave_path():
    """Handle cave path logic."""
    update_background(r"C:\Users\Jacob\Desktop\Final Project\Images\cave.png")
    search_cave()
    check_game_over()

def use_blood_gem():
    """Use the Blood Gem to restore health."""
    global health, event_message
    if "Blood Gem" in inventory:
        heal = random.randint(1, 15)
        health += heal
        inventory.remove("Blood Gem")
        update_inventory_display()
        event_message = f"The Blood Gem restored {heal} health!"
    else:
        event_message = "You don't have a Blood Gem!"
    update_status()

def open_inventory():
    """Expand the game window to display inventory."""
    global inventory_open
    if not inventory_open:
        root.geometry("800x700")
        inventory_frame.pack(pady=10)
        update_inventory_display()
        inventory_open = True
    else:
        root.geometry("800x600")
        inventory_frame.pack_forget()
        inventory_open = False

def update_inventory_display():
    """Update the inventory display."""
    for widget in inventory_frame.winfo_children():
        widget.destroy()
    if inventory:
        for item in inventory:
            if item in gems:
                img = ImageTk.PhotoImage(Image.open(gems[item]).resize((50, 50)))
                btn = tk.Button(inventory_frame, image=img, command=lambda i=item: use_item(i))
                btn.image = img  # Prevent garbage collection
                btn.pack(side=tk.LEFT, padx=5)
            else:
                lbl = tk.Label(inventory_frame, text=item, font=("Arial", 12))
                lbl.pack(side=tk.LEFT, padx=5)
    else:
        tk.Label(inventory_frame, text="Your inventory is empty.", font=("Arial", 14)).pack()

def use_item(item):
    """Use an item from the inventory."""
    if item == "Blood Gem":
        use_blood_gem()
    else:
        event_label.config(text=f"The {item} cannot be used right now.")

def check_game_over():
    """Check if the game is over."""
    if health <= 0:
        event_label.config(text="Game Over! You ran out of health.")
        forest_button.config(state=tk.DISABLED)
        cave_button.config(state=tk.DISABLED)
    elif "Diamond" in inventory and "Sapphire" in inventory:
        event_label.config(text="Victory! You collected the treasures and won!")
        forest_button.config(state=tk.DISABLED)
        cave_button.config(state=tk.DISABLED)

# Setup GUI
root = tk.Tk()
root.title("Adventure Quest")
root.geometry("800x600")

# Canvas for images
canvas = tk.Canvas(root, width=800, height=400)
canvas.pack()

# Load initial background
bg_image = ImageTk.PhotoImage(Image.open(r"C:\Users\Jacob\Desktop\Final Project\Images\forest.png").resize((800, 400)))
background = canvas.create_image(0, 0, anchor="nw", image=bg_image)

# Status Labels
health_label = tk.Label(root, text=f"Health: {health}", font=("Arial", 14))
health_label.pack()

event_label = tk.Label(root, text="", font=("Arial", 14), wraplength=700, justify="center")
event_label.pack(pady=10)

# Buttons
buttons_frame = tk.Frame(root)
buttons_frame.pack()

forest_button = tk.Button(buttons_frame, text="Forest Path", command=forest_path, font=("Arial", 14))
forest_button.grid(row=0, column=0, padx=10)

cave_button = tk.Button(buttons_frame, text="Cave Path", command=cave_path, font=("Arial", 14))
cave_button.grid(row=0, column=1, padx=10)

inventory_button = tk.Button(buttons_frame, text="Inventory", command=open_inventory, font=("Arial", 14))
inventory_button.grid(row=0, column=2, padx=10)

# Inventory Frame
inventory_frame = tk.Frame(root)

# Start the main event loop
root.mainloop()
