# calculate user expense
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager,Screen,SlideTransition

import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import firebase_admin
from firebase_admin import credentials, db


signedin_user=""
signedin_name=""
cred=credentials.Certificate("config.json")
firebase_admin.initialize_app(cred,{
    "databaseURL":"https://splitwise-57178-default-rtdb.firebaseio.com"
})

# --- Color Theme ---
Window.clearcolor = (0.01, 0.09, 0.17, 1)  # Dark Navy Blue

PRIMARY_COLOR = (0.2, 0.6, 0.8, 1)  # Teal Blue
SECONDARY_COLOR = (0.1, 0.4, 0.6, 1)
TEXT_COLOR = (1, 1, 1, 1)
BUTTON_TEXT_COLOR = (1, 1, 1, 1)


email_input_signup=None
password_input=None
name_input=None
user_data = {
    "otp": "",
    "email":"",
    "password":"",
    "name":""
}

print(user_data)

sm=ScreenManager()
sm.transition=SlideTransition()
#---write into the database-----

def go_to_signup(instance):
    sm.transition.direction='left'
    sm.current='Signup'
    
def go_to_login(instance):
    sm.transition.direction='right'
    sm.current='Login'
    
def go_to_dashboard(instance):
    sm.transition.direction='up'
    sm.current='Dashboard'
    
def go_to_group(instance):
    sm.transition.direction='down'
    sm.current='Group'

def go_to_expense(instance):
    sm.transition.direction='down'
    sm.current='Expense'
    
# --- Popup ---
def show_popup(title, message):
    popup = Popup(title=title, content=Label(text=message, color=TEXT_COLOR),
                  size_hint=(None, None), size=(300, 200),
                  background_color=SECONDARY_COLOR)
    popup.open()
    
def write_email_and_password(user_id,email,password,name):
    if user_id is None:
        user_id=random.randint(1,9999)
        ref=db.reference(f"users/{user_id}")
        ref.set({
            "name":name,
            "email":email,
            "password":password
        })
        print(f"User {user_id} has been added sucsessfuly!")
def send_otp(instance):
    email=email_input_signup.text.strip()
    if not email:
        show_popup('Error','Please enter a valid email.')
    
    otp=str(random.randint(100000,999999))
    user_data['otp']=otp
    user_data['email']=email
    
    sender_email='orangetree254@gmail.com'
    sender_password='ptwq denh qjub dvpo'
    subject='Your otp code'
    body=f'Your otp is {otp}.'
    
    message=MIMEMultipart()
    message['From']=sender_email
    message['To']=email
    message['Subject']=subject
    message.attach(MIMEText(body,'plain'))
    
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender_email,sender_password)
        server.sendmail(sender_email,email,message.as_string())
        server.quit()
        show_popup('Success','OTP sent')
    except:
        show_popup('Error','OTP was not able to be sent.')

def verify_otp(instance):
    global name_input_signup
    global email_input_signup
    global password_input_signup
    if otp_input_signup.text.strip()==user_data['otp']:
        show_popup('Success','Redirecting you to the next page!')
        sm.current="Dashboard"
        user_data['name']=name_input_signup.text.strip()
        name=user_data['name']
        user_data['email']=email_input_signup.text.strip()
        email=user_data['email']
        user_data['password']=password_input_signup.text.strip()
        password=user_data['password']
        write_email_and_password(None,email,password,name)
        
    else:
        show_popup('Error','Incorrect OTP!')
def on_submit(instance):
    global signedin_user
    global signedin_name
    email=email_input.text.strip()
    password=password_input.text.strip()
    if not email or not password:
        show_popup('Error','Please enter both email and password')
        return
    ref=db.reference('users')
    users_data=ref.get()
    found=False
    if users_data:
        for user_id,user_info in users_data.items():
            fetch_email=user_info['email']
            fetch_password=user_info['password']
            if fetch_email==email and fetch_password==password:
                found=True
                signedin_user=user_id
                signedin_name=user_info['name']
                break
    if found:
        show_popup('Success','Login was successful.')
        sm.current='Dashboard'
# ----SCREEN TEMPLATES----

# --- Login Screen ---
def build_login_screen():
    global email_input,password_input
    layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
    layout.add_widget(Label(text='[b]SmartSplit App[/b]', markup=True, font_size=36,
                            size_hint=(1, None), height=60, color="yellow"))

    float_layout = FloatLayout(size_hint=(1, 1))

    email_input = TextInput(hint_text='Email', multiline=False,
                            size_hint=(0.6, None), height=50,
                            pos_hint={'center_x': 0.5, 'center_y': 0.7},
                            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    password_input = TextInput(hint_text='Password', password=True, multiline=False,
                               size_hint=(0.6, None), height=50,
                               pos_hint={'center_x': 0.5, 'center_y': 0.55},
                               background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    submit_btn = Button(text='Login', size_hint=(0.4, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.4},
                        background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR,on_press=on_submit)
    

    float_layout.add_widget(email_input)
    float_layout.add_widget(password_input)
    float_layout.add_widget(submit_btn)

    layout.add_widget(float_layout)

    switch_btn = Button(text='New User? Go to Signup', size_hint=(1, None), height=50,
                        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR,on_press=go_to_signup)

    layout.add_widget(switch_btn)

    return layout

# --- Signup Screen ---
def build_signup_screen():
    global email_input_signup, otp_input_signup, password_input_signup, name_input_signup

    layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
    layout.add_widget(Label(text='[b]SIGN UP[/b]', markup=True, font_size=36,
                            size_hint=(1, None), height=60, color=TEXT_COLOR))

    float_layout = FloatLayout(size_hint=(1, 1))

    name_input_signup = TextInput(hint_text='Name', multiline=False,
                           size_hint=(0.6, None), height=50,
                           pos_hint={'center_x': 0.5, 'center_y': 0.85},
                           background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    email_input_signup = TextInput(hint_text='Email', multiline=False,
                                   size_hint=(0.6, None), height=50,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.70},
                                   background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    password_input_signup = TextInput(hint_text='Password', password=True, multiline=False,
                               size_hint=(0.6, None), height=50,
                               pos_hint={'center_x': 0.5, 'center_y': 0.55},
                               background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    generate_otp_btn = Button(text='Generate OTP', size_hint=(0.4, None), height=40,
                              pos_hint={'center_x': 0.5, 'center_y': 0.40},
                              background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR, on_press=send_otp)
    
    otp_input_signup = TextInput(hint_text='Enter OTP', multiline=False,
                                 size_hint=(0.6, None), height=50,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.25},
                                 background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    verify_btn = Button(text='Verify OTP', size_hint=(0.4, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.10},
                        background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR, on_press=verify_otp)


    float_layout.add_widget(name_input_signup)
    float_layout.add_widget(email_input_signup)
    float_layout.add_widget(password_input_signup)
    float_layout.add_widget(generate_otp_btn)
    float_layout.add_widget(otp_input_signup)
    float_layout.add_widget(verify_btn)

    layout.add_widget(float_layout)

    switch_btn = Button(text='Already a user? Go to Login', size_hint=(1, None), height=50,
                        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR,on_press=go_to_login)
    
    layout.add_widget(switch_btn)

    return layout

#-----Dashboard-----

def build_dashboard_screen():
  
    global owe_amount_label, other_owe_amount_label

    layout = FloatLayout(size_hint=(1, 1))

    # Welcome label
    welcome_label = Label(
        text=f'[b]WELCOME {signedin_name.upper()}![/b]',
        markup=True,
        font_size=28,
        size_hint=(None, None), size=(300, 30),
        pos_hint={'center_x': 0.5, 'top': 0.95},
        color="yellow"
    )
    layout.add_widget(welcome_label)

    # Info bar container
    info_float = FloatLayout(size_hint=(None, None), size=(650, 90),
                             pos_hint={'center_x': 0.5, 'top': 0.88})



    # Horizontal box for balances and refresh
    info_box = BoxLayout(orientation='horizontal',
                         spacing=30,
                         size_hint=(None, None),
                         size=(600, 60),
                         pos_hint={'center_x': 0.5, 'center_y': 0.5})

    # YOU OWE section
    owe_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(120, 60))
    owe_label = Label(text='[b]YOU OWE[/b]', markup=True, font_size=18,
                      color="yellow", size_hint=(1, 0.4))
    owe_amount_label = Label(text=str(0), font_size=24,
                             color=TEXT_COLOR, size_hint=(1, 0.6))
    owe_box.add_widget(owe_label)
    owe_box.add_widget(owe_amount_label)

    # OTHERS OWE YOU section
    other_owe_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(160, 60))
    other_owe_label = Label(text='[b]OTHERS OWE YOU[/b]', markup=True,
                            font_size=18, color="yellow", size_hint=(1, 0.4))
    other_owe_amount_label = Label(text=str(0), font_size=24,
                                   color=TEXT_COLOR, size_hint=(1, 0.6))
    other_owe_box.add_widget(other_owe_label)
    other_owe_box.add_widget(other_owe_amount_label)

   
    refresh_btn = Button(
        text='Refresh',
        size_hint=(None, None), size=(100, 40),
        background_color=SECONDARY_COLOR,
        color=(1, 1, 1, 1),
        font_size=16,
       
    )

    # Add all to the info box
    info_box.add_widget(owe_box)
    info_box.add_widget(other_owe_box)
    info_box.add_widget(refresh_btn)

    info_float.add_widget(info_box)
    layout.add_widget(info_float)

    # Group members
    group =["member1", "member2", "member3"]  # Placeholder for group members
    num_members = len(group)
    cols = 3 + num_members

    # Table
    table = GridLayout(cols=cols, size_hint_y=None, spacing=5, padding=5)
   # table.bind(minimum_height=table.setter('height'))

    # Add header row
    headers = ['DESCRIPTION', 'PAID BY', 'AMOUNT'] + group
    for col in headers:
        table.add_widget(Label(text=f"[b]{col}[/b]", markup=True,
                            color="yellow", size_hint_y=None, height=40))
    ref=db.reference('transaction')
    transactions=ref.get()
    if transactions:
        for transaction_id, transaction_info in transactions.items():
            description=transaction_info.get('description','')
            who_paid=transaction_info.get('who_paid','')
            amount=transaction_info.get('amount',0.00)
            table.add_widget(Label(text=str(description),size_hint_y=None,height=40))
            table.add_widget(Label(text=str(who_paid),size_hint_y=None,height=40))
            table.add_widget(Label(text=str(amount),size_hint_y=None,height=40))
            split=transaction_info.get('split',{})
            for member in group:
                share=split.get(member,"")
                if isinstance(share,(int,float)):
                    share_text=f'{share:.2f}'
                elif share=='' or share is None:
                    share_text='-'
                else:
                    try:
                        share_text=f'{float(share):.2f}'
                    except:
                        share_text=str(share)
                table.add_widget(Label(text=f'Share={share_text}',size_hint_y=None,height=30))

    # Buttons at bottom
    btn_layout = BoxLayout(
        orientation='horizontal',
        size_hint=(1, None), height=60, spacing=20, padding=[0, 0, 0, 10]
    )
    add_expense_btn = Button(
        text='Add Expense',
        size_hint=(0.5, 1),
        background_color=SECONDARY_COLOR,
        color=(1, 1, 1, 1),
        on_press=go_to_expense
    )
    add_group_members_btn = Button(
        text='Add Group Members',
        size_hint=(0.5, 1),
        background_color=SECONDARY_COLOR,
        color=(1, 1, 1, 1),
        on_press=go_to_group
    )
    
    btn_layout.add_widget(add_expense_btn)
    btn_layout.add_widget(add_group_members_btn)
    layout.add_widget(btn_layout)

    return layout

#---- Add Group Member Screen ---
def build_add_group_screen():
        global member_name_input, member_email_input, contact_input
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        layout.add_widget(Label(
            text='[b]ADD GROUP MEMBER[/b]', markup=True, font_size=36,
            size_hint=(1, None), height=60, color="yellow"
        ))

        float_layout = FloatLayout(size_hint=(1, 1))

        # Name
        name_label = Label(text='Name:', size_hint=(None, None), size=(100, 40),
                        pos_hint={'center_x': 0.2, 'center_y': 0.75}, color=TEXT_COLOR)
        member_name_input = TextInput(size_hint=(0.6, None), height=50,
                                    pos_hint={'center_x': 0.6, 'center_y': 0.75},
                                    background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        # Email
        email_label = Label(text='Email:', size_hint=(None, None), size=(100, 40),
                            pos_hint={'center_x': 0.2, 'center_y': 0.6}, color=TEXT_COLOR)
        member_email_input = TextInput(size_hint=(0.6, None), height=50,
                                    pos_hint={'center_x': 0.6, 'center_y': 0.6},
                                    background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        # Contact
        contact_label = Label(text='Contact (optional):', size_hint=(None, None), size=(150, 40),
                            pos_hint={'center_x': 0.2, 'center_y': 0.45}, color=TEXT_COLOR)
        contact_input = TextInput(size_hint=(0.6, None), height=50,
                                pos_hint={'center_x': 0.6, 'center_y': 0.45},
                                background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        # Buttons
        add_btn = Button(text='Add Member', size_hint=(0.4, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.3},
                        background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR,
                        on_press=add_members
                       )

        back_btn = Button(text='Back to Dashboard', size_hint=(1, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.15},
                        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR,
                        on_press=go_to_dashboard
                       )

        # Add to layout
        float_layout.add_widget(name_label)
        float_layout.add_widget(member_name_input)
        float_layout.add_widget(email_label)
        float_layout.add_widget(member_email_input)
        float_layout.add_widget(contact_label)
        float_layout.add_widget(contact_input)
        float_layout.add_widget(add_btn)
        float_layout.add_widget(back_btn)

        layout.add_widget(float_layout)
        return layout
def add_members(instance):
    name=member_name_input.text.strip()
    email=member_email_input.text.strip()
    contact=contact_input.text.strip()
    ref=db.reference('users')
    users_data=ref.get()
    if users_data:
        for user_id,user_info in users_data.items():
            if user_info.get("email",'').lower()==email.lower():
                show_popup('Error',f'This Email Aready Exists:{email}')
                return
            if user_info.get("name",'').lower()==name.lower():
                show_popup('Error',f'This Name Aready Exists:{name}')
                return
        new_user_id=random.randint(1,9999)
        new_user_password=random.randint(1,999999999999999999)
        ref=db.reference(f'users/{new_user_id}')
        ref.set({
            'name': name,
            'email': email,
            'contact': contact,
            'password': new_user_password
        })
        show_popup('Sucess',f'{name} Has Been Added succesfuly')
        name_input.text=''
        email_input.text=''
        contact_input.text=''
        
def send_group_member_email(email):
    
    sender_email='orangetree254@gmail.com'
    sender_password='ptwq denh qjub dvpo'
    subject='You have been added to the splitwise app.'
    ref=db.reference('user')
    users_data=ref.get()
    if users_data:
        for user_id,user_info in users_data.items():
            if user_info.get("email",'').lower()==email.lower():
                password=user_info.get('password')
                break
    if not password:
        show_popup('Error','Could not find the password in the data base')
        return
    body=f'You Have Been Invited To Use The Splitwise App With Your Friend, Here is your email and password, {email},{password}'
    message=MIMEMultipart()
    message['from']=sender_email
    message['to']=email
    message['subject']=subject
    message.attach(MIMEText(body,'plain'))
    try:
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender_email,sender_password)
        server.sendmail(sender_email,email,message.as_string())
        server.quit()
        show_popup('Success','Invitation Mail sent.')
    except:
        show_popup('Error','Invitation Mail was not able to be sent.')
        
def add_expense(instance):
    who=who_paid_spinner.text()
    description=description_input.text.strip()
    amount=amount_input.text.strip()
    if not who or not description or not amount:
        show_popup('Error', 'Fill in all fields')
        return
    amount=float(amount)
    split_amount=len(group_members)
    split_dict=dict.fromkeys(group_members,split_amount)
    ref=db.reference('transactions')
    ref.push({
        'transaction_id': random.randint(1000,9999),
        'description':description,
        'amount': amount,
        'who_paid':who
        'split': split_dict
    })
    
    show_popup('Sucess',f'Expense Has Been Added succesfuly')
    who_paid_spinner.text='Group Members'
    description_input.text=''
    amount_input.text=''

def fetch_group_members():
    global group_members
    group_members=[]
    ref=db.reference('users')
    users_data=ref.get()
    if users_data:
        for user_id,user_info in users_data.items():
            name=user_info.get('name')
            group_members.append(name)
        return group_members
            
    
    
            #---- Add Expense Screen ---
def build_add_expense_screen():
    global who_paid_spinner, description_input, amount_input
    layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

    layout.add_widget(Label(
        text='[b]ADD EXPENSE[/b]', markup=True, font_size=36,
        size_hint=(1, None), height=60, color="yellow"
    ))

    float_layout = FloatLayout(size_hint=(1, 1))

    # Who Paid
    who_paid_label = Label(text='Who Paid:', size_hint=(None, None), size=(120, 40),
                           pos_hint={'center_x': 0.18, 'center_y': 0.75}, color=TEXT_COLOR)
    
    # who_paid_input = TextInput(size_hint=(0.6, None), height=50,
    #                            pos_hint={'center_x': 0.6, 'center_y': 0.75},
    #                            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
    group=["member1", "member2", "member3"]  # Placeholder for group members
    who_paid_spinner= Spinner(
        text='Group Members',
        values=group,
        size_hint=(0.5, None), size=(180, 50),
        pos_hint={'x': 0.3, 'center_y': 0.75},
        background_color="white",
        color=TEXT_COLOR,
        font_size=16,
    )
    # Description
    description_label = Label(text='Description:', size_hint=(None, None), size=(120, 40),
                              pos_hint={'center_x': 0.18, 'center_y': 0.6}, color=TEXT_COLOR)
    description_input = TextInput(size_hint=(0.6, None), height=50,
                                  pos_hint={'center_x': 0.6, 'center_y': 0.6},
                                  background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    # Amount
    amount_label = Label(text='Amount:', size_hint=(None, None), size=(120, 40),
                         pos_hint={'center_x': 0.18, 'center_y': 0.45}, color=TEXT_COLOR)
    amount_input = TextInput(size_hint=(0.6, None), height=50,
                             pos_hint={'center_x': 0.6, 'center_y': 0.45},
                             background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    # Buttons
    add_btn = Button(text='Add', size_hint=(0.4, None), height=50,
                     pos_hint={'center_x': 0.5, 'center_y': 0.28},
                     background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR,
                     )

    back_btn = Button(
        text='Back to Dashboard',
        size_hint=(1, None), height=50,
        pos_hint={'center_x': 0.5, 'center_y': 0.14},
        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR,
        on_press=go_to_dashboard
    )

    # Call add_expense when the button is pressed, then go to dashboard
   
    # Add widgets
    float_layout.add_widget(who_paid_label)
    float_layout.add_widget(who_paid_spinner)
    float_layout.add_widget(description_label)
    float_layout.add_widget(description_input)
    float_layout.add_widget(amount_label)
    float_layout.add_widget(amount_input)
    float_layout.add_widget(add_btn)
    float_layout.add_widget(back_btn)

    layout.add_widget(float_layout)

    return layout

signup_screen=Screen(name='Signup')
signup_screen.add_widget(build_signup_screen())
login_screen=Screen(name='Login')
login_screen.add_widget(build_login_screen())
dashboard_screen=Screen(name='Dashboard')
dashboard_screen.add_widget(build_dashboard_screen())
group_screen=Screen(name='Group')
group_screen.add_widget(build_add_group_screen())
expense_screen=Screen(name='Expense')
expense_screen.add_widget(build_add_expense_screen())

sm.add_widget(signup_screen)
sm.add_widget(login_screen)
sm.add_widget(dashboard_screen)
sm.add_widget(group_screen)
sm.add_widget(expense_screen)
class MyApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyApp().run() 