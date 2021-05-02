from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import auth
import pyrebase
from classify_system.forms import RegistrationForm
from django.core.exceptions import PermissionDenied
import firebase_admin
from firebase_admin import credentials, firestore, storage
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files import File
import time
from datetime import datetime, timezone
import pytz

from fastai import *
from fastai.vision import *
from fastai.vision.models import *
from fastai.vision.image import Image as I

from PIL import Image
from urllib.request import urlopen

import torchvision.transforms as T

serviceAccount = {
  "type": "service_account",
  "project_id": "malocclusionfyp",
  "private_key_id": "a56b09b72364146893b27d2c72fcbab1e485568f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCPk2IRDZ/gxb7N\nkBO7JqNfU7lqWDn36kLR0BVa1A4q4atmuq893qAXB9FWnz6zzAVKDD8un0kp15eC\nLV3ZPC3O60wuIIYDtzw/n26NPjxv4RKpflCDCJ0XI2UsSTVGzt1pXJMQ0Kvs+SvS\nh6plUiJSTt33ZBuVs49x+fRYyhdeYLz1kD6LOhFOWpca7XNo2wW/serOTUX9AdxR\nT8B0F3nD2cALSgWHFGFgbQeDKcugnpxqCfxN8I6sIY7EzBXljBWXwZ+ZcV8lmJp1\nHObljd4zhOzYnu2OoB2cuvzDG5tvompS6dFmKPiEFnZleZQ77S29XkbZ4TDvQrTv\nB76nhg2tAgMBAAECggEAMct6bBKvG+xJUA8DoNl2OOYXPOhLdo2zTgRem6lHHp00\n7oSZqZoQKNynwGSrgP0l6ngT464P2Giy3c2xKloCQyz9N1RFVn2S8jfvxiHLITxM\n1ib+cmum2/MFMFZVmXC+fr/CK8dLkX0bs0ElGk3hpG1A83+vR3zGp896bN7uOudK\nNPSKEpm3OQ+UNwpMXkTzySzLm7MwPJoMm7ejtWIDhdK0LWUh2q6c2AKixWTGt3NU\nO/2Kys6GTbypMbcR603dwVxKARzFETBaTPws3JwkYMjCMaXMEDme6RvYnyiWkr7v\n9jXSIo/GjJqzksF6xRBw3q81pk8hZvjftTv3q5xsWwKBgQDBIH9HQ8C0nHTqZMWN\ndxr/0mzkn5fZ6gIPUPN6qIT4PszF6GqX4VRZ5c2nFGLF73SgjJeDyz5Af1BMbnPV\n+J9xf+YHDc7htbRuL0YWcf4PTstUUlxIZWfxTjY1MQ39jWX6H0SKy5NiqQJvXPCO\ntKr8ABiDNpoootKM03Icf0quRwKBgQC+UTVyNk5hFZZY0vure8dmVIV0u8R5ygYQ\n8/2xfDHMUve5WGVtAe/yaQ18N8wMxKpJ5uv4wGcAGnWUdktqBC9G+YJpg0CF9qtu\nOuuF18A0eW7fUvasrzNlZU/XY6LtJIHA4b/56oYTOuT92sSS6TcZ4KMaCQdpXG8X\nHdAFd4QaawKBgCRdLhoJE9vuKcWIu/nrF1ZcFMznj/wkJ8cigvXxjTgA+yW4oXl/\noBZdQt/W4tJKSDeCwXS7bDlQv5nkokMD0WHZp0JkwzOUtyiYFiZbyG6xc2+pIl8v\nWOcCxwo09mFromv6PzmzI0lMcXzujw0Pz7IrgnIScex83BBQMAhVn4Y5AoGAdWqC\nz9kDWFBKNrjMPksahV6mC5QArqbeQT1XClY2HvodDcOkp7EnSWZYxIdkI4h+CyQl\n9400vtKUMikdc+XrCR3MwK4Sc9Pwhgxh3Gx0j6tPpQZ5W6anzenIbXlyPl5kkwx0\nNYrkdx7BwoBjAMRTk2qNFfX2FaHKg/eHrKfE38sCgYATX3OBPGUix50YIyuMmZcV\n1VNRqoB70mzZUYWWyFQAiuWQa+G7HDq5/Dc4k0xKm5cEPODUhK+PRS8x0ZMgoXpD\nW2/+BgvgAg6xKOa/apo+c55mBMQk5hRifkY2Cdqy/d1DuSFYBTmDzL5OMkLC+UDC\ns2/aczEj8VhLIoDdmMcC5A==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-cp60i@malocclusionfyp.iam.gserviceaccount.com",
  "client_id": "114337027340257357588",
  "auth_uri": "https://.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-cp60i%40malocclusionfyp.iam.gserviceaccount.com"
}

config = {
    'apiKey': "AIzaSyDdGbKmYXtT37bG_OLTeiLNCwWm3uECadk",
    'authDomain': "malocclusionfyp.firebaseapp.com",
    "databaseURL": "https://malocclusionfyp-default-rtdb.firebaseio.com",
    'projectId': "malocclusionfyp",
    'storageBucket': "malocclusionfyp.appspot.com",
    'messagingSenderId': "329082234324",
    'appId': "1:329082234324:web:9cb84f3476952ffb276241",
    'measurementId': "G-Q7XCMFQ4CG",
    'serviceAccount': serviceAccount
}

cred = credentials.Certificate(serviceAccount)
firebase_admin.initialize_app(cred, {'storageBucket': "malocclusionfyp.appspot.com"})
bucket = storage.bucket()

firebase = pyrebase.initialize_app(config)

authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()

patient_path = "patient/"

def retrieveCurrU(request):
    idtoken = request.session['uid']
    curr_user = authe.get_account_info(idtoken)
    curr_user = curr_user['users']
    curr_user = curr_user[0]
    curr_user = curr_user['localId']
    
    return(curr_user)

def list_all_patient(request):
    patient = database.child('patient').shallow().get().val()
    p_list = []
    for p in patient:
        p_data = {
            "pid": p,
            "name": database.child('patient').child(p).child('pname').get().val(),
            "age": database.child('patient').child(p).child('age').get().val(),
            "gender": database.child('patient').child(p).child('gender').get().val(),
            "classes": database.child('patient').child(p).child('classes').get().val(),
            "pic": database.child('patient').child(p).child('pic').get().val(),
        }
        p_list.append(p_data)

    return(sorted(p_list, key=lambda x: x['name'], reverse=False))

def registerS(request):
    return render(request, "registerStudent.html")

def registerD(request):
    return render(request, "registerDoctor.html")

def postRegisterD(request):
    name = request.POST.get('name')
    userid = request.POST.get('userid')
    level = request.POST.get('level')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authe.create_user_with_email_and_password(email, password)

    uid = user['localId']

    data = {
        "post": "Doctor", 
        "name": name.upper(), 
        "userid": userid, 
        "status": "1", 
        "level": level
    }
    database.child("user").child(uid).child("details").set(data)
    return render(request, "registration/login.html")

def postRegisterS(request):
    name = request.POST.get('name')
    userid = request.POST.get('userid')
    level = request.POST.get('level')
    email = request.POST.get('email')
    password = request.POST.get('password')

    user = authe.create_user_with_email_and_password(email, password)
    uid = user['localId']

    data = {
        "post": "Student", 
        "name": name.upper(), 
        "userid": userid, 
        "status": "1", 
        "level": level
    }
    database.child("user").child(uid).child("details").set(data)
    return render(request, "registration/login.html")

def aboutPage(request):
    curr_u = retrieveCurrU(request)
    u_name = database.child('user').child(curr_u).child('details').child('name').get().val()
    return render(request, "about.html", {"name": u_name, "about": "active",})

def login(request):
    return render(request, "registration/login.html")

def logout(request):
    auth.logout(request)
    return render(request, "registration/login.html")

def post_login(request):
    email = request.POST.get('email')
    password = request.POST.get("password")

    try:
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        message = "Invalid Credentials"
        return render(request, "login.html", {"message": message})

    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return HttpResponseRedirect('/home/')

def dashboard(request):
    curr_u = retrieveCurrU(request)
    u_name = database.child('user').child(curr_u).child('details').child('name').get().val()
    all_patient = list_all_patient(request)
    total_p = len(all_patient)
    #Content
    #Graph 1: New added patient per month

    #Graph 2: Male and Female patient
    male = []
    female = []
    for p in all_patient:
        if p["gender"] == "Male":
            male.append(p)
        elif p["gender"] == "Female":
            female.append(p)
    male_no = len(male)
    female_no = len(female)
    male_per = round((male_no/(male_no+female_no))*100)
    female_per = round((female_no/(male_no+female_no))*100)

    #Graph 3: Number of all 3 classes
    class1 = []
    class2 = []
    class3 = []
    for p in all_patient:
        if p["classes"] == 1:
            class1.append(p)
        elif p["classes"] == 2:
            class2.append(p)
        else:
            class3.append(p)
    class1_no = len(class1)
    class2_no = len(class2)
    class3_no = len(class3)
    class1_per = round((class1_no/(class1_no+class2_no+class3_no))*100)
    class2_per = round((class2_no/(class1_no+class2_no+class3_no))*100)
    class3_per = round((class3_no/(class1_no+class2_no+class3_no))*100)

    #All data to display
    data = {
        "name": u_name,
        "home": "active",
        "male_no": male_no,
        "total": total_p,
        "female_no": female_no,
        "male_per": male_per,
        "female_per": female_per,
        "class1_no": class1_no,
        "class2_no": class2_no,
        "class3_no": class3_no,
        "class1_per": class1_per,
        "class2_per": class2_per,
        "class3_per": class3_per
    }

    return render(request, "dashboard.html", data)

def viewProfile(request):
    curr_u = retrieveCurrU(request)
    position = database.child('user').child(curr_u).child('details').child('post').get().val()
    detail = database.child('user').child(curr_u).child('details').get().val()

    #Retrieve patient under the account
    patient = database.child('patient').shallow().get().val()
    p_list = []
    for p in patient:
        p_data = {
            "pid": p,
            "name": database.child('patient').child(p).child('pname').get().val(),
            "age": database.child('patient').child(p).child('age').get().val(),
            "gender": database.child('patient').child(p).child('gender').get().val(),
            "pic": database.child('patient').child(p).child('pic').get().val(),
        }
        if p_data["pic"] == detail["userid"]:
            p_list.append(p_data)

    data = {
        "account": "active",
        "name": detail["name"],
        "level": detail["level"],
        "userid": detail["userid"],
        "patient": sorted(p_list, key=lambda x: x['name'], reverse=False)
    }
    if position == "Doctor":
        return render(request, "profileD.html", data)
    elif position == "Student":
        return render(request, "profileS.html", data)

def updateProfile(request):
    curr_u = retrieveCurrU(request)
    
    #Update content
    name = request.POST.get('name')
    userid = request.POST.get('userid')
    level = request.POST.get('level')

    data = {
        "name": name.upper(), 
        "userid": userid,
        "level": level
    }

    database.child("user").child(curr_u).child("details").update(data)
    return redirect('/profile/')

def listPatient(request, pid=None):
    curr_u = retrieveCurrU(request)
    u_name = database.child('user').child(curr_u).child('details').child('name').get().val()

    p_list = list_all_patient(request)
    data = {
        "patient": p_list,
        "name": u_name,
        "patientt": "active",
    }
    return render(request, "patient.html", data)

def viewPatient(request, pid):
    curr_u = retrieveCurrU(request)
    u_name = database.child('user').child(curr_u).child('details').child('name').get().val()
    idtoken = request.session['uid']

    patient = database.child('patient').child(pid).get().val()
    screening = database.child('patient').child(pid).child('screening').get().val()

    screen_list = []
    if screening is not None:
        for p in screening:
            temp_class = database.child('patient').child(pid).child('screening').child(p).get().val()
            
            # Convert classes
            if temp_class['classes'] == 4:
                str_class = "No prediction yet"
            elif temp_class['classes'] == 1:
                str_class = "Predicted as Class I"
            elif temp_class['classes'] == 2:
                str_class = "Predicted as Class II"
            else:
                str_class = "Predicted as Class III"

            # Convert date
            pf = float(p)
            date = datetime.fromtimestamp(pf).strftime('%H:%M %d-%m-%Y')
            p_data = {
                "date": date,
                "datetime": p,
                "classes": str_class,
                "class1": temp_class['class1'],
                "class2": temp_class['class2'],
                "class3": temp_class['class3'],
                "xray_url": storage.child(patient_path+pid+"/"+p+".jpg").get_url(idtoken)
            }
            screen_list.append(p_data)
    
    data = {
        "name": u_name,
        "pname": patient["pname"],
        "pid": pid,
        "age": patient["age"],
        "gender": patient["gender"],
        "pic": patient["pic"],
        "screening": screen_list
    }
    return render(request, "profileP.html", data)

def addPatient(request):
    curr_u = retrieveCurrU(request)
    u_name = database.child('user').child(curr_u).child('details').child('name').get().val()
    return render(request, "addPatient.html", {"name": u_name})

def post_addPatient(request):
    curr_u = retrieveCurrU(request)
    pic = database.child('user').child(curr_u).child('details').child('userid').get().val()

    # Add patient
    pname = request.POST.get('pname')
    pid = request.POST.get('pid')
    age = request.POST.get('age')
    gender = request.POST.get('gender')

    data = {
        "pname": pname.upper(),
        "age": age,
        "gender": gender,
        "pic": pic
    }

    database.child("patient").child(pid).set(data)

    return redirect('/patient_list/')

def addScreening(request):
    pid = request.POST.get('pid')
    # Set date
    tz = pytz.timezone('Asia/Kuala_Lumpur')
    curr_time = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(curr_time.timetuple()))

    classes = 4
    class1 = 0.0
    class2 = 0.0
    class3 = 0.0
    data = {
        "classes": classes,
        "class1": class1,
        "class2": class2,
        "class3": class3,
    }

    # Save to db
    database.child("patient").child(pid).child("screening").child(millis).set(data)

    # Upload screening
    xray = request.FILES.get('xray')
    filename = patient_path+pid+"/"+str(millis)+".jpg"
    blob = bucket.blob(filename, chunk_size=262144)
    blob.upload_from_file(xray)

    return redirect('/patient_list/patient_profile/'+pid)

def updatePatient(request):
    curr_u = retrieveCurrU(request)
    pic = database.child('user').child(curr_u).child('details').child('userid').get().val()

    # Update patient
    pname = request.POST.get('pname')
    pid = request.POST.get('pid')
    age = request.POST.get('age')
    gender = request.POST.get('gender')

    data = {
        "pname": pname.upper(),
        "age": age,
        "gender": gender,
        "pic": pic
    }

    database.child("patient").child(pid).update(data)

    return redirect('/patient_list/patient_profile/'+pid)

def delete(request, pid):
    curr_u = retrieveCurrU(request)
    u_name = database.child('user').child(curr_u).child('details').child('name').get().val()

    database.child('patient').child(pid).remove()
    storage.delete(patient_path+pid+".jpg")

    message = "Patient Deleted"

    #Retrieve all patient
    p_list = list_all_patient(request)

    data = {
        "patient": p_list,
        "name": u_name,
        "message": message
    }
    return render(request, "patient.html", data)

def search(request):
    curr_u = retrieveCurrU(request)
    u_name = database.child('user').child(curr_u).child('details').child('name').get().val()
    p_list = list_all_patient(request)

    display_list = []
    search = request.POST.get("search")
    for p in p_list:
        if search in p["name"] or p["pid"] == search:
            display_list.append(p)
    
    display_list = sorted(display_list, key=lambda x: x['name'], reverse=False)
    data = {
        "name": u_name,
        "patient": display_list,
        "clear": "True"
    }

    return render(request, "patient.html", data)

def showStatistical(request):
    curr_u = retrieveCurrU(request)
    u_name = database.child('user').child(curr_u).child('details').child('name').get().val()

    data = {
        "name": u_name
    }
    return render(request, "statistical.html", data)

def classifier_home(request):
    curr_u = retrieveCurrU(request)
    u_name = database.child('user').child(curr_u).child('details').child('name').get().val()

    data = {
        "name": u_name
    }
    return render(request, "classifier.html", data)

def classifier(request, pid=None, dt=None):
    idtoken = request.session['uid']

    # Open patient image
    xray_url = storage.child(patient_path+pid+"/"+dt+".jpg").get_url(idtoken)

    img = Image.open(urlopen(xray_url))
    img_tensor = T.ToTensor()(img)
    img_fastai = I(img_tensor)

    # Prediction
    classifier = load_learner('./')
    if classifier:
        pred_class, pred_idx, output = classifier.predict(img_fastai)
    else:
        print("no model")

    class1 = round(output.numpy()[0], 4)
    class2 = round(output.numpy()[1], 4)
    class3 = round(output.numpy()[2], 4)

    classes = 4
    if class1 > class2:
        if class1 > class3:
            classes = 1
        else:
            if class2 > class1:
                if class2 > class3:
                    classes = 2
    else:
        classes = 3

    updated = {
        "classes": classes,
        "class1": str(class1),
        "class2": str(class2),
        "class3": str(class3)
    }
    
    database.child("patient").child(pid).child("screening").child(dt).update(updated)
    print("before redirect")
    return redirect('/patient_list/patient_profile/'+pid)
