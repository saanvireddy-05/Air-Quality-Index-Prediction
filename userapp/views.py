from django.shortcuts import render, redirect
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Create your views here.
from userapp.models import *
from django.contrib import messages
import random
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import default_storage
import urllib.request
import urllib.request
import urllib.parse
import os
from django.contrib.auth import logout





def generate_otp(length=4):
    otp = "".join(random.choices("0123456789", k=length))
    return otp


def index(request):
    return render(request, "farmer/index.html")



def awareness(request):
    return render(request, "farmer/awareness.html")


def about(request):
    return render(request, "farmer/about.html")



def userLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)
        request.session['Email_id'] = email
        try:
            user = User.objects.get(user_email = email, user_password = password)
            print(user)
            
            
            if user.user_password ==  password :
                if user.user_email == email:
                        messages.success(request,'login successfull')
                        request.session['user_id'] = user.user_id
                        print('login sucessfull')
                        user.No_Of_Times_Login += 1
                        user.save()
                        return redirect('userDashboard')
                   
                
                else:
                    messages.info(request,"Login credentials was incorrect...")
            else:
                 messages.error(request,'Login credentials was incorrect...')    
        except:
            print(';invalid credentials')
            print('exce ')
            return redirect('userLogin')
    return render(request, 'farmer/user-login.html')




# def userLogin(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         try:
#             user = User.objects.get(user_email=email)
#             if user.user_password == password:
#                 request.session["user_id"] = user.user_id
#                 resp = sendSMS(user.user_name, user.otp, user.user_phone)
#                 subject = "OTP Verification for  Query Response Update"
#                 otp = f"Your OTP for verification is: {user.otp}"
#                 message = f"Hello {user.user_name},\n\nYou are attempting to log in to your  query account. Your OTP for login verification is: {otp}\n\nIf you did not request this OTP, please ignore this email."
#                 from_email = settings.EMAIL_HOST_USER
#                 recipient_list = [user.user_email]
#                 send_mail(
#                     subject, message, from_email, recipient_list, fail_silently=False
#                 )
#                 messages.success(request, "Otp sent To mail and phone number !")
#                 return redirect("otp")
#             else:
#                 messages.error(request, "Incorrect Password")
#                 return redirect("userLogin")
#         except User.DoesNotExist:
#             messages.error(request, "Invalid Login Details")
#             return redirect("userLogin")
#     return render(request, "farmer/user-login.html")


def contact(request):
    return render(request, "farmer/contact.html")



def userRegister(req):
    if req.method == "POST":
        name = req.POST.get("name")
        email = req.POST.get("email")
        phone = req.POST.get("phone")
        password = req.POST.get("password")
        location = req.POST.get("address")
        profile = req.FILES.get("profile")
        otp = str(random.randint(1000, 9999)) 
        print(otp, 'generated otp')
        
        # email messages
        try:
            user_data = User.objects.get(user_email = email)
            messages.info(req, 'mail already registered')
            return redirect('userRegister')
        except:
            mail_message = f'Registration Successfully\n Your 4 digit Pin is below\n {otp}'
            print(mail_message)
            send_mail("Student Password", mail_message , settings.EMAIL_HOST_USER, [email])
            # text message
        
            User.objects.create(
                user_name=name,
                user_email=email,
                user_phone=phone,
                user_profile=profile,
                user_password=password,
                user_location=location,
                otp=otp,
            )
            req.session['Email_id'] = email
            messages.success(req, 'Your account was created..')

            return redirect('otp')
    return render(req, 'farmer/user-register.html')



# def userRegister(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         phone = request.POST.get("phone")
#         password = request.POST.get("password")
#         location = request.POST.get("address")
#         profile = request.FILES.get("profile")
#         try:
#             User.objects.get(user_email=email)
#             messages.info(request, "Email Already Exists!")
#             return redirect("otp")
#         except:
#             otp = generate_otp()
#             user = User.objects.create(
#                 user_name=name,
#                 user_email=email,
#                 user_phone=phone,
#                 user_profile=profile,
#                 user_password=password,
#                 user_location=location,
#                 otp=otp,
#             )
#             print(user)
#             subject = "Response is Updated For Your  Query"
#             # message = f'Hello {user.name},\n\nYour  query  response had been Updated from our expert.\n\n This is Updated Response: {response_text}'
#             # from_email = os.environ.get('EMAIL_HOST_USER')
#             # recipient_list = [user.email]
#             # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#             messages.success(request, "Account Created Successfully!")
#             return redirect("userRegister")
#     return render(request, "farmer/user-register.html")


def userDashboard(request):
    user_id = request.session["Email_id"]
    user = User.objects.get(user_email = user_id)
    prediction_count =  User.objects.all().count()

    return render(request, "farmer/user-dashboard.html", { 'la':prediction_count })
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def feedback(request):
    views_id = request.session['Email_id']
    user = User.objects.get(user_email=views_id)
    if request.method == 'POST':
        u_feedback = request.POST.get('review')
        u_rating = request.POST.get('rating')

        if not u_feedback:
            return redirect('')  # Specify the appropriate redirect target

        # Sentiment analysis
        sid = SentimentIntensityAnalyzer()
        score = sid.polarity_scores(u_feedback)
        sentiment = None
        if score['compound'] > 0 and score['compound'] <= 0.5:
            sentiment = 'positive'
        elif score['compound'] > 0.5:
            sentiment = 'very positive'
        elif score['compound'] < -0.5:
            sentiment = 'very negative'
        elif score['compound'] < 0 and score['compound'] >= -0.5:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        print(sentiment)
        user.star_feedback = u_feedback
        user.star_rating = u_rating
        user.save()

        UserFeedbackModels.objects.create(
            user_details=user,
            star_feedback=u_feedback,
            star_rating=u_rating,
            sentment=sentiment
        )
        
        # Send feedback to user's email
        mail_message = f"Thank you for your feedback!\n\nYour review: {u_feedback}\nYour rating: {u_rating}\nSentiment: {sentiment}"
        send_mail(
            "Thank you for your feedback",
            mail_message,
            settings.EMAIL_HOST_USER,
            [user.user_email]
        )

        rev = UserFeedbackModels.objects.filter()
        messages.success(request,'Feedback sent successfully')

    return render(request, "farmer/user-feedback.html")





def prediction(request):
   
        
    
    return render(request, 'farmer/prediction-copy.html')






import time

def userlogout(request):
    view_id = request.session["user_id"]
    user = User.objects.get(user_id = view_id) 
    t = time.localtime()
    user.Last_Login_Time = t
    current_time = time.strftime('%H:%M:%S', t)
    user.Last_Login_Time = current_time
    current_date = time.strftime('%Y-%m-%d')
    user.Last_Login_Date = current_date
    user.save()
    messages.info(request, 'You are logged out..')
    # print(user.Last_Login_Time)
    # print(user.Last_Login_Date)
    return redirect('user')


def otp(request):
    user_id = request.session["Email_id"]
    user = User.objects.get(user_email=user_id)
    if request.method == "POST":
        otp_entered = request.POST.get("otp")
        print(otp_entered, "otp enterd")
        print(user_id)
        if not otp_entered:
            messages.error(request, "Please enter the OTP")
            print("OTP not entered")
            return redirect("otp")
        try:
            user = User.objects.get(user_email=user_id)
            if str(user.otp) == otp_entered:
                user_id = request.session["Email_id"]
                messages.success(request, "OTP verification and Login are successful!")
                return redirect("userDashboard")
            else:
                messages.error(request, "Invalid OTP entered")
                print("Invalid OTP entered")
                return redirect("otp")
        except User.DoesNotExist:
            messages.error(request, "Invalid user")
            print("Invalid user")
            return redirect("userRegister")
    return render(request, "farmer/otp.html")


def chatbot(request):
    return render(request, "farmer/chatbot.html")


def myprofile(request):
    user_id = request.session.get("Email_id")
    user = User.objects.get(user_email=user_id)
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        try:
            profile = request.FILES["profile"]
            user.user_profile = profile
        except MultiValueDictKeyError:
            profile = user.user_profile
        password = request.POST.get("password")
        location = request.POST.get("location")
        user.user_name = name
        user.user_email = email
        user.user_phone = phone
        user.user_password = password
        user.user_location = location
        user.save()
        messages.success(request, "updated succesfully!")
        return redirect("myprofile")
    return render(request, "farmer/myprofile.html", {"i": user})





def result(request):
    

    return render(request, "farmer/result.html")


def user_logout(request):
    logout(request)
    return redirect("userLogin")
