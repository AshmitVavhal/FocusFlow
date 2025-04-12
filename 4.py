import customtkinter as ctk
import sys
email = sys.argv[1] if len(sys.argv) > 1 else None
import tkinter as tk
import subprocess
from tkinter import Canvas
from PIL import Image, ImageTk, ImageDraw
from datetime import datetime
import cv2

# === Appearance Settings ===
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# === Root Window ===
root = ctk.CTk()
root.geometry("1200x750")
root.title("Dashboard UI")
root.configure(fg_color="#e9ecf6")

# === Sidebar ===
sidebar = ctk.CTkFrame(root, fg_color="#f5f7fc", width=220, height=750, corner_radius=0)
sidebar.place(x=0, y=0)

ctk.CTkLabel(sidebar, text="🔸  User", font=("Segoe UI", 12, "bold"),
             text_color="#5c60a8", fg_color="#f5f7fc", anchor="w", padx=20, width=220).place(x=0, y=20)

ctk.CTkFrame(sidebar, fg_color="#e0e3f0", height=1, width=180).place(x=20, y=60)

ctk.CTkLabel(sidebar, text="MENU", font=("Segoe UI", 9, "bold"),
             text_color="#9aa1b9", fg_color="#f5f7fc", anchor="w", padx=20, width=220).place(x=0, y=80)

menu_items = [
    ("📊  Dashboard", True),
    ("🗓️  Upcoming Meeting", False),
    ("🎯  Manage Goals", False),
    ("💬  Customer Review", False)
]

y_offset = 110
for label, is_active in menu_items:
    bg = "#e9edfb" if is_active else "#f5f7fc"
    fg = "#4a4e6c" if is_active else "#9ca2b8"
    font = ("Segoe UI", 10, "bold") if is_active else ("Segoe UI", 10)
    ctk.CTkLabel(sidebar, text=label, font=font, text_color=fg,
                 fg_color=bg, anchor="w", padx=30, width=220, height=35).place(x=0, y=y_offset)
    y_offset += 40

ctk.CTkLabel(sidebar, text="OTHERS", font=("Segoe UI", 9, "bold"),
             text_color="#9aa1b9", fg_color="#f5f7fc", anchor="w", padx=20, width=220).place(x=0, y=y_offset + 10)

other_items = ["⚙️  Settings", "💳  Payment", "👤  Accounts", "❓  Help"]
y_offset += 40
for label in other_items:
    ctk.CTkLabel(sidebar, text=label, font=("Segoe UI", 10),
                 text_color="#9ca2b8", fg_color="#f5f7fc", anchor="w", padx=30, width=220, height=35).place(x=0, y=y_offset)
    y_offset += 40

# === Main Content ===
main_frame = ctk.CTkFrame(root, fg_color="#e9ecf6")
main_frame.place(x=220, y=0, relwidth=1, relheight=1)

# Greeting Card
def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good Morning"
    elif 12 <= hour < 17:
        return "Good Afternoon"
    elif 17 <= hour < 21:
        return "Good Evening"
    else:
        return "Good Night"

greeting_card = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=35, width=500, height=140)
greeting_card.place(x=30, y=30)

greeting_text = get_greeting()
ctk.CTkLabel(greeting_card, text=f"{greeting_text}, Ayush 👋",
             font=("Segoe UI", 18, "bold"), text_color="#2f2f5f", fg_color="transparent").place(x=30, y=28)

ctk.CTkLabel(greeting_card, text="Hope you're having a productive day!",
             font=("Segoe UI", 11), text_color="#666a88", fg_color="transparent").place(x=30, y=60)

clock_label = ctk.CTkLabel(greeting_card, text="", font=("Segoe UI", 28, "bold"),
                           text_color="#2f2f5f", fg_color="transparent")
clock_label.place(x=30, y=95)

def update_time():
    current_time = datetime.now().strftime("%I:%M %p").lower()
    clock_label.configure(text=current_time)
    root.after(1000, update_time)

update_time()

# Weather Card
weather_frame = ctk.CTkFrame(main_frame, width=240, height=150, fg_color="white", corner_radius=20)
weather_frame.place(x=560, y=30)

try:
    cloud_img = Image.open("cloud.png").resize((70, 70), Image.Resampling.LANCZOS)
    cloud_img_ctk = ctk.CTkImage(light_image=cloud_img, size=(70, 70))
    ctk.CTkLabel(weather_frame, image=cloud_img_ctk, text="", fg_color="white").place(x=10, y=10)
except:
    ctk.CTkLabel(weather_frame, text="☁️", font=("Segoe UI", 36), fg_color="white").place(x=10, y=10)

ctk.CTkLabel(weather_frame, text="26°", font=("Segoe UI", 28, "bold"),
             text_color="#4a4a72", fg_color="white").place(x=90, y=20)

ctk.CTkLabel(weather_frame, text="Heavy Rain", font=("Segoe UI", 11),
             text_color="#7d7f9e", fg_color="white").place(x=15, y=90)

ctk.CTkLabel(weather_frame, text="Pune.  Sunday, April 7", font=("Segoe UI", 9),
             text_color="#9a9cb3", fg_color="white").place(x=15, y=115)

# === Live Camera Feed with Face Detection ===
camera_box = ctk.CTkFrame(main_frame, width=300, height=300, fg_color="#DCE5FF",
                          corner_radius=20, border_color="#9FA8DA", border_width=2)
camera_box.place(x=30, y=200)

video_label = tk.Label(camera_box, bg="#DCE5FF")
video_label.place(relx=0.5, rely=0.5, anchor="center")

face_status_label = ctk.CTkLabel(main_frame, text="", font=("Segoe UI", 14, "bold"),
                                 text_color="#4CAF50", fg_color="transparent")
face_status_label.place(x=30, y=510)

cap = None
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def apply_rounded_corners(img, radius):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    img.putalpha(mask)
    return img

detecting = False
def toggle_detection():
    global detecting, cap

    detecting = not detecting
    toggle_btn.configure(text="Stop Detection" if detecting else "Start Detection")

    if detecting:
        # Stop camera in 4.py
        if cap:
            cap.release()
            cap = None

        # Launch project.py for eye tracking
        subprocess.Popen(["python", "project.py", "--email", email])


toggle_btn = ctk.CTkButton(main_frame, text="Start Detection", command=toggle_detection,
                           width=140, height=36, corner_radius=20, font=("Segoe UI", 12))
toggle_btn.place(x=460, y=470)

def start_camera():
    global cap
    cap = cv2.VideoCapture(0)

    def update_frame():
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                display_frame = cv2.resize(frame, (400, 400))

                gray = cv2.cvtColor(display_frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(60, 60))

            

                for (x, y, w, h) in faces:
                    cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(display_frame, "Face Detected", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                rgb_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb_frame)
                img = apply_rounded_corners(img, radius=40)
                imgtk = ImageTk.PhotoImage(image=img)

                video_label.imgtk = imgtk
                video_label.configure(image=imgtk)

        video_label.after(15, update_frame)

    update_frame()

def on_closing():
    if cap and cap.isOpened():
        cap.release()
    root.destroy()

start_camera()
root.protocol("WM_DELETE_WINDOW", on_closing)

# === Monthly Goals Widget ===
class ProgressCircle(Canvas):
    def __init__(self, parent, value, **kwargs):
        super().__init__(parent, width=60, height=60, bg="#ffffff", highlightthickness=0, **kwargs)
        self.value = value
        self.draw_circle()

    def draw_circle(self):
        self.create_oval(5, 5, 55, 55, width=2, outline="#d1d1d1")
        angle = 360 * self.value
        self.create_arc(5, 5, 55, 55, start=90, extent=-angle, style="arc", outline="#4477ff", width=4)
        self.create_text(30, 30, text=f"{int(self.value*4)}/4", font=("Helvetica", 10, "bold"))

class MonthlyGoalsWidget(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, corner_radius=25, fg_color="#ffffff", width=300, height=250)
        self.configure(border_color="#e2e2f2", border_width=1)
        self.grid_propagate(False)
        self.completed = tk.IntVar(value=1)
        self.goals = [
            ("1h Meditation", True),
            ("10m Running", False),
            ("30m Workout", False),
            ("30m Pooja & read book", False)
        ]
        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(self, text="🗕️ Monthly Goals", font=("Segoe UI", 15, "bold"), text_color="#1a1a2f")
        title.grid(row=0, column=0, padx=(20, 0), pady=(20, 10), sticky="w")

        self.progress = ProgressCircle(self, self.completed.get() / 4)
        self.progress.grid(row=0, column=1, padx=(0, 20), pady=(20, 10), sticky="e")

        for i, (text, checked) in enumerate(self.goals):
            var = tk.BooleanVar(value=checked)
            checkbox = ctk.CTkCheckBox(
                self, text=text, variable=var,
                font=("Segoe UI", 12),
                hover_color="#e0e0e0",
                border_color="#bcbcbc",
                fg_color="#4477ff" if checked else "#dddddd",
                text_color="#000000" if checked else "#777777",
                corner_radius=10,
                height=24,
                command=self.update_progress
            )
            checkbox.grid(row=i + 1, column=0, columnspan=2, padx=20, pady=4, sticky="w")

    def update_progress(self):
        count = sum(1 for child in self.winfo_children() if isinstance(child, ctk.CTkCheckBox) and child.get())
        self.completed.set(count)
        self.progress.destroy()
        self.progress = ProgressCircle(self, count / 4)
        self.progress.grid(row=0, column=1, padx=(0, 20), pady=(20, 10), sticky="e")

monthly_goals = MonthlyGoalsWidget(main_frame)
monthly_goals.place(x=460, y=200)

# === Last Projects Section ===
class LastProjects(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.configure(corner_radius=20)
        self.build_ui()

    def build_ui(self):
        title = ctk.CTkLabel(self, text="Last project’s", font=("Segoe UI", 20, "bold"), text_color="#1a1a1a")
        title.grid(row=0, column=0, padx=10, pady=(10, 20), sticky="w")

        cards = [
            ("New Schedule", "In Progress", 95, "Create a new and unique design for my YouTube family."),
            ("Javascript", "Completed", 100),
            ("Chatbot", "Completed", 100),
        ]

        for index, (project, status, percent, *desc) in enumerate(cards):
            card = ctk.CTkFrame(self, fg_color="white", corner_radius=20, width=230, height=140)
            card.grid(row=1, column=index, padx=12, pady=10)
            card.grid_propagate(False)

            title_label = ctk.CTkLabel(card, text=project, font=("Segoe UI Semibold", 16), text_color="#222")
            title_label.place(x=15, y=15)

            status_color = "#4CAF50" if status == "Completed" else "#F0AD4E"
            status_label = ctk.CTkLabel(card, text=f"● {status}", font=("Segoe UI", 12), text_color=status_color)
            status_label.place(x=15, y=45)

            if desc:
                desc_label = ctk.CTkLabel(card, text=f"Done: {desc[0]}", font=("Segoe UI", 11), text_color="#777",
                                           wraplength=200, justify="left")
                desc_label.place(x=15, y=70)

            percent_label = ctk.CTkLabel(card, text=f"{percent}%", font=("Segoe UI Bold", 14), text_color="#000",
                                         fg_color="#f0f0f0", corner_radius=999, width=45, height=30)
            percent_label.place(relx=1.0, y=15, anchor="ne", x=-10)

last_projects = LastProjects(main_frame)
last_projects.place(x=30, y=620)

# === Main Loop ===
root.mainloop()

