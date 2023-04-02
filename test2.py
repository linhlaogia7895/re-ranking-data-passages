import tkinter as tk

root = tk.Tk()

# Create a tkinter variable to hold the selected option
selected_option = tk.StringVar()

# Create the dropdown menu with radio buttons
option_menu = tk.OptionMenu(root, selected_option, "Option 1", "Option 2", "Option 3")
option_menu.pack()
# Bind the function to the dropdown menu
selected_option.trace("w", lambda *args: show_selected())

def show_selected():
    print(selected_option.get())

root.mainloop()