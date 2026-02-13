from PIL import Image, ImageTk
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import csv
import numpy as np
from numpy import asarray, expand_dims
from time import ctime
import time
import os
from os import listdir
import pickle
import cv2
from keras_facenet import FaceNet
import datetime
import firebase_admin
from firebase_admin import credentials, db

# ----------- إعدادات الموديلات والوقت ----------- #
# تحميل مصنف الوجوه وموديل FaceNet
HaarCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
MyFaceNet = FaceNet()

now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d ")

# إعداد Firebase (تأكد من وجود ملف yourfile.json بجانب الكود)
# cred = credentials.Certificate("yourfile.json")

# ----------- إعدادات الواجهة ----------- #
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk(fg_color="#f9f9f9")
app.title("Facial Detection - Optimized for CPU")
app.geometry("850x550")
app.resizable(False, False)

# أيقونة البرنامج من مجلد imgfac
try:
    app.iconbitmap("imgfac/Gemini_Generated_Image_x6jazkx6jazkx6ja.ico")
except:
    pass

# ----------- الشريط الجانبي (ToolBar) ----------- #
toolbar = ctk.CTkFrame(app, width=200, corner_radius=0)
toolbar.pack(side="left", fill="y")
toolbar.pack_propagate(False)
toolbar.configure(fg_color="black") 

# ----------- المتغيرات العامة ----------- #
dir_pathi = "./fotoPeserta/"  
if not os.path.exists(dir_pathi):
    os.makedirs(dir_pathi)

folder_path = "fcfolderr"  
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

database = {}
dir_path = "./imagesmehdi/"
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

fire = ""

# ----------- دالة إضافة مستخدم جديد ----------- #
def open_add_user_window():
    popup = ctk.CTkToplevel()
    popup.title("Add User")
    popup.geometry("400x220")
    popup.resizable(False, False)
    popup.grab_set()
    popup.focus_set()
    popup.transient()

    ctk.CTkLabel(popup, text="Enter Name:", font=ctk.CTkFont(size=14)).pack(pady=(20, 5))
    name_entry = ctk.CTkEntry(popup, width=300)
    name_entry.pack()

    image_label = ctk.CTkLabel(popup, text="No image captured yet.", text_color="gray")
    image_label.pack(pady=(10, 10))

    def capture_from_camera():
        nameid = name_entry.get().strip()
        if not nameid:
            image_label.configure(text="Please enter a name first.", text_color="red")
            return

        if not os.path.exists("test.txt"):
            with open("test.txt", "w"): pass

        with open("test.txt", "r") as file:
            content = file.read()

        if nameid in content:
            messagebox.showwarning('Info', f'Name "{nameid}" already exists.')
            return
        else:
            with open("test.txt", "a") as file:
                file.write(f"\n{nameid}")

        video = cv2.VideoCapture(0)
        count = 0
        while True:
            ret, frame = video.read()
            if not ret: break
            faces = HaarCascade.detectMultiScale(frame, 1.1, 4)
            for x, y, w, h in faces:
                count += 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.imshow("Camera", frame)
                cv2.waitKey(1)
                if count > 30:
                    image_path = os.path.join(dir_pathi, f"{nameid}.jpg")
                    cv2.imwrite(image_path, frame[y:y+h, x:x+w])
                    break
            if count > 30: break
        video.release()
        cv2.destroyAllWindows()
        popup.destroy()

    ctk.CTkButton(popup, text="Capture", command=capture_from_camera, fg_color="#007acc").pack(pady=(10, 20))

# ----------- دالة البحث عن السجلات ----------- #
def search():
    rot = ctk.CTkToplevel()
    rot.title("Search User")
    rot.geometry('600x400+400+80')
    rot.resizable(False, False)
    rot.grab_set()

    def sumer():
        total = []
        name, month, year = enr1.get().lower(), enr2.get().lower(), enr3.get().lower()
        d1, d2 = int(enr4.get()), int(enr5.get())
        for i in range(d1, d2 + 1):
            file_name = f"{year}-{month}-{'0' + str(i) if i < 10 else i} .csv"
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, "r") as csvfile:
                    reader = csv.reader(csvfile)
                    nll = [row[2] for row in reader if row[0].lower() == name]
                    if nll:
                        t1, t2 = list(map(int, nll[0].split(":"))), list(map(int, nll[-1].split(":")))
                        total.append((t2[0] - t1[0]) * 60 + (t2[1] - t1[1]))
            except: continue
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("end", f"Total: {sum(total)} minutes")
        text_widget.configure(state="disabled")

    def searchs():
        name, month, year = enr1.get().lower(), enr2.get().lower(), enr3.get().lower()
        d1, d2 = int(enr4.get()), int(enr5.get())
        disks = []
        for i in range(d1, d2 + 1):
            f_name = f"{year}-{month}-{'0' + str(i) if i < 10 else i} .csv"
            f_path = os.path.join(folder_path, f_name)
            if os.path.exists(f_path):
                with open(f_path, "r") as f:
                    reader = csv.reader(f)
                    found = [row for row in reader if row[0].lower() == name]
                    disks.append(f"{f_name}: Found" if found else f"{f_name}: Not Found")
            else: disks.append(f"{f_name}: Missing")
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("end", "\n".join(disks))
        text_widget.configure(state="disabled")

    enr1 = ctk.CTkEntry(rot, width=100, placeholder_text="Name"); enr1.place(x=100, y=20)
    enr2 = ctk.CTkEntry(rot, width=100, placeholder_text="Month"); enr2.place(x=100, y=70)
    enr3 = ctk.CTkEntry(rot, width=100, placeholder_text="Year"); enr3.place(x=100, y=120)
    enr4 = ctk.CTkEntry(rot, width=100, placeholder_text="Day From"); enr4.place(x=100, y=170)
    enr5 = ctk.CTkEntry(rot, width=100, placeholder_text="Day To"); enr5.place(x=100, y=220)
    
    ctk.CTkButton(rot, text="Search", command=searchs, width=70).place(x=500, y=60)
    ctk.CTkButton(rot, text="Sum", command=sumer, width=60).place(x=370, y=60)
    text_widget = ctk.CTkTextbox(rot, height=160, width=350); text_widget.place(x=220, y=140)

# ----------- معالجة البيانات وتدريب الموديل ----------- #
def traindata():
    for filename in listdir(dir_pathi):
        gbr2 = cv2.imread(os.path.join(dir_pathi, filename))
        wajah = HaarCascade.detectMultiScale(gbr2, 1.1, 4)
        if len(wajah) > 0:
            x1, y1, w, h = wajah[0]
            face = gbr2[y1:y1+h, x1:x1+w]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = Image.fromarray(face).resize((160, 160))
            face = expand_dims(asarray(face), axis=0)
            database[os.path.splitext(filename)[0]] = MyFaceNet.embeddings(face)
    with open('database.pkl', 'wb') as f:
        pickle.dump(database, f)
    messagebox.showinfo("Success", "Data trained successfully!")

def processing():
    global fire
    if not os.path.exists('database.pkl'):
        messagebox.showerror("Error", "No database found. Please train data first.")
        return
    with open('database.pkl', 'rb') as f:
        db_loaded = pickle.load(f)

    cap = cv2.VideoCapture(0)
    isme, koo, ss, threshold = 'l', [""], [""], 1.0

    while True:
        _, frame = cap.read()
        wajah = HaarCascade.detectMultiScale(frame, 1.1, 4)
        if len(wajah) > 0:
            x1, y1, w, h = wajah[0]
            x2, y2 = x1 + w, y1 + h
            face = cv2.cvtColor(frame[y1:y2, x1:x2], cv2.COLOR_BGR2RGB)
            face = Image.fromarray(face).resize((160, 160))
            signature = MyFaceNet.embeddings(expand_dims(asarray(face), axis=0))
            
            min_dist, identity = 100, ' '
            for key, val in db_loaded.items():
                dist = np.linalg.norm(val - signature)
                if dist < min_dist:
                    min_dist, identity = dist, key
            
            if min_dist > threshold: identity = 'unknown'
            
            cv2.putText(frame, identity, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            if isme == identity:
                koo.append(identity)
                if len(koo) == 8:
                    koo = [""]
                    if identity not in ss and identity != "unknown":
                        ss.append(identity)
                        fire = identity
                        noww = datetime.datetime.now()
                        log_data = [[identity, ctime(), f"{noww.hour}:{noww.minute}"]]
                        f_name = formatted_date + ".csv"
                        with open(os.path.join(folder_path, f_name), "a", newline="") as f:
                            csv.writer(f).writerows(log_data)
                        cv2.imwrite(os.path.join(dir_path, identity + "_cap.jpg"), frame)
            else: koo = [""]
            isme = identity

        cv2.imshow('Face Recognition (Press Q to quit)', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

# ----------- معلومات عنا المساعدة ----------- #
def aboutus():
    rot1 = ctk.CTkToplevel(); rot1.geometry('800x400')
    rot1.configure(fg_color="#131314")
    img = ctk.CTkImage(dark_image=Image.open("imgfac/Helloimage.PNG"), size=(300, 150))
    ctk.CTkLabel(rot1, image=img, text="").pack(pady=10)
    txt = "We are a group of passionate engineers... (Algerian Digital Transformation)"
    scroll = ctk.CTkScrollableFrame(rot1, width=500, height=200, fg_color="#1a1a1a")
    scroll.pack(pady=10); ctk.CTkLabel(scroll, text=txt, wraplength=450).pack()

def helpyou():
    rot2 = ctk.CTkToplevel(); rot2.geometry('600x500')
    rot2.configure(fg_color="#131314")
    img = ctk.CTkImage(dark_image=Image.open("imgfac/Helloimage.PNG"), size=(300, 150))
    ctk.CTkLabel(rot2, image=img, text="").pack()
    contacts = ["LABSI Mohamed Souliemen: 0797 27 02 47", "LABSI Mehdi: 0549 16 08 82"]
    for c in contacts: ctk.CTkLabel(rot2, text=c).pack(pady=5)

# ----------- الأزرار والقائمة الجانبية ----------- #
def add_toolbar_button(icon_path, text, command=None, side="top"):
    icon = ctk.CTkImage(light_image=Image.open(icon_path), size=(30, 30))
    btn = ctk.CTkButton(toolbar, image=icon, text=text, width=200, height=50, fg_color="black", hover_color="#1f1f1f", compound="left", anchor="w", command=command)
    btn.pack(side=side, pady=2)

add_toolbar_button("imgfac/house.png", "Home")
add_toolbar_button("imgfac/search-user.png", "Search", command=search)
add_toolbar_button("imgfac/dedicated-server.png", "Server")
add_toolbar_button("imgfac/add-user.png", "Add User", command=open_add_user_window)
add_toolbar_button("imgfac/algorithms.png", "Processing", command=processing)
add_toolbar_button("imgfac/database-storage.png", "Data", command=traindata)
add_toolbar_button("imgfac/question-mark.png", "Help", side="bottom", command=helpyou)
add_toolbar_button("imgfac/user.png", "About Us", side="bottom", command=aboutus)

# ----------- الواجهة الرئيسية ----------- #
ctk.CTkLabel(app, text="Welcome To Our Company", font=("Arial", 20), text_color="black").pack(pady=10)
logo_img = ctk.CTkImage(dark_image=Image.open("imgfac/Logo du Moniteur Industriel Intelligent.png"), size=(250, 250))
ctk.CTkLabel(app, image=logo_img, text="").pack()

# صور جانبية أسفل الواجهة
f_frame = ctk.CTkFrame(app, fg_color="transparent")
f_frame.pack(side="bottom", pady=20)

def add_small_img(path):
    try:
        img = ctk.CTkImage(dark_image=Image.open(path), size=(100, 100))
        ctk.CTkLabel(f_frame, image=img, text="").pack(side="left", padx=20)
    except: pass

add_small_img("imgfac/photo_2025-05-28_21-51-07.jpg")
add_small_img("imgfac/IFMCP.jpg")
add_small_img("imgfac/WorkerHealth Logo Design.png")

app.mainloop()
