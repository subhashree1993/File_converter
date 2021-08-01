from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
import json, os
from pathlib import Path
from .models import User, FileConvert
from datetime import datetime
import cloudconvert

API_KEY='eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiZDNiY2NkMzY4N2Y1Y2FhZDFjZDQ0N2VlNDc0MzNkY2IwNWY2NmVlZTlmMzFiN2Q3Nzc5OGFhYTI3NDhhYzI0NTBmMzE4YzdmMWI3MWEyYWQiLCJpYXQiOjE2Mjc4MzM2MjAuMjM4NTkzLCJuYmYiOjE2Mjc4MzM2MjAuMjM4NTk1LCJleHAiOjQ3ODM1MDcyMjAuMjAyNzk4LCJzdWIiOiI1MjU5Nzc0MiIsInNjb3BlcyI6WyJ1c2VyLnJlYWQiLCJ1c2VyLndyaXRlIiwidGFzay5yZWFkIiwidGFzay53cml0ZSIsIndlYmhvb2sucmVhZCIsIndlYmhvb2sud3JpdGUiLCJwcmVzZXQucmVhZCIsInByZXNldC53cml0ZSJdfQ.Vl52OeQHm_iUlP9V_HW5Yn3_pJjgmozuEd4iSGxl9-BKLoDfc-oJ5czwvGpGnTbHOxKIl5ucdj8oY2TN6rPJT-vbH5CiNyQF6PCQW0qMOE0amlgdKMBhKLuVUg4rHewEAKarPICDqigRx--8UfKdg6uHN4xkjgcE0ATtK0TLfJfYSrxqQ3xkPvmT9DLSYB1pXCdbijVZGCvwuswg2Ym6qrydIRxgjn8na1WYLAS72PvmJcpw4cXB0p_O2V637qV31Gb_fApn-P09opkT6qk5Kbrl-GmYJGH0XgZ5sMUkcJYNSbPMfp33Vp_ugAQtTc3DjX5Bjt8zG6GiLN0UDKxPcQGt3orQXIaUCnr-7WxkZWh0MuDC22gzmzSi1-Q4u-01U4lXn_R6jp-NLl9YvXL8S8ILns9twDmvQj_GjsU9ym94hWSFb7T3J8kH9XjwxtZ2PAH01xF_igHmmGLT4YDMYzq7o2lspwJy74xMlYM9n9x-Xj4DTfyZFjUn5F40sIO4NZDEru2Iu_NgZ6VEubFFi9sTdwb7pM2EY46quCr003H2ykby-ajHQ2QNHNgywdtEE_HVlXSf8RAg6CWRfXxiQd1yGuJ4QJsEvfYz3KEO_2t50p3bXSSgqgUc8d5bL8Hlqi_nlUgX_swwTxUDf0Ro02bn7rXpwwOrF0Cp5S-5L90'

cloudconvert.configure(api_key = API_KEY, sandbox = False) # sandbox=false : Production
# from docx2pdf import convert
# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_FILE_PATH = os.path.join(BASE_DIR, 'uploadedFiles')

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password=request.POST.get('password')
        if not User.objects.filter(email=email).exists():
            reg = User(name=name, email=email, password=password)
            reg.save()
            return render(request,"registrationSuccess.html")
        else: 
            return redirect('/login')
            # return render(request,"login.html", {"message" : 'User already exists. Please Login'})
            # response_data = {}
            # response_data['sts'] = False
            # response_data['message'] = 'User already exists. Please Login'
            # return HttpResponse(json.dumps(response_data), content_type="application/json")
            

    return render(request,"index.html")

def registrationSuccess(request):
    return render(request,"registrationSuccess.html")

def login(request):  # User already Existing
    if request.method == 'POST':
        return checkLogInSubmit(request)

    return render(request,"login.html", {"message" : 'User already exists. Please Login'})

def loginAfterRegistration(request):  # After User registered
    if request.method == 'POST':
        return checkLogInSubmit(request)

    return render(request,"login.html")

def checkLogInSubmit(request):
    userInfo = User.objects.get(email=request.POST['email'])
    if userInfo.password == request.POST['password']:
        request.session['user_id'] = userInfo.id
        request.session['email'] = request.POST['email']
        request.session.modified = True  # Confirm that the session is modified
        return HttpResponseRedirect('/upload')
    else:
        return render(request,"login.html", {"message" : 'Invalid Email or Password'})


def upload(request):
    global UPLOAD_FILE_PATH
    if request.method == 'POST':
        user_id = request.session.get('user_id', False) # if does not Exist return False
        user_email = request.session.get('email', False) # if does not Exist return False
        if not user_id or not user_email:
            return render(request,"login.html")
        else:
            convertFrom = request.POST['convertFrom']
            convertTo = request.POST['convertTo']
            myfile = request.FILES['file']
            fs = FileSystemStorage()

            fileStoredPath = os.path.join(UPLOAD_FILE_PATH, str(user_id), myfile.name)
            filename = fs.save(fileStoredPath, myfile) # Create File Path

            uploaded_file_url = fs.url(filename)

            reg = FileConvert(
                userId = user_id,
                fileName = myfile.name,
                originalFilePath = uploaded_file_url,
                # convertedFilePath,
                convertedFrom = convertFrom,
                convertedTo = convertTo,
                requestedTime = datetime.now(),
                conversionStatus = False
            )
            reg.save()

            # https://github.com/cloudconvert/cloudconvert-python
            job = cloudconvert.Job.create(payload={  # https://github.com/cloudconvert/cloudconvert-python/blob/master/tests/integration/testJobs.py#L55
                "tasks": {
                    'upload-my-file': { # Uploaded file
                        'operation': 'import/upload',
                        'file_name': fileStoredPath
                    },
                    'convert-my-file': { # Convert Uploaded file
                        'operation': 'convert',
                        'input': 'upload-my-file',
                        'output_format': convertTo,
                    },
                    'export-my-file': { # Get Download URL
                        'operation': 'export/url',
                        'input': 'convert-my-file'
                    }
                }
            })

            upload_task = None
            convert_task = None
            export_task = None
            for task in job["tasks"]:
                task_name = task.get("name")
                if task_name == "upload-my-file":
                    upload_task = task
                if task_name == "convert-my-file":
                    convert_task = task
                if task_name == "export-my-file":
                    export_task = task

            upload_task_id = upload_task.get("id")
            convert_task_id = convert_task.get("id")
            export_task_id = export_task.get("id")

            upload_task = cloudconvert.Task.find(id=upload_task_id)

            res_upload = cloudconvert.Task.upload(file_name=fileStoredPath, task=upload_task) # result = true/false
            # print("-----res_upload", res_upload)
            if res_upload:
                print("Uploaded file successfully..")
                convert_task = cloudconvert.Task.wait(id=convert_task_id) # Wait toill convertion not finished
                # print("-----convert_task", convert_task)
                if convert_task:
                    export_task = cloudconvert.Task.wait(id=export_task_id) # Get Download URL
                    # print("-----export_task", export_task)
                    # get exported url
                    exported_url = export_task.get("result").get("files")[0].get("url")
                    # print("-----exported_url", exported_url)

                    reg.convertedFilePath=exported_url
                    reg.conversionStatus=True
                    reg.save()


    return render(request,"upload.html")



def getLogs(request):
    global UPLOAD_FILE_PATH
    if request.method == 'GET':
        user_id = request.session.get('user_id', False) # if does not Exist return False
        user_email = request.session.get('email', False) # if does not Exist return False
        if not user_id or not user_email:
            return render(request,"login.html")
        else:
            all_entries = FileConvert.objects.all().filter(userId = user_id).order_by('requestedTime').reverse()
            return render(request, 'logs.html', {"data":all_entries})