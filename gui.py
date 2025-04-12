import tkinter as tk
from PIL import Image, ImageTk
import cv2

# Setup
root = tk.Tk()
root.title("FocusFlow")
root.geometry("1200x700")
root.configure(bg="white")

cap = None
running = False

# Functions
def show_frame():
    global cap, running
    if running and cap:
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (590, 360))
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
        video_label.after(10, show_frame)

def start_camera():
    global cap, running
    if not running:
        cap = cv2.VideoCapture(0)
        running = True
        show_frame()

def stop_camera():
    global cap, running
    running = False
    if cap:
        cap.release()
        cap = None
    video_label.configure(image='')

def create_rounded_button(parent, text, command, y_offset):
    canvas = tk.Canvas(parent, width=160, height=45, bg="white", highlightthickness=0)
    canvas.place(relx=0.5, y=y_offset, anchor="center")

    def draw_button(fill_color, outline_color):
        canvas.delete("all")
        canvas.create_round_rect(2, 2, 158, 43, radius=20, fill=fill_color, outline=outline_color, width=2)
        canvas.create_text(80, 22, text=text, fill="white", font=("Segoe UI", 10, "bold"), tags="label")

    def on_enter(event):
        draw_button("#2c3e50", "#2980b9")

    def on_leave(event):
        draw_button("#2980b9", "#2980b9")

    def on_click(event):
        command()

    def _create_round_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    tk.Canvas.create_round_rect = _create_round_rect

    draw_button("#2980b9", "#2980b9")
    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.tag_bind("label", "<Button-1>", on_click)

def styled_box(x, y, width, height):
    frame = tk.Frame(root, bg="white", width=width, height=height)
    frame.place(x=x, y=y)

    # Left & right border
    tk.Frame(frame, bg="#dcdcdc", width=2, height=height).place(x=0, y=0)
    tk.Frame(frame, bg="#dcdcdc", width=2, height=height).place(x=width - 2, y=0)

    # Thin top & bottom lines
    tk.Frame(frame, bg="#eaeaea", width=width, height=1).place(x=0, y=0)
    tk.Frame(frame, bg="#eaeaea", width=width, height=1).place(x=0, y=height - 1)

    return frame

# Sidebar
sidebar = tk.Frame(root, bg="#f8f9fa", width=100, height=700)
sidebar.place(x=0, y=0)

def create_sidebar_option(parent, icon, label):
    frame = tk.Frame(parent, bg="#f8f9fa", width=100, height=70)
    frame.pack_propagate(False)
    frame.pack(pady=10)

    inner_frame = tk.Frame(frame, bg="#f8f9fa")
    inner_frame.place(relx=0.5, rely=0.5, anchor="center")

    icon_label = tk.Label(inner_frame, text=icon, font=("Segoe UI", 18), bg="#f8f9fa")
    icon_label.pack()

    text_label = tk.Label(inner_frame, text=label, font=("Segoe UI", 9, "bold"), bg="#f8f9fa", fg="#2c3e50")
    text_label.pack(pady=(2, 0))

create_sidebar_option(sidebar, "🏠", "Home")
create_sidebar_option(sidebar, "👁️", "Focus")
create_sidebar_option(sidebar, "⚙️", "Settings")

# Camera Feed Box
tk.Label(root, text="Live Camera Feed", bg="white", fg="#2c3e50", font=("Segoe UI", 12, "bold")).place(x=120, y=20)
box1 = styled_box(110, 50, 600, 370)
video_label = tk.Label(box1, bg="white")
video_label.place(x=5, y=5, width=590, height=360)

# Camera Controls
tk.Label(root, text="Camera Controls", bg="white", fg="#2c3e50", font=("Segoe UI", 12, "bold")).place(x=880, y=30, anchor="center")
box2 = styled_box(730, 50, 300, 180)
create_rounded_button(box2, "Start Camera", start_camera, y_offset=70)
create_rounded_button(box2, "Stop Camera", stop_camera, y_offset=125)

# Additional Panels
box3 = styled_box(730, 240, 300, 180)
box4 = styled_box(110, 440, 300, 220)
box5 = styled_box(420, 440, 300, 220)
box6 = styled_box(730, 440, 300, 220)

root.mainloop()



