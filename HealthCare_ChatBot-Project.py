import subprocess
import tkinter as tk
from tkinter import *
import mysql.connector as sql
from tkinter import messagebox
import re
from tkcalendar import Calendar, DateEntry
import smtplib
from email.message import EmailMessage

import sys

win = tk.Tk()

page1 = Frame(win,width=925,height=600, bg='#fff')
page1.place(x=0, y=0)

page2 = Frame(win, width=925,height=600,bg='#fff')
page2.place(x=0, y=0)

page3 = Frame(win, width=925, height=600, bg='#fff')
page3.place(x=0, y=0)

page4 = Frame(win, width=925, height=600, bg='#fff')
page4.place(x=0, y=0)

img3 = PhotoImage(file='Health-Insurance.png')
Label(page3, image=img3, border=0, width=920, height=600, bg='white').place(x=20, y=70)

#MySQL DB Connections

m = sql.connect(host="localhost", user="root", passwd="*#@rajpatle20051308",
                database="regbotapp", auth_plugin = 'mysql_native_password',)

cursor = m.cursor()

# ################ Appointment ###############################

def booknow (ent1, ent2, ent3, ent4):

    name = ent1.get()
    phone = ent2.get()
    vdate = ent3.get()
    email = ent4.get()

    if len(name)>0 and len(phone)>0 and len(vdate)>0 and len(email)>0:

        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            vals = (name, phone, vdate, email)
            c = "insert into bookedappointment values(%s, %s, %s, %s)".format(name, phone, vdate,email)
            # insert_query = "INSERT INTO 'register' ('email', 'pass1', 'pass2') VALUES (%s,%s,%s)"
            cursor.execute(c, vals)
            m.commit()

            msg = EmailMessage()
            msg.set_content('Dear '+name + '\n\nI trust this email finds you well. We are writing to confirm your scheduled appointment with Health Care.'
                                           '\n\nAppointment Details:'
                                           '\nDate:'+vdate+','
                                           '\nTime: 11am to 8PM'
                                           '\n\nYour commitment to this meeting is greatly appreciated. If there are any changes or if you encounter any scheduling conflicts, '
                                            '\nkindly inform us promptly by replying to this email.'
                                            '\nThank you for choosing [Your Company/Organization Name]. We look forward to a successful engagement.'
                                            '\n\nBest Regards'
                                            '\nHealth Care')

            msg['Subject'] = ' Appointment Confirmation'
            msg['From'] = "rajpatlepro1308@gmail.com"
            msg['To'] = email
            # ________________________________________

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Connect to the server
            server.ehlo()
            server.login("rajpatlepro1308@gmail.com", "hfezmopqjvdzxfoj")  # Login to the email server
            server.send_message(msg)
            server.quit()  # Logout of the email server

            # ________________________________________
            messagebox.showinfo("Congress", "Your Appointment Booked Successfully.. !Please Check Your Email")
            page3.tkraise()
            # print("Valid email address")

        else:
            messagebox.showwarning("Warning", "Invalid Email Address")

    else:
        messagebox.showwarning("Warning", "Please Fill Carefully..")


def appointment():
    page4.tkraise()
    Frame(page4, width=925, height=65, bg='#28AE89').place(x=0, y=2)
    lb1 = Label(page4, text="GET AN APPOINTMENT", fg='white', bg='#28AE89',
                font=('Microsoft YaHei UI Light', 33, 'bold'))
    lb1.place(x=240, y=3)
#    --------------------------------------------------
    label1 = Label(page4, text="Your Full Name*", fg='black', bg='white', font=('Microsoft YaHei UI Light', 12))
    label1.place(x=100, y=130)
    ent1 = Entry(page4, width=30, fg='black', border=1, bg="#D3D3D3", font=('Microsoft YaHei UI Light', 12))
    ent1.place(x=100, y=160)

    label2 = Label(page4, text="Your Phone Number*", fg='black', bg='white', font=('Microsoft YaHei UI Light', 12))
    label2.place(x=450, y=130)
    ent2 = Entry(page4, width=30, fg='black', border=1, bg="#D3D3D3", font=('Microsoft YaHei UI Light', 12))
    ent2.place(x=450, y=160)

    label3 = Label(page4, text="Your Visit Date* M/D/Y", fg='black', bg='white', font=('Microsoft YaHei UI Light', 12))
    label3.place(x=100, y=270)
    ent3 = DateEntry(page4, width=26, fg='black', bg="#D3D3D3", bd=1, font=('Microsoft YaHei UI Light', 12))
    ent3.place(x=100, y=300)

    label4 = Label(page4, text="Your Email*", fg='black', bg='white', font=('Microsoft YaHei UI Light', 12))
    label4.place(x=450, y=270)
    ent4 = Entry(page4, width=30, fg='black', border=1, bg="#D3D3D3", font=('Microsoft YaHei UI Light', 12))
    ent4.place(x=450, y=300)

    Button(page4, width=20, pady=7, text='BOOK NOW', bg='#28AE89', fg='white', border=0,
           font=('Microsoft YaHei UI Light', 15, 'bold'),
           command=lambda: booknow(ent1, ent2, ent3, ent4)).place(x=180, y=400)

    Button(page4, width=7, pady=7, text='《 BACK', bg='#28AE89', fg='white', border=0,
           font=('Microsoft YaHei UI Light', 10, 'bold'),
           command=lambda: page3.tkraise()).place(x=800, y=530)
#   ---------------------------------------------


def healthcare():
    subprocess.call([sys.executable, 'hcbot.py', 'htmlfilename.htm'])
    # process = subprocess.run(["python", "hcbot.py"])

# ========================== Log In ================================


def LogIN():
    emailid = user.get()
    passw1 = code.get()

    c = "select * from register where email='{}' and pass2='{}'".format(emailid, passw1)
    cursor.execute(c)
    t = tuple(cursor.fetchall())

    if t == ():
        messagebox.showinfo("Warning", "Invalid Data")

    elif (emailid == "") or (passw1 == ""):
        messagebox.showinfo("Warning", "Please Fill The Form")
    else:
        page3.tkraise()
        Frame(page3, width=925, height=65, bg='#57a1f8').place(x=0, y=2)
        lb1 = Label(page3, text="Choose Your Options", fg='white', bg='#57a1f8', font=('Microsoft YaHei UI Light', 33, 'bold'))
        lb1.place(x=240, y=3)

        Button(page3, width=12, pady=7, text='《 Log Out', bg='#57a1f8', fg='white', border=0,font=('Microsoft YaHei UI Light', 10, 'bold'),
               command=lambda: page1.tkraise()).place(x=800, y=70)

        Button(page3, width=29, pady=7, text='GET APPOINTMENT 》', bg='#57a1f8', fg='white', border=0,font=('Microsoft YaHei UI Light', 13, 'bold'),
               command=lambda: appointment()).place(x=45, y=200)
        Button(page3, width=29, pady=7, text='HEALTHCARE CHATBOT 》', bg='#57a1f8', fg='white', border=0,font=('Microsoft YaHei UI Light', 13, 'bold'),
               command=lambda: healthcare()).place(x=45, y=320)

# ================================== End =============================================


img = PhotoImage(file='digi-col-login.png')
Label(page1, image=img, bg='white').place(x=10, y=30)

frame = Frame(page1, width=350, height=350, bg='white')
frame.place(x=530, y=70)

heading = Label(frame, text='Log In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)


def on_enter(e):
    user.delete(0, 'end')


def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Email Id*')


user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=50, y=80)
user.insert(0, 'Email Id*')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=290, height=2, bg='black').place(x=40, y=106)

# ========================================================

def on_ente(e):
    code.delete(0, 'end')

def on_leav(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password*')


code = Entry(frame, width=25, fg='black',show='*', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
code.place(x=50, y=160)
code.insert(0, 'Password*')
code.bind('<FocusIn>', on_ente)
code.bind('<FocusOut>', on_leav)

Frame(frame, width=290, height=2, bg='black').place(x=40, y=186)


Button(frame, width=39, pady=7, text='Log In', bg='#57a1f8', fg='white', border=0, command=lambda: LogIN()).place(x=45, y=204)
label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

sign_up = Button(frame, width=6, text='Sign Up', border=0, bg='white',command=lambda: page2.tkraise(), cursor='hand2', fg='#57a1f8')
sign_up.place(x=215, y=270)

################################################


def register():

    emailid = user2.get()
    passw1 = pass1.get()
    passw2 = conf_pass.get()

    if len(emailid)>0 and len(passw1)>0 and len(passw2)>0 and passw1 == passw2:

        if re.match(r"[^@]+@[^@]+\.[^@]+", emailid):
            vals = (emailid, passw1, passw2)
            c = "insert into register values(%s, %s, %s)".format(emailid, passw1, passw2)
            # insert_query = "INSERT INTO 'register' ('email', 'pass1', 'pass2') VALUES (%s,%s,%s)"
            cursor.execute(c, vals)
            m.commit()
            messagebox.showinfo("Congress", "Your account has been created Successfully..")
            page1.tkraise()
            # print("Valid email address")

        else:
            messagebox.showwarning("Warning", "Invalid Email Address")

    else:
        messagebox.showwarning("Warning", "Please Fill Carefully..")

img2 = PhotoImage(file='sign-up.png')
Label(page2, image=img2, border=0, bg='white').place(x=0, y=0)

frame2 = Frame(page2, width=350, height=390, bg='#fff')
frame2.place(x=500, y=50)


heading = Label(frame2, text='Sign Up', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=120, y=5)
# ========================================================
def on_enter(e):
    user2.delete(0, 'end')

def on_leave(e):
    name = user2.get()
    if name == '':
        user2.insert(0, 'Email Id*')

user2 = Entry(frame2, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user2.place(x=70, y=80)
user2.insert(0, 'Email Id*')
user2.bind('<FocusIn>', on_enter)
user2.bind('<FocusOut>',on_leave)

Frame(frame2, width=290, height=2, bg='black').place(x=40, y=106)

# ========================================================

def on_ente(e):
    pass1.delete(0, 'end')

def on_leav(e):
    name=pass1.get()
    if name == '':
        pass1.insert(0, 'Password*')


pass1 = Entry(frame2, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
pass1.place(x=70, y=160)
pass1.insert(0, 'Password*')
pass1.bind('<FocusIn>', on_ente)
pass1.bind('<FocusOut>', on_leav)

Frame(frame2, width=290, height=2, bg='black').place(x=40, y=186)

# ========================================================

def on_ente(e):
    conf_pass.delete(0, 'end')

def on_leav(e):
    name = conf_pass.get()
    if name == '':
        conf_pass.insert(0, 'Confirm Password*')

conf_pass = Entry(frame2, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
conf_pass.place(x=70, y=240)
conf_pass.insert(0, 'Confirm Password*')
conf_pass.bind('<FocusIn>', on_ente)
conf_pass.bind('<FocusOut>', on_leav)

Frame(frame2, width=290, height=2, bg='black').place(x=40, y=266)

# ========================================================

Button(frame2, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0,  command=lambda: register()).place(x=45, y=284)
label = Label(frame2, text="You have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=95, y=330)

sign_up = Button(frame2, width=6, text='LogIn', command=lambda: page1.tkraise(), border=0, bg='white', cursor='hand2', fg='#57a1f8')
sign_up.place(x=235, y=330)

#_______________________________________________________________
page2.tkraise()
win.geometry('925x600+300+100')
win.title("Healthcare App")
win.configure(bg='#fff')
win.resizable(False, False)
win.mainloop()