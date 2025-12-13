import tkinter as tk
import psutil

UPDATE_MS = 1000

def get_usage():
    cpu = int(psutil.cpu_percent(interval=None))
    ram = int(psutil.virtual_memory().percent)
    return cpu, ram

def update_label():
    cpu, ram = get_usage()
    text = f"CPU: {cpu}%  RAM: {ram}%"
    label.config(text=text)
    root.lift()
    root.focus_force()
    root.after(UPDATE_MS, update_label)

root = tk.Tk()
root.title("CPU/RAM Monitor")
root.overrideredirect(True)  # Keep your icon-only style
root.attributes("-topmost", True)

# Add toolwindow attribute for stability WITHOUT changing appearance
root.wm_attributes("-toolwindow", 1)

bg_color = "#ADD8E6"
fg_color = "black"
root.configure(bg=bg_color)

label = tk.Label(
    root,
    text="CPU: ---% RAM: ---%",
    font=("Segoe UI", 10),
    bg=bg_color,
    fg=fg_color,
)
label.pack(padx=6, pady=2)

# Safe positioning ABOVE taskbar
root.update_idletasks()
w = root.winfo_width()
h = root.winfo_height()
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
margin = 10
x = 160
y = screen_h - h - margin
root.geometry(f"{w}x{h}+{x}+{y}")

def start_move(event):
    root._drag_start_x = event.x
    root._drag_start_y = event.y

def do_move(event):
    x = root.winfo_x() + event.x - root._drag_start_x
    y = root.winfo_y() + event.y - root._drag_start_y
    root.geometry(f"+{x}+{y}")

label.bind("<ButtonPress-1>", start_move)
label.bind("<B1-Motion>", do_move)

def close(event=None):
    root.destroy()

menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Exit", command=close)

def show_menu(event):
    menu.tk_popup(event.x_root, event.y_root)
    menu.grab_release()

label.bind("<Button-3>", show_menu)

update_label()
root.mainloop()
