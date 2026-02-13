from PIL import Image,ImageTk
import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
from PIL import Image
import csv
import numpy as np
from numpy import asarray
from numpy import expand_dims
from time import ctime
import time
import os
from os import listdir
import pickle
import cv2
from keras_facenet import FaceNet
HaarCascade = cv2.CascadeClassifier(cv2.samples.findFile(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'))
MyFaceNet = FaceNet()
import datetime
now = datetime.datetime.now()
formatted_date = now.strftime("%Y-%m-%d ")
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("yourfile.json")
### # إعدادات عامة للواجهة
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

#---------- الإعدادات الأساسية للنافذة الرئيسية -----------#

app = ctk.CTk(fg_color="#f9f9f9")
app.title("Facial Detection")
app.geometry("850x550")
app.resizable(False, False)
# تم التعديل هنا
app.iconbitmap("imgfac/Gemini_Generated_Image_x6jazkx6jazkx6ja.ico")

#----------- الشريط الجانبي (ToolBar) -----------#

toolbar = ctk.CTkFrame(app, width=200, corner_radius=0)
toolbar.pack(side="left", fill="y")
toolbar.pack_propagate(False)
toolbar.configure(fg_color="black") 

#----------- المتغيرات العامة -----------#
dir_pathi = "./fotoPeserta/"  # تأكد من وجود هذا المسار
if not os.path.exists(dir_pathi):
    os.makedirs(dir_pathi)
folder_path = "fcfolderr"  # يجب تعديل هذا المسار حسب مكان الملفات
HaarCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
database = {}
dir_path = "./imagesmehdi/"
fire=""

#----------- دالة إضافة مستخدم جديد -----------#
def open_add_user_window():
    # إنشاء نافذة جديدة منبثقة
    popup = ctk.CTkToplevel()
    popup.title("Add User")
    popup.geometry("400x220")
    popup.resizable(False, False)
    popup.grab_set()
    popup.focus_set()
    popup.transient()

    # عنوان الإدخال
    name_label = ctk.CTkLabel(popup, text="Enter Name:", font=ctk.CTkFont(size=14))
    name_label.pack(pady=(20, 5))

    # حقل إدخال الاسم
    name_entry = ctk.CTkEntry(popup, width=300)
    name_entry.pack()

    # حالة الصورة
    image_label = ctk.CTkLabel(popup, text="No image captured yet.", text_color="gray")
    image_label.pack(pady=(10, 10))

    def capture_from_camera():
        nameid = name_entry.get().strip()

        # التحقق من وجود اسم
        if not nameid:
            image_label.configure(text="Please enter a name first.", text_color="red")
            return

        # التحقق من وجود ملف الأسماء، وإنشاؤه إذا لم يوجد
        if not os.path.exists("test.txt"):
            with open("test.txt", "w"): pass

        with open("test.txt", "r") as file:
            content = file.read()

        # التحقق من تكرار الاسم
        if nameid in content:
            messagebox.showwarning('Info', f'Name "{nameid}" already exists. Please choose another name.')
            return
        else:
            with open("test.txt", "a") as file:
                file.write(f"\n{nameid}")

        # تشغيل الكاميرا والتقاط الوجه
        video = cv2.VideoCapture(1)
        count = 0

        while True:
            ret, frame = video.read()
            if not ret:
                break

            faces = HaarCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=4)
            for x, y, w, h in faces:
                count += 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.imshow("Camera", frame)
                cv2.waitKey(1)

                if count > 30:
                    if not os.path.exists(dir_pathi):
                        os.makedirs(dir_pathi)
                    image_path = os.path.join(dir_pathi, f"{nameid}.jpg")
                    cv2.imwrite(image_path, frame[y:y+h, x:x+w])
                    break

            if count > 30:
                break

        video.release()
        cv2.destroyAllWindows()
        popup.destroy()

    # زر لبدء التصوير من الكاميرا
    capture_button = ctk.CTkButton(popup, text="Capture", command=capture_from_camera, fg_color="#007acc")
    capture_button.pack(pady=(10, 20))

def search():
    rot = ctk.CTkToplevel()
    rot.title("Search User")
    rot.geometry('600x400+400+80')
    rot.resizable(False, False)
    rot.grab_set()
    rot.focus_set()
    rot.transient()
    
    def sumer():
        total = []
        name = enr1.get().lower()
        month = enr2.get().lower()
        year = enr3.get().lower()
        day1 = enr4.get().lower()
        day2 = enr5.get().lower()
        a = int(day1)
        b = int(day2)

        for i in range(a, b + 1):
            file_name = f"{year}-{month}-{'0' + str(i) if i < 10 else i} .csv"
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, "r") as csvfile:
                    reader = csv.reader(csvfile)
                    nll = [row[2] for row in reader if row[0].lower() == name]
                    if nll:
                        time1 = list(map(int, nll[0].split(":")))
                        time2 = list(map(int, nll[-1].split(":")))
                        total_diff = (time2[0] - time1[0]) * 60 + (time2[1] - time1[1])
                        total.append(total_diff)
            except FileNotFoundError:
                continue

        result = sum(total)
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("end", f"{result} minute")
        text_widget.configure(state="disabled")

    def cancel():
        enr1.delete(0, "end")
        enr2.delete(0, "end")
        enr3.delete(0, "end")
        enr4.delete(0, "end")
        enr5.delete(0, "end")
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.configure(state="disabled")

    def searchs():
        name = enr1.get().lower()
        month = enr2.get().lower()
        year = enr3.get().lower()
        day1 = enr4.get().lower()
        day2 = enr5.get().lower()
        a = int(day1)
        b = int(day2)
        disks = []

        for i in range(a, b + 1):
            file_name = f"{year}-{month}-{'0' + str(i) if i < 10 else i} .csv"
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, "r") as csvfile:
                    reader = csv.reader(csvfile)
                    found = False
                    for row in reader:
                        if row[0].lower() == name:
                            disks.append(f"Found in {file_name}: {row}")
                            found = True
                            break
                    if not found:
                        disks.append(f"Not found in {file_name}")
            except FileNotFoundError:
                disks.append(f"{file_name} does not exist")

        result_text = "\n".join(disks)
        text_widget.configure(state="normal")
        text_widget.delete("1.0", "end")
        text_widget.insert("end", result_text)
        text_widget.configure(state="disabled")

    enr1 = ctk.CTkEntry(rot, width=100, placeholder_text="Name")
    enr1.place(x=100, y=20)
    ctk.CTkLabel(rot, text="Name", text_color="white").place(x=10, y=20)

    enr2 = ctk.CTkEntry(rot, width=100, placeholder_text="Month")
    enr2.place(x=100, y=70)
    ctk.CTkLabel(rot, text="Month", text_color="white").place(x=10, y=70)

    enr3 = ctk.CTkEntry(rot, width=100, placeholder_text="Year")
    enr3.place(x=100, y=120)
    ctk.CTkLabel(rot, text="Year", text_color="white").place(x=10, y=120)

    enr4 = ctk.CTkEntry(rot, width=100, placeholder_text="Day From")
    enr4.place(x=100, y=170)
    ctk.CTkLabel(rot, text="Day From", text_color="white").place(x=10, y=170)

    enr5 = ctk.CTkEntry(rot, width=100, placeholder_text="Day To")
    enr5.place(x=100, y=220)
    ctk.CTkLabel(rot, text="Day To", text_color="white").place(x=10, y=220)
    # زر الإلغاء بدون صورة
    cancel_button = ctk.CTkButton(rot, text="Cancel", command=cancel, width=70)
    cancel_button.place(x=240, y=60)
    search_button = ctk.CTkButton(rot, text="Search", command=searchs, width=70)
    search_button.place(x=500, y=60)
    sum_button = ctk.CTkButton(rot, text="Sum", command=sumer, width=60)
    sum_button.place(x=370, y=60)

    text_widget = ctk.CTkTextbox(rot, height=160, width=350, wrap="word")
    text_widget.insert("end", "")
    text_widget.configure(state="disabled")
    text_widget.place(x=220, y=140)

    rot.mainloop()
#### train data
def traindata():
    for filename in listdir(dir_pathi):
        path = dir_pathi + filename
        gbr2 = cv2.imread(dir_pathi + filename)
    
        wajah = HaarCascade.detectMultiScale(gbr2,1.1,4)
    
        if len(wajah)>0:
            x1, y1, width, height = wajah[0]         
        else:
            x1, y1, width, height = 1, 1, 10, 10
        
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
    
        gbr = cv2.cvtColor(gbr2, cv2.COLOR_BGR2RGB)
        gbr = Image.fromarray(gbr)                  # konversi dari OpenCV ke PIL
        gbr_array = asarray(gbr)
    
        face = gbr_array[y1:y2, x1:x2]                        
    
        face = Image.fromarray(face)                        
        face = face.resize((160,160))
        face = asarray(face)
    
        face = expand_dims(face, axis=0)
        signature = MyFaceNet.embeddings(face)
    
        database[os.path.splitext(filename)[0]]=signature
    
    with open('database.pkl', 'wb') as f:       
        pickle.dump(database, f)
#### processing
def processing():
    global  fire
# Load the database
    with open('database.pkl', 'rb') as f:
        database = pickle.load(f)

    cap = cv2.VideoCapture(1)
    isme='l'
    t=[]
    koo=[""]
    ss=[""]
    threshold = 1
    while(1):
        _, gbr1 = cap.read()
    
        wajah = HaarCascade.detectMultiScale(gbr1,1.1,4)
    
        if len(wajah)>0:
            x1, y1, width, height = wajah[0]        
        else:
            x1, y1, width, height = 1, 1, 10, 10
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        gbr = cv2.cvtColor(gbr1, cv2.COLOR_BGR2RGB)
        gbr = Image.fromarray(gbr)                  # konversi dari OpenCV ke PIL
        gbr_array = asarray(gbr)
    
        face = gbr_array[y1:y2, x1:x2]                        
    
        face = Image.fromarray(face)                        
        face = face.resize((160,160))
        face = asarray(face)
   
        face = expand_dims(face, axis=0)
        signature = MyFaceNet.embeddings(face)
    
        min_dist=100
        identity=' '   
        for key, value in database.items() :
            dist = np.linalg.norm(value-signature)
            if dist <min_dist :
                      
                min_dist = dist
                identity = key      
        if min_dist > threshold:
            identity = 'unknown'    
        cv2.putText(gbr1,identity, (x1, y1-10),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.rectangle(gbr1,(x1,y1),(x2,y2), (0,255,0), 2)
        
        cv2.imshow('res',gbr1)
        if isme==identity:
            koo.append(identity)
            if len(koo)==8:
                koo=[""]
                if identity not in ss and  identity != "unknown" :
                    ss.append(identity)
                    t.append(identity)
                    iii=identity
                    fire=identity
                    
                    ii=ctime()
                    noww = datetime.datetime.now()
                    current_hour = noww.hour
                    current_minute = noww.minute
                    iiii=f"{current_hour}:{current_minute}"
                    print(current_minute)
                    file_name=formatted_date+".csv"
                    file_path = os.path.join(folder_path, file_name)
                    data=[[iii,ii,iiii]]
                    with open(file_path, "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerows(data) 
                    print(t)
                    cv2.imwrite(os.path.join(dir_path, identity+"captured_image.jpg"), gbr1)    
        if isme!=identity:
            koo=[""]
        isme=identity
        
        if cv2.waitKey(1) & 0xFF == ord('q') :
            cap.release()
            cv2.destroyAllWindows()
            return
    app.after(10, processing)
#-------------------- About Us --------------------#

def aboutus():
    rot1 = ctk.CTkToplevel()
    rot1.title("About Us")
    rot1.geometry('800x400')
    rot1.resizable(False, False)
    rot1.grab_set()
    rot1.focus_set()
    rot1.transient()
    rot1.configure(fg_color="#131314") 
    # تم التعديل هنا
    welcome_image1 = Image.open("imgfac/Helloimage.PNG")
    welcome_photo1 = ctk.CTkImage(dark_image=welcome_image1, size=(300, 150))
    image_label1 = ctk.CTkLabel(rot1, image=welcome_photo1, text="")
    image_label1.pack(pady=1)
    text_us="We are a group of passionate programmers and engineers aiming to elevate the standards of industrial facilities in Algeria. Our vision is to bring modern technology to every corner of the country—for all of us, and for future generations. As part of our graduation project, we are developing an intelligent platform for monitoring and managing industrial faults, integrated with a facial recognition-based attendance system. Our goal is not only to improve industrial efficiency but also to enhance worker safety and well-being through health tracking features such as blood pressure and glucose monitoring. Through innovation, dedication, and collaboration, we aspire to be a driving force in the digital transformation of Algerian industry"
    scroll_frame = ctk.CTkScrollableFrame(rot1, width=200, height=200, fg_color="#1a1a1a")
    scroll_frame.pack(padx=10, pady=10, fill="both", expand=False)
    text_label = ctk.CTkLabel(scroll_frame, text=text_us, font=ctk.CTkFont(size=13), wraplength=450, justify="left")
    text_label.pack(padx=10, pady=10, anchor="center")

#---------------------Button Help ----------------------------------------------------------------------------------------#

def helpyou():
    rot2 = ctk.CTkToplevel()
    rot2.title("Help")
    rot2.geometry('600x500')
    rot2.resizable(False, False)
    rot2.transient()
    rot2.configure(fg_color="#131314")
    # تم التعديل هنا
    welcome_image1 = Image.open("imgfac/Helloimage.PNG")
    welcome_photo1 = ctk.CTkImage(dark_image=welcome_image1, size=(300, 150))
    image_label1 = ctk.CTkLabel(rot2, image=welcome_photo1, text="")
    image_label1.pack(pady=1)
    content_frame = ctk.CTkFrame(rot2, fg_color="transparent")
    content_frame.pack(padx=10, pady=10, fill="both", expand=True)
    text_help = "If you need help call for Us"
    text_label1 = ctk.CTkLabel(content_frame, text=text_help, font=ctk.CTkFont(size=13), wraplength=450, justify="left")
    text_label1.pack(padx=10, pady=10, anchor="w")
    contacts = [
        "BOURBIA Oussila Ing/Pro/Doc: 0699 18 72 19",
        "LABSI Mohamed Souliemen Ing/Dev/Pro: 0797 27 02 47",
        "LABSI Mehdi Ing: 0549 16 08 82",
        "Berkane Mohammed Ing: 0796 23 61 50",
        "KHALFI Kaouther Anfel Ing: 0792 82 51 55 ",
        "HABCHI Boutheina Nesrine Ing: 0796 75 41 12"
    ]
    for contact in contacts:
        ctk.CTkLabel(content_frame, text=contact, text_color="white", anchor="w").pack(anchor="w", padx=20, pady=5)


#----------Buttons-------------------------------------------------------------#
def add_toolbar_button(icon_path, text, command=None, side="top"):
    icon = ctk.CTkImage(light_image=Image.open(icon_path), size=(30, 30))
    btn = ctk.CTkButton(
        toolbar, image=icon, text=text, width=200, height=50,
        fg_color="#000000", hover_color="#1f1f1f",
        compound="left", anchor="w", corner_radius=0, font=("", 15),
        command=command
    )
    if side == "bottom":
        btn.pack(side="bottom", pady=0.25)
    else:
        btn.pack(pady=0.25)
    return btn
#####################################server###################
def sever():
   
    ef = db.reference('student')
    ef.child("admi").child("pur").set(fire)
    print(fire)
    
# تم التعديل هنا لجميع الأزرار
add_toolbar_button("imgfac/house.png", "Home")
add_toolbar_button("imgfac/search-user.png", "Search",command=search)
add_toolbar_button("imgfac/dedicated-server.png", "Server",command=sever)
add_toolbar_button("imgfac/add-user.png", "Add User", command=open_add_user_window)
add_toolbar_button("imgfac/algorithms.png", "Processing", command=processing)
add_toolbar_button("imgfac/database-storage.png", "Data",command=traindata)
add_toolbar_button("imgfac/setting.png", "Setting", side="bottom")
add_toolbar_button("imgfac/user.png", "About Us", side="bottom",command=aboutus)
add_toolbar_button("imgfac/question-mark.png", "Help", side="bottom",command=helpyou)

#---------- واجهة الترحيب والصور ----------#
try:
    label_app = ctk.CTkLabel(app, text="Welcome To Our Company", font=("Arial", 16), text_color="black")
    label_app.pack(pady=10)

    # تم التعديل هنا
    welcome_image = Image.open("imgfac/Logo du Moniteur Industriel Intelligent.png")
    welcome_photo = ctk.CTkImage(dark_image=welcome_image, size=(300, 300))
    image_label = ctk.CTkLabel(app, image=welcome_photo, text="")
    image_label.pack(pady=1)

    label_app1 = ctk.CTkLabel(app, text="This is our Project", font=("Arial", 16), text_color="black")
    label_app1.pack(pady=10)

except Exception as e:
    error_label = ctk.CTkLabel(app, text=f"Error: {e}", text_color="red")
    error_label.pack(pady=20)

#---------- صور إضافية ----------#
def add_side_image(image_path, side, padx):
    img = Image.open(image_path)
    photo = ctk.CTkImage(dark_image=img, size=(125, 125))
    lbl = ctk.CTkLabel(app, image=photo, text="")
    lbl.pack(side=side, padx=padx, pady=20)

# تم التعديل هنا للصور الجانبية
add_side_image("imgfac/photo_2025-05-28_21-51-07.jpg", "left", 30)
add_side_image("imgfac/IFMCP.jpg", "right", 30)
add_side_image("imgfac/WorkerHealth Logo Design.png", "right", 70)

#---------- تشغيل التطبيق ----------#
app.mainloop()
