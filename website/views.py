import csv
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages, auth
from django.http import HttpResponse,HttpResponseRedirect
from .models import AdminStudent, Jobs, CompanyProfile
from .models import Students,StudentProfile,CompanyApprove,JobApplication,internship,classdetails,videolibrary,ccontent, LikedContent, Alumni
from .models import resumeadmin, LikedContent1, ResumeBuilder, Review, Event, ExcelData, AddAptitude, AptitudeTest,Question, Option, ExamSchedule
from .models import *
from django.shortcuts import render, get_object_or_404, redirect

def index(request):
    return render(request, 'index.html')
def jobs(request):
    return render(request, 'jobs.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def cjob(request):
    return render(request, 'cjob.html')
def blog(request):
    return render(request, 'blog.html')
def postjob(request):
    return render(request, 'postjob.html')

def admin_index2(request):
    stu=StudentProfile.objects.filter(is_alumni = False)
    stu_count=stu.count()
    comp=CompanyProfile.objects.filter(is_approved = 'approved')
    comp_count=comp.count()
    com=CompanyProfile.objects.filter(is_approved = 'approved')
    com_count=comp.count()
    job=Jobs.objects.filter(is_active = True)
    job_count=job.count() 
    context={
        'stu':stu,
        'stu_count':stu_count,
        'comp':comp,
        'comp_count':comp_count,
        'com':com,
        'com_count':com_count,
        'job':job,
        'job_count':job_count,
        }
    return render(request, 'admin/index-2.html',context)
def admin_profile(request):
    return render(request, 'admin/profile.html')
def admin_editprofile(request):
    return render(request, 'admin/edit-profile.html')

def admin_company(request):
    return render(request, 'admin/company.html')

def admin_studentadd(request):
    return render(request,'admin/student_add.html')
def ad_cprofile(request):
    return render(request, 'admin/ad_cprofile.html')

def srequest(request):
    admin_student = request.user.student_profile
    return render(request, 'student/srequest.html',{'admin_student':admin_student})

def loginn(request):
    if request.method == "POST":
        username=request.POST['email']
        # email = request.POST['email']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)     
            if Alumni.objects.filter(user=user):
                return redirect('alumni_index')
            else:
                if user.is_superuser:
                    return redirect('admin_index2')
                elif user.is_staff:
                    return redirect('sindex')
                else:
                    return redirect('cindex')
        else:
            messages.info(request, "Invalid Login")
            return redirect('loginn')
    else:
        return render(request, 'login.html') 

def reg(request):
    if request.method == "POST":
        companyname = request.POST['companyname']
        username = request.POST['email']
        email = request.POST['email']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
       
        
        
        if password == confirmPassword:
            # if User.objects.filter(companyname=companyname).exists():
            #     return render(request, 'registration.html', {'companyname_exists': True})
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Email already exists') 
                return redirect('reg')
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                # company_approve = CompanyApprove(companyname=companyname, email=email, user=user)
                
                company = CompanyProfile(user=user, companyname=companyname) 

                
                user.save()
                # company_approve.save()
                company.save()

                messages.success(request, 'Registration successful! You can Login now..')
                return redirect('loginn')
        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('reg')
    else:
        return render(request, 'registration.html')
    


def loggout(request):
    print('Logged Out')
    auth.logout(request)
    return redirect('/')

def sample2(request):
    return render(request, 'sample2.html')


from django.shortcuts import get_object_or_404

def cindex(request):
    if request.user.is_authenticated:
        try:
            # Try to retrieve the company profile
            companyprofile = request.user.companyprofile
        except CompanyApprove.DoesNotExist:
            # If the user doesn't have a companyprofile, redirect to the profile creation page
            return redirect('loginn')

        return render(request, 'cindex.html', {'companyprofile': companyprofile})
    else:
        return redirect('loginn')


def aboutuser(request):
    return render(request, 'aboutuser.html') 
def contactuser(request):
    return render(request, 'contactuser.html')



def studentloginn(request):
    if request.method == "POST":
        username=request.POST['email']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, "Invalid Login")
            return redirect('studentloginn')
    else:
        return render(request, 'studentlogin.html') 

from django.core.files.images import get_image_dimensions
from django.http import HttpResponseBadRequest

def addjob(request):
        
        # obj=CompanyProfile.objects.get(id=obj_id)
        # cmp = get_object_or_404(CompanyProfile, user=request.user)
        # print(cmp)
    # except CompanyProfile.DoesNotExist:
            

            user = request.user
            

            if request.method == 'POST':
                cname = request.POST.get('cname')
                jname = request.POST.get('jname') 
                salary = request.POST.get('salary')
                email = request.POST.get('email')
                sdate = request.POST.get('sdate')
                edate = request.POST.get('edate')
                link = request.POST.get('link')
                job_descriptions = request.POST.get('job_descriptions')
                qualifications = request.POST.get('qualifications')
                preferred_skills = request.POST.get('preferred_skills')
                responsibilities = request.POST.get('responsibilities')
                required_current_cgpa = request.POST.get('required_current_cgpa')
                required_tenth_cgpa = request.POST.get('required_tenth_cgpa')
                required_twelfth_cgpa = request.POST.get('required_twelfth_cgpa')
                required_backlog = request.POST.get('required_backlog')
                # criteria=request.FILES['criteria'] if 'criteria' in request.FILES else None

                # if criteria and not criteria.name.endswith('.pdf'):
                #     messages.error(request, 'Please upload a PDF file for the criteria.')
                #     return redirect('postjob')


                obj = Jobs()
                obj.user = request.user
                obj.cname = cname
                obj.jname = jname
                obj.salary = salary
                obj.email = email
                obj.sdate = sdate
                obj.edate = edate
                obj.link = link
                obj.job_descriptions = job_descriptions
                obj.qualifications = qualifications
                obj.preferred_skills = preferred_skills
                obj.responsibilities = responsibilities
                obj.required_current_cgpa = required_current_cgpa
                obj.required_tenth_cgpa = required_tenth_cgpa
                obj.required_twelfth_cgpa = required_twelfth_cgpa
                obj.required_backlog = required_backlog
                
                # obj.criteria=criteria
                
                obj.save()
                messages.success(request, 'Job added successfully!')
                
            # Redirect to the doctors page
                return redirect('postjob')  # Redirect to the doctors page URL name
            
            return render(request, 'addjob.html',{'user':user})

def postjob(request):
    user = request.user
    job = Jobs.objects.filter(user=user)
    print(job)
    return render(request, 'postjob.html', {'job': job})
from django.shortcuts import render
from .models import Jobs



# bccgfcg





# edit_job

from django.shortcuts import render, get_object_or_404, redirect
from .models import Jobs

def edit_job(request, job_id):
    job = get_object_or_404(Jobs, pk=job_id)
    criteriafile = request.FILES.get('criteria')
    if request.method == 'POST':
        job.cname = request.POST.get('cname')
        job.jname = request.POST.get('jname')
        job.salary = request.POST.get('salary')
        job.email = request.POST.get('email')
        job.sdate = request.POST.get('sdate')
        job.edate = request.POST.get('edate')
        job.link = request.POST.get('link')
        job.job_descriptions = request.POST.get('job_descriptions')
        job.responsibilities = request.POST.get('responsibilities')
        job.preferred_skills = request.POST.get('preferred_skills')
        job.qualifications = request.POST.get('qualifications')
       
        job.save()
        # Redirect to a success page or back to the job listing page
        return redirect('postjob')  # Change 'job_listing' to the appropriate URL name
        
    return render(request, 'editjob.html', {'job': job})

# deletejob
from django.shortcuts import render, redirect
from .models import Jobs

from django.shortcuts import render, get_object_or_404, redirect
from .models import Jobs

def delete_job(request, job_id):
    # Get the job object by id
    job = get_object_or_404(Jobs, id=job_id)
    
    if request.method == 'POST':
        # Set the is_active field to False
        job.is_active = False
        job.save()  # Save the updated job object with is_active=False
        return redirect('postjob')  # Redirect to a suitable page after deletion

    return render(request, 'delete_job.html', {'job': job})

def CRegistration(request):
    return render(request, 'registration.html')


def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_index')  # Redirect to admin dashboard
        else:
            # Invalid credentials, handle error or show message
            pass
    
    return render(request, 'admin/admin_login.html')



#jobs_table_view 
from django.shortcuts import render
from .models import Jobs  # Import your Jobs model here


def jobslist(request):
    job_list = Jobs.objects.filter(is_active=True)
    context = {'job_list': job_list}
    return render(request, 'admin/admin_jobtable.html', context)



from django.shortcuts import render
from .models import CompanyProfile

def companyprofilelist(request):
    company_profiles = CompanyProfile.objects.filter(is_approved='approved')
    return render(request, 'admin/companyprofilelist.html', {'company_profiles': company_profiles})


def addstudents(request):
    if request.method == 'POST':
        sname = request.POST.get('sname')
        email = request.POST.get('email')
        # passw = request.POST.get('passw')
        # password=request.POST.get('password')
        course = request.POST.get('course')
        department = request.POST.get('department')
        semester = request.POST.get('semester')

        obj = Students()
        obj.sname = sname
        obj.email = email
        # obj.passw = passw
        # obj.password = password
        obj.course = course
        obj.department = department
        obj.semester = semester
        
        
        obj.save()
        messages.success(request, 'Student added successfully!')

       # Redirect to the doctors page
        return redirect('admin_poststudent')  # Redirect to the doctors page URL name
    
    return render(request, 'admin/student_add.html')




def profc(request):
    return render(request,'admin/profc.html')
def admin_poststudent(request):
    stus=Students.objects.all()
    return render(request,'admin/admin_poststudent.html',{'stus': stus})

def search_company(request):
    if 'companyname' in request.GET:
        companyname = request.GET['companyname']
        # Perform the company name search, for example:
        company_profiles = CompanyProfile.objects.filter(companyname__icontains=companyname)
    else:
        company_profiles = CompanyProfile.objects.all()  # Display all company profiles if no search query

    return render(request, 'admin/companyprofilelist.html', {'company_profiles': company_profiles})
def search_student(request):
    studentname = request.GET.get('studentname', '')
    
    # Filter students based on the search query
    students = Students.objects.filter(sname__icontains=studentname)
    
    return render(request, 'admin/admin_poststudent.html', {'stus': students})
def search_student2(request):
    admission_no = request.GET.get('admission_no', '')
    
    # Filter students based on the search query
    adstudents = StudentProfile.objects.filter(admission_no__icontains=admission_no)
    
    return render(request, 'admin/ad_studentlist.html', {'adstus': adstudents})
def search_course(request):
    semail= request.GET.get('semail', '')
    
    # Filter students based on the search query
    students = Students.objects.filter(email__icontains=semail)
    
    return render(request, 'admin/admin_poststudent.html', {'stus': students})

from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import render
from .models import CompanyProfile

from django.shortcuts import render
from .models import CompanyProfile

def adsearch_company(request):
    companysname = request.GET.get('companysname', '')

    print("Search query:", companysname)

    # Search for the company
    job_list = CompanyProfile.objects.filter(companyname__icontains=companysname)

    print("Company list:", job_list)

    return render(request, 'admin/admin_jobtable.html', {'job_list': job_list})






def search_job(request):
    jobsname = request.GET.get('jobsname', '')
    print("Search query:", jobsname)  # Print the search query to console

    job_list = Jobs.objects.filter(jname__icontains=jobsname)
    print("Job list:", job_list)  # Print the job list to console

    return render(request, 'admin/admin_jobtable.html', {'job_list': job_list})





def edit_student(request):
    return render(request, 'edit_student.html')


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Students

def edit_student(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    
    if request.method == 'POST':
        # Update student data based on form input
        student.sname = request.POST.get('sname')
        student.email = request.POST.get('email')
        student.password = request.POST.get('password')
        student.course = request.POST.get('course')
        student.department = request.POST.get('department')
        student.semester = request.POST.get('semester')
        student.save()
        return redirect('admin_poststudent')
    return render(request, 'admin/edit_student.html', {'student': student})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Students

def delete_student(request, student_id):
    student = get_object_or_404(Students, id=student_id)

    # Mark the student as inactive
    student.is_active = False
    student.save()

    # Redirect to admin_poststudent view
    return redirect('admin_poststudent')
def delete_company(request):
    return render(request, 'admin/ad_deletecompany.html')


def ad_deletecompany(request, comp_id):
    company_profile = get_object_or_404(CompanyProfile, id=comp_id)

    if request.method == 'POST':
        company_profile.is_active= False
        company_profile.save()
        return redirect('companyprofilelist')  # Redirect to a relevant URL after deletion

    return render(request, 'admin/ad_deletecompany.html', {'company_profile': company_profile})


import os
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.conf import settings
from django.views import View
from django.utils.text import slugify
from .models import Jobs

class download_criteria(View):
    def get(self, request, job_id):
        # Get the job and retrieve the criteria file path
        job = get_object_or_404(Jobs, pk=job_id)
        criteria_path = job.criteria.path

        if os.path.exists(criteria_path):
            with open(criteria_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{slugify(os.path.basename(criteria_path))}"'
                return response
        else:
            raise Http404("File not found")



from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from pathlib import Path
from django.conf import settings
from website.models import Students  # Replace `your_app` with the actual app name

# def generate_pdf(request):
#     # Your existing code for template path, context, and response
#     template_path = 'admin/admin_poststudent.html'
#     students = Students.objects.values(id,email,course,department,semester,sname)  # Retrieve students data

#     # context = {'students': students}

#     # Construct the PDF file path
#     pdf_file_path = str(Path(settings.MEDIA_ROOT) / 'temp_students_list.pdf')

#     # Rest of your existing code for PDF generation
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{pdf_file_path}"'

#     template = get_template(template_path)
#     html = template.render(context)
#     pisa_status = pisa.CreatePDF(html, dest=response)

#     if pisa_status.err:
#         return HttpResponse('We had some errors <pre>' + html.escape(str(pisa_status.err)) + '</pre>')

#     return response
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models import Students  # Import your model

def generate_pdf(request):
    # Fetch department data from your model
    stu = Students.objects.values ('email','course','department','semester','sname')

    # Load the HTML template
    template = get_template('admin/admin_poststudent.html')

    # Render the template with department data
    html_content = template.render({'stu': stu})

    # Create a PDF file-like object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students_list.pdf"'

    # Generate PDF
    pdf = pisa.CreatePDF(BytesIO(html_content.encode('UTF-8')), response)

    if not pdf.err:
        return response

    return HttpResponse('Error generating PDF: %s' % pdf.err)


from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Students  # Assuming your student model is named 'Students'

def stureg(request):
    if request.method == "POST":
        studentname = request.POST.get('studentname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        course = request.POST.get('course')
        phoneNumber = request.POST.get('phoneNumber')

        # Check if passwords match
        if password == confirmPassword:
            # Check if the email already exists
            if Students.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
                return redirect('stureg')
            else:
                # Create the student object
                student = Students(studentname=studentname, email=email, password=password, course=course, phoneNumber=phoneNumber)
                student.save()

                messages.success(request, 'Registration successful! You can log in now.')
                return redirect('loginn')
        else:
            messages.error(request, 'Password confirmation does not match')
            return redirect('stureg')
    else:
        return render(request, 'sregistration.html')

def sloginn(request):
    if request.method == "POST":
        username=request.POST['email']
        # email = request.POST['email']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_index2')
            elif user.is_staff:
                return redirect('sindex')
            else:
                return redirect('cindex')
        else:
            messages.info(request, "Invalid Login")
            return redirect('loginn')
    else:
        return render(request, 'login.html') 
from django.shortcuts import render
from website.models import Student

def student_list(request):
    students = Student.objects.all()
    return render(request, 'admin/student/student_list.html', {'students': students})

from django.http import JsonResponse
from .models import Student

def get_student_data(request):
    students = Student.objects.all()
    student_data = [{'id':student.id,'username': student.username, 'password': student.password} for student in students]
    return JsonResponse(student_data, safe=False)

from django.shortcuts import render
from website.models import CompanyProfile

from django.shortcuts import render
from website.models import CompanyProfile

def companyapprove(request):
    # Retrieve a list of company profiles
    company_profiles = CompanyProfile.objects.all()

    context = {
        'company_profiles': company_profiles
    }

    return render(request, 'admin/companyapprove.html', context)


def approve_comp(request, company_id):
    certification = get_object_or_404(CompanyProfile, id=company_id)
    if request.method == 'POST':
        certification.is_approved = CompanyProfile.APPROVED  # Set it to 'approved'
        certification.save()
    return redirect('companyapprove')

def admin_addstudents(request):
    return render(request, 'admin/student/student.html')




from django.shortcuts import render
from .models import StudentProfile,AdminStudent

def ad_studentlist(request):

    adstus = StudentProfile.objects.filter(is_alumni=False)
    # Handling passout year filter
    passout_year_filter = request.GET.get('passout_year')
    if passout_year_filter:
        adstus = adstus.filter(passout_year=passout_year_filter)

    # Handling department filter
    selected_departments = request.GET.getlist('department')
    if selected_departments:
        adstus = adstus.filter(department__in=selected_departments)

    # Handling course filter
    selected_courses = request.GET.getlist('course')
    if selected_courses:
        adstus = adstus.filter(course__in=selected_courses)

    # Generate a list of academic years from 2020 to 2030
    available_years = range(2020, 2031)

    admstu = AdminStudent.objects.filter(alumni=False)
    
    return render(request, 'admin/student/ad_studentlist.html', {'adstus': adstus, 'available_years': available_years, 'admstu':admstu})



import csv
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminStudent
from django.core.mail import send_mail
from django.conf import settings
# def add_student(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name', '')
#         last_name = request.POST.get('last_name', '')
#         admission_no = request.POST.get('admission_no', '')
#         email = request.POST.get('email', '')
#         phone = request.POST.get('phone', '')

#         # Path to your CSV file for validation
#         csv_file_path = 'dataset/student.csv'
#         match_found = False

#         with open(csv_file_path, 'r') as csv_file:
#             csv_reader = csv.DictReader(csv_file)
#             for row in csv_reader:
#                 if (
#                     row['first_name'] == first_name and
#                     row['last_name'] == last_name and
#                     row['admission_no'] == admission_no
#                 ):
#                     match_found = True
#                     break

#         if match_found:
#             # Check if a user with the same email already exists
#             existing_user = User.objects.filter(username=email).first()

#             if existing_user:
#                 messages.error(request, 'User with this email already exists')
#             else:
#                 # Create a new user with is_staff=True
#                 user = User.objects.create_user(
#                     username=email,
#                     first_name=first_name,
#                     last_name=last_name,
#                     email=email,
#                 )
#                 user.is_staff = True  # Set as staff
#                 user.set_password("Student@Zillionhire1")
#                 user.save()

#                 # Create a new Student
#                 student = AdminStudent(
#                     user=user,
#                     admission_no=admission_no,
#                     phone=phone,
#                     email=email
#                 )
#                 student.save()

#                 subject = 'ZillionHire Student Login Details'
#                 message = f'Registered as Student. Your username: {email}, Password: Student@Zillionhire1'
#                 from_email = settings.EMAIL_HOST_USER # Your email address
#                 recipient_list = [user.email] # Employee's email address

#                 send_mail(subject, message, from_email, recipient_list)


#                 messages.success(request, 'Student added successfully')
#         else:
#             messages.error(request, 'No matching records found')

#     return render(request, 'admin/student/student.html', context={'messages': messages.get_messages(request)})
def add_student(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        admission_no = request.POST.get('admission_no', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        course_end_date = request.POST.get('course_end_date', '')  # New field

        # Path to your CSV file for validation
        csv_file_path = 'dataset/student.csv'
        match_found = False

        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if (
                    row['first_name'] == first_name and
                    row['last_name'] == last_name and
                    row['admission_no'] == admission_no
                ):
                    match_found = True
                    break

        if match_found:
            # Check if a user with the same email already exists
            existing_user = User.objects.filter(username=email).first()

            if existing_user:
                messages.error(request, 'User with this email already exists')
            else:
                # Create a new user with is_staff=True
                user = User.objects.create_user(
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
                user.is_staff = True  # Set as staff
                user.set_password("Student@Zillionhire1")
                user.save()

                # Create a new Student
                student = AdminStudent(
                    user=user,
                    admission_no=admission_no,
                    phone=phone,
                    email=email,
                    course_end_date=course_end_date  # Assign course end date
                )
                student.save()

                subject = 'ZillionHire Student Login Details'
                message = f'Registered as Student. Your username: {email}, Password: Student@Zillionhire1'
                from_email = settings.EMAIL_HOST_USER  # Your email address
                recipient_list = [user.email]  # Employee's email address

                send_mail(subject, message, from_email, recipient_list)

                messages.success(request, 'Student added successfully')
        else:
            messages.error(request, 'No matching records found')

    return render(request, 'admin/student/student.html', context={'messages': messages.get_messages(request)})
def adpostjob(request):
    return render(request,'adpostjob.html')



    from django.shortcuts import get_object_or_404, redirectprimary
    # @login_required(login_url='login_page')
def approved_jobs(request, job_id):
    approvejob = get_object_or_404(Jobs, id=job_id)
    
    approvejob.is_approved = True
    approvejob.save()       
        # Redirect back to the list of approved appointments
    return redirect('jobslist')
 

def job_approve(request, studentprofile_id):
    admjob = Jobs.objects.filter(is_approved=True)
    studentprofile = StudentProfile.objects.filter(id=studentprofile_id).first()
    print(studentprofile)
    print(admjob) 
    return render(request, 'adpostjob.html', {'admjob': admjob, 'studentprofile_id': studentprofile_id,'studentprofile':studentprofile})


def eligibility(request):
    return render(request,'eligibility.html')

def cprofile(request, companyprofile_id):
    companyprofile=CompanyProfile.objects.get(id=companyprofile_id)
    
    if request.method == "POST":
         addressline1 = request.POST.get('addressline1')
         contact = request.POST.get('contact')
         website = request.POST.get('website')
         reset_password = request.POST.get('reset_password')
         old_password = request.POST.get('old_password')
    
         companydp=request.FILES['companydp'] if 'companydp' in request.FILES else None
 
         companyprofile.addressline1 = addressline1
         companyprofile.contact = contact
         companyprofile.website= website 
         companyprofile.companydp=companydp

         if request.user.check_password(old_password):
            #  the old password is correct, set the new password
                request.user.set_password(reset_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Update the session to prevent logging out
         else:
            messages.error(request, "Incorrect old password. Password not updated.")
        
        
         companyprofile.reset_password = reset_password
         companyprofile.save()
         
         messages.success(request, 'Profile updated successfully.')
         return redirect('cindex')
    else:
         print("NO")
    context={
        'companyprofile': companyprofile
        
    }
    return render(request, 'cprofile.html', context)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from website.models import StudentProfile



@login_required
def sindex(request):
    try:
        studentprofile = request.user.studentprofile
        return render(request, 'sindex.html', {'studentprofile': studentprofile})
    except StudentProfile.DoesNotExist:
        studentprofile = StudentProfile.objects.create(user=request.user)
        return redirect(reverse('sprofile', kwargs={'studentprofile_id': studentprofile.id}))



#student
@login_required
def sabout(request):
    try:
        studentprofile = request.user.studentprofile
        return render(request, 'sabout.html', {'studentprofile': studentprofile})
    except StudentProfile.DoesNotExist:
        studentprofile = StudentProfile.objects.create(user=request.user)
        return redirect(reverse('sprofile', kwargs={'studentprofile_id': studentprofile.id}))


@login_required
def scontact(request):
    try:
        studentprofile = request.user.studentprofile
        return render(request, 'scontact.html', {'studentprofile': studentprofile})
    except StudentProfile.DoesNotExist:
        studentprofile = StudentProfile.objects.create(user=request.user)
        return redirect(reverse('sprofile', kwargs={'studentprofile_id': studentprofile.id}))


@login_required
def shome(request):
    return render(request, 'shome.html')

from django.contrib.auth import update_session_auth_hash  # Add this import
@login_required
def sprofile(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    admin_student = request.user.student_profile  # Accessing the related AdminStudent
    
    if request.method == "POST":
        admission_no = request.POST.get('admission_no')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        dob = request.POST.get('dob')
        nationality = request.POST.get('nationality')
        religion = request.POST.get('religion')
        profile_photo = request.FILES.get('profile_photo')
        gender = request.POST.get('gender')

        email = request.POST.get('email')
        phone = request.POST.get('phone')
        present_address = request.POST.get('present_address')
        permanent_address = request.POST.get('permanent_address')

        course = request.POST.get('course')
        department = request.POST.get('department')
        academic_year = request.POST.get('academic_year')
        passout_year = request.POST.get('passout_year')
        current_semester = request.POST.get('current_semester')
        cgpa = request.POST.get('cgpa')
        c_backlog=request.POST.get('c_backlog')


        twelfth_institution = request.POST.get('twelfth_institution')
        twelfth_cgpa = request.POST.get('twelfth_cgpa')
        twelfth_course = request.POST.get('twelfth_course')
        # profile_photo = request.FILES.get('profile_photo')
        twelfth_certificate_upload = request.FILES.get('twelfth_certificate_upload')

        tenth_institution = request.POST.get('tenth_institution')
        tenth_cgpa = request.POST.get('tenth_cgpa')
        tenth_course = request.POST.get('tenth_course')
        tenth_certificate_upload = request.FILES.get('tenth_certificate_upload')

        ug_institution = request.POST.get('ug_institution')
        ug_cgpa = request.POST.get('ug_cgpa')
        ug_course = request.POST.get('ug_course')
        ug_certificate_upload = request.FILES.get('ug_certificate_upload')


        reset_password = request.POST.get('reset_password')
        old_password = request.POST.get('old_password')


        # Update the student profile
        if profile_photo:
            studentprofile.profile_photo = profile_photo

        studentprofile.admission_no = admission_no
        studentprofile.first_name = first_name
        studentprofile.last_name = last_name
        studentprofile.gender = gender
        studentprofile.dob = dob
        studentprofile.nationality = nationality
        studentprofile.religion = religion
    
        studentprofile.email = email
        studentprofile.phone = phone
        studentprofile.present_address = present_address
        studentprofile.permanent_address = permanent_address

        studentprofile.course = course
        studentprofile.department = department
        studentprofile.academic_year = academic_year
        studentprofile.passout_year = passout_year
        studentprofile.current_semester = current_semester
        studentprofile.c_cgpa = cgpa
        studentprofile.c_backlog = c_backlog

        studentprofile.twelfth_institution = twelfth_institution
        studentprofile.twelfth_cgpa = twelfth_cgpa
        studentprofile.twelfth_course = twelfth_course
        if twelfth_certificate_upload:
            studentprofile.twelfth_certificate_upload = twelfth_certificate_upload
        # studentprofile.twelfth_certificate_upload = twelfth_certificate_upload

        studentprofile.tenth_institution = tenth_institution
        studentprofile.tenth_course = tenth_course
        studentprofile.tenth_cgpa = tenth_cgpa
        if tenth_certificate_upload:
            studentprofile.tenth_certificate_upload = tenth_certificate_upload
        # studentprofile.tenth_certificate_upload = tenth_certificate_upload

        studentprofile.ug_institution = ug_institution
        studentprofile.ug_course = ug_course
        studentprofile.ug_cgpa = ug_cgpa
        if ug_certificate_upload:
            studentprofile.ug_certificate_upload = ug_certificate_upload
        # studentprofile.ug_certificate_upload = ug_certificate_upload

        
        if request.user.check_password(old_password):
            #  the old password is correct, set the new password
                request.user.set_password(reset_password)
                request.user.save()
                update_session_auth_hash(request, request.user)  # Update the session to prevent logging out
        else:
            messages.error(request, "Incorrect old password. Password not updated.")
        
        
        studentprofile.reset_password = reset_password
        studentprofile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('sprofile', studentprofile_id=studentprofile_id)
        

    context = {
        'studentprofile': studentprofile,
        'admin_student':admin_student,
    }
    return render(request, 'student/sprofile.html', context)


# def jobapply(request, jobapply_id):

#     stuprof = get_object_or_404(StudentProfile, user=request.user)
    
#     job = get_object_or_404(Jobs, id=jobapply_id)
#     existing_certification = JobApplication.objects.filter(user=request.user,job=job).first()

#     if existing_certification:
#         certification_status = existing_certification.is_approved
#     else:
#         certification_status = 'pending'  # Set a default value if no certification exists
#     print(existing_certification)

#     if certification_status == 'pending':
#         if request.method == "POST":
            
#             # jobapply = JobApplication(stuprof=stuprof)

#             cname=request.POST.get('cname')
#             jname=request.POST.get('jname')
#             first_name = request.POST.get('first_name')
#             last_name = request.POST.get('last_name')
#             dob = request.POST.get('dob')
#             nationality = request.POST.get('nationality')
#             profile_photo = request.FILES.get('profile_photo')
#             gender = request.POST.get('gender')
#             email = request.POST.get('email')
#             phone = request.POST.get('phone')
#             present_address = request.POST.get('present_address')
#             permanent_address = request.POST.get('permanent_address')
#             area_code = request.POST.get('area_code')

#             c_course = request.POST.get('c_course')
#             c_institution = request.POST.get('c_institution')
#             c_university = request.POST.get('c_university')
#             academic_year = request.POST.get('academic_year')
#             c_backlog = request.POST.get('c_backlog')
#             c_cgpa = request.POST.get('c_cgpa')

#             twelfth_institution = request.POST.get('twelfth_institution')
#             twelfth_cgpa = request.POST.get('twelfth_cgpa')
#             twelfth_board = request.POST.get('twelfth_board')
#             twelfth_certificate_upload = request.FILES.get('twelfth_certificate_upload')

#             tenth_institution = request.POST.get('tenth_institution')
#             tenth_cgpa = request.POST.get('tenth_cgpa')
#             tenth_board = request.POST.get('tenth_board')
#             tenth_certificate_upload = request.FILES.get('tenth_certificate_upload')

#             ug_course = request.POST.get('ug_course')
#             ug_institution = request.POST.get('ug_institution')
#             ug_cgpa = request.POST.get('ug_cgpa')
#             ug_university = request.POST.get('ug_university')
#             ug_certificate_upload = request.FILES.get('ug_certificate_upload')

#             skills=request.POST.get('skills')
#             newcourse=request.POST.get('newcourse')
#             newcert=request.FILES.get('newcert')

#             workexperience=request.POST.get('workexperience')
#             jobresp=request.POST.get('jobresp')
#             period=request.POST.get('period')
#             companydetails=request.POST.get('companydetails')

#             crime=request.POST.get('crime')
#             dtoc=request.POST.get('dtoc')
#             doc=request.POST.get('doc')
#             nature=request.POST.get('nature')

#             resume = request.FILES.get('resume')

#             # jobapply = get_object_or_404(JobApplication, stuprof=stuprof)

#             jobapply = JobApplication.objects.create(
#                     user=request.user,
#                     job=job,
#                     stuprof=stuprof,
#                     cname = cname,
#                     jname = jname,
#                     first_name = first_name,
#                     last_name = last_name,
#                     gender = gender,
#                     dob = dob,
#                     nationality = nationality,
#                     area_code = area_code,
#                     profile_photo=profile_photo,
        
#                     email = email,
#                     phone = phone,
#                     present_address = present_address,
#                     permanent_address = permanent_address,

#                     c_course = c_course,
#                     c_institution = c_institution,
#                     c_university = c_university,
#                     academic_year = academic_year,
#                     c_backlog = c_backlog,
#                     c_cgpa = c_cgpa,

#                     twelfth_institution = twelfth_institution,
#                     twelfth_cgpa = twelfth_cgpa,
#                     twelfth_board = twelfth_board,
        
#                     twelfth_certificate_upload = twelfth_certificate_upload,
#             # studentprofile.twelfth_certificate_upload = twelfth_certificate_upload

#                     tenth_institution = tenth_institution,
#                     tenth_board = tenth_board,
#                     tenth_cgpa = tenth_cgpa,
#                     tenth_certificate_upload = tenth_certificate_upload,
#             # studentprofile.tenth_certificate_upload = tenth_certificate_upload

#                     ug_institution = ug_institution,
#                     ug_university= ug_university,
#                     ug_course = ug_course,
#                     ug_cgpa = ug_cgpa,
#                     ug_certificate_upload = ug_certificate_upload,
#             # studentprofile.ug_certificate_upload = ug_certificate_upload

#                     skills=skills,
#                     newcourse=newcourse,
#                     newcert=newcert,

#                     workexperience=workexperience,
#                     jobresp=jobresp,
#                     period=period,
#                     companydetails=companydetails,

#                     crime=crime,
#                     dtoc=dtoc,
#                     doc=doc,
#                     nature=nature,
#                     resume = resume
#                 )

#             jobapply.save()
#             messages.success(request, 'Job submitted successfully.')
#             print("Job Apply ID:", jobapply_id)

#             return redirect('jobapply', jobapply_id=jobapply_id)  # Use job.id instead of jobapply.id



#         context = {
#             # 'jobapply': jobapply,
#             # 'admin_student':admin_student,
#             'sprof':stuprof,
#             'jobapply_id': jobapply_id,
#             'job':job,
#             'certification_status': certification_status
#         }
#         return render(request, 'student/jobapply.html', context)
    
#     else:
#         return render(request, 'student/jobapply.html', {'certification_status': certification_status})

def jobapply(request, jobapply_id):

    stuprof = get_object_or_404(StudentProfile, user=request.user)
    # company_profile = CompanyProfile.objects.get(user=request.user)
    job = get_object_or_404(Jobs, id=jobapply_id)
    existing_certification = JobApplication.objects.filter(user=request.user,job=job).first()

    if existing_certification:
        certification_status = existing_certification.is_approved
    else:
        certification_status = 'pending'  # Set a default value if no certification exists
    print(existing_certification)

    if certification_status == 'pending':
        if request.method == "POST":
            
            # jobapply = JobApplication(stuprof=stuprof)

            cname=request.POST.get('cname')
            jname=request.POST.get('jname')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            dob = request.POST.get('dob')
            nationality = request.POST.get('nationality')
            profile_photo = request.FILES.get('profile_photo')
            gender = request.POST.get('gender')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            present_address = request.POST.get('present_address')
            permanent_address = request.POST.get('permanent_address')
            area_code = request.POST.get('area_code')

            c_course = request.POST.get('c_course')
            c_institution = request.POST.get('c_institution')
            c_university = request.POST.get('c_university')
            academic_year = request.POST.get('academic_year')
            c_backlog = request.POST.get('c_backlog')
            c_cgpa = request.POST.get('c_cgpa')

            twelfth_institution = request.POST.get('twelfth_institution')
            twelfth_cgpa = request.POST.get('twelfth_cgpa')
            twelfth_board = request.POST.get('twelfth_board')
            twelfth_certificate_upload = request.FILES.get('twelfth_certificate_upload')

            tenth_institution = request.POST.get('tenth_institution')
            tenth_cgpa = request.POST.get('tenth_cgpa')
            tenth_board = request.POST.get('tenth_board')
            tenth_certificate_upload = request.FILES.get('tenth_certificate_upload')

            ug_course = request.POST.get('ug_course')
            ug_institution = request.POST.get('ug_institution')
            ug_cgpa = request.POST.get('ug_cgpa')
            ug_university = request.POST.get('ug_university')
            ug_certificate_upload = request.FILES.get('ug_certificate_upload')

            skills=request.POST.get('skills')
            newcourse=request.POST.get('newcourse')
            newcert=request.FILES.get('newcert')

            workexperience=request.POST.get('workexperience')
            jobresp=request.POST.get('jobresp')
            period=request.POST.get('period')
            companydetails=request.POST.get('companydetails')

            crime=request.POST.get('crime')
            dtoc=request.POST.get('dtoc')
            doc=request.POST.get('doc')
            nature=request.POST.get('nature')

            resume = request.FILES.get('resume')

            # jobapply = get_object_or_404(JobApplication, stuprof=stuprof)

            jobapply = JobApplication.objects.create(
                    user=request.user,
                    job=job,
                    stuprof=stuprof,
                    cname = cname,
                    jname = jname,
                    first_name = first_name,
                    last_name = last_name,
                    gender = gender,
                    dob = dob,
                    nationality = nationality,
                    area_code = area_code,
                    profile_photo=profile_photo,
        
                    email = email,
                    phone = phone,
                    present_address = present_address,
                    permanent_address = permanent_address,

                    c_course = c_course,
                    c_institution = c_institution,
                    c_university = c_university,
                    academic_year = academic_year,
                    c_backlog = c_backlog,
                    c_cgpa = c_cgpa,

                    twelfth_institution = twelfth_institution,
                    twelfth_cgpa = twelfth_cgpa,
                    twelfth_board = twelfth_board,
        
                    twelfth_certificate_upload = twelfth_certificate_upload,
            # studentprofile.twelfth_certificate_upload = twelfth_certificate_upload

                    tenth_institution = tenth_institution,
                    tenth_board = tenth_board,
                    tenth_cgpa = tenth_cgpa,
                    tenth_certificate_upload = tenth_certificate_upload,
            # studentprofile.tenth_certificate_upload = tenth_certificate_upload

                    ug_institution = ug_institution,
                    ug_university= ug_university,
                    ug_course = ug_course,
                    ug_cgpa = ug_cgpa,
                    ug_certificate_upload = ug_certificate_upload,
            # studentprofile.ug_certificate_upload = ug_certificate_upload

                    skills=skills,
                    newcourse=newcourse,
                    newcert=newcert,

                    workexperience=workexperience,
                    jobresp=jobresp,
                    period=period,
                    companydetails=companydetails,

                    crime=crime,
                    dtoc=dtoc,
                    doc=doc,
                    nature=nature,
                    resume = resume
                )

            jobapply.save()
            messages.success(request, 'Job submitted successfully.')
            print("Job Apply ID:", jobapply_id)

            return redirect('jobapply', jobapply_id=jobapply_id)  # Use job.id instead of jobapply.id



        context = {
            # 'jobapply': jobapply,
            # 'admin_student':admin_student,
            'sprof':stuprof,
            'jobapply_id': jobapply_id,
            'job':job,
            'certification_status': certification_status,
            # 'company_profile': company_profile 
        }
        return render(request, 'student/jobapply.html', context)
    
    else:
        return render(request, 'student/jobapply.html', {'certification_status': certification_status})





 
def appliedstudents(request):
    # Retrieve all Jobs instances associated with the current user
    jobs_instances = Jobs.objects.filter(user=request.user)

    if jobs_instances.exists():
        # If Jobs instances are found, filter JobApplications based on them
        app_stu = JobApplication.objects.filter(job__in=jobs_instances)
    else:
        # If no Jobs instances are found, provide an empty queryset
        app_stu = JobApplication.objects.none()

    context = {'app_stu': app_stu}
    return render(request, 'company/appliedstudents.html', context)

def adminappstudents(request):
    
    app_stu = JobApplication.objects.all()
    context = {'app_stu': app_stu }
    return render(request, 'admin/adminappstudents.html',context)

def admin_shortlist(request):
    jobs_instances = Jobs.objects.all()

    if jobs_instances.exists():
        # If Jobs instances are found, filter JobApplications based on them
        app_stu = JobApplication.objects.all()
    else:
        # If no Jobs instances are found, provide an empty queryset
        app_stu = JobApplication.objects.none()

    context = {'app_stu': app_stu}
    return render(request,'admin/admin_shortlist.html', context)
 
def cfirstround(request):
    jobs_instances = Jobs.objects.filter(user=request.user)

    if jobs_instances.exists():
        # If Jobs instances are found, filter JobApplications based on them
        app_stu = JobApplication.objects.filter(job__in=jobs_instances)
    else:
        # If no Jobs instances are found, provide an empty queryset
        app_stu = JobApplication.objects.none()

    context = {'app_stu': app_stu}
    return render(request,'company/cfirstround.html', context)

@login_required
def sappliedjobs(request, studentprofile_id):
    user=request.user
    app_stu = JobApplication.objects.filter(user=user)
    context = {'app_stu': app_stu, 'studentprofile_id': studentprofile_id}

    return render(request,'sappliedjobs.html',context)




def s_shortlist(request, studentprofile_id):
    user=request.user
    app_stu = JobApplication.objects.filter(user=user)
    context = {'app_stu': app_stu, 'studentprofile_id': studentprofile_id}
    return render(request, 'sfirstround.html', context)



from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def studentprofileapp(request, studentprofile_id):
    print(f"Requested studentprofile_id: {studentprofile_id}")
    print(f"Authenticated user: {request.user}")
    # stuprof = get_object_or_404(StudentProfile, user=request.user)

    # Retrieve the JobApplication based on the user and studentprofile_id
    job_application = get_object_or_404(JobApplication, id=studentprofile_id)
    # job_application = JobApplication.objects.filter(stuprof__id=studentprofile_id)
    print('First Name:', job_application.first_name)
    print('Job' , job_application)
    # Pass the retrieved JobApplication to the template
    context = {'job_application': job_application, 'studentprofile_id': studentprofile_id}
    return render(request, 'company/studentprofileapp.html', context)










def approve_shortlist(request, application_id):
    shortlist = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        shortlist.is_approved = JobApplication.APPROVED  # Set it to 'approved'
        shortlist.save()
        
    return redirect('appliedstudents')


def reject_shortlist(request, application_id):
    shortlist = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        shortlist.is_approved = JobApplication.REJECTED  # Set it to 'approved'
        shortlist.save()
    return redirect('appliedstudents')

#admin_resources
def admincontent(request):
    return render(request, 'admin/resources/content.html')

def contentform(request):
    # if 'cmp' in request.session:
    return render(request,'admin/resources/contentform.html')
    # return render(request,'index.html')


def contentview(request,id):
    feed=internship.objects.all()
    more=classdetails.objects.filter(candi_id=id)
    context = {'feed': feed,'more':more}
    return render(request,'admin/resources/contentview.html', context)
def interinfo(request):
    if 'can' in request.session:
       inid=request.POST.get('inid')
       data=internship.objects.filter(intern_id=inid)
       return render(request,"interinfo.html",{'data':data})
    return render(request,'index.html')
def classdetail(request):  
    inid= request.POST['inid']
    caid= request.POST['caid']
    more=classdetails.objects.filter(candi_id=caid,inter_id=inid)
    feed=internship.objects.filter(intern_id=inid)
    can=User.objects.get(id=caid)
    inter=internship.objects.get(intern_id=inid)
    # user = classdetails(candi_id=caid,inter_id=inid,interndate,interntimes)
    # user.save()
    return render(request,'classdetails.html',{'can':can.username,'inter':inter.title,'interid':inter.intern_id,'more':more,'feed':feed,'mo':inid,'mor':caid})

from datetime import datetime
def intern1(request):
      if request.method == 'POST':
        tit = request.POST['tit']
        cap = request.POST['cap']
        sdate = request.POST['sdate']
        about = request.POST['about']
        image = request.FILES.get('p')
        pdf_file = request.FILES.get('pdf')
        member = internship(title=tit,caption=cap,stdate=sdate,img=image,pdf=pdf_file,moreinfo=about)
        member.save()
        return redirect('contentform')
      
def resumeform(request):
    # if 'cmp' in request.session:
    return render(request,'admin/resources/resumeform.html')

def resume1(request):
    if request.method == 'POST':
        title = request.POST['title']
        more = request.POST['more']
        date = request.POST['date']

        image = request.FILES.get('image')
        pdf_file = request.FILES.get('pdf')
        video = request.FILES.get('video')
        
        entry = resumeadmin(title=title, more=more, date=date, image=image, pdf=pdf_file, video=video)
        entry.save()
        return redirect('resumeform')



def resumelist(request):
    adconts=resumeadmin.objects.all()
    return render(request,'admin/resources/resumelist.html',{'adconts': adconts})

def contentlist(request):
    adconts=internship.objects.all()
    return render(request,'admin/resources/contentlist.html',{'adconts': adconts})


from .models import StudentProfile

def toggle_alumni_status(request, student_profile_id):
    student_profile = StudentProfile.objects.get(pk=student_profile_id)

    # Toggle the is_alumni field
    student_profile.is_alumni = not student_profile.is_alumni
    student_profile.save()

    return redirect('ad_studentlist')  # Replace 'your_redirect_url' with the appropriate URL name
def videoform(request):
    # if 'cmp' in request.session:
    return render(request,'admin/resources/videoform.html')

def videolibraryadd(request):
    if request.method == 'POST':
        print(request.POST)  # Add this line to print the POST data to the console
        tit = request.POST['tit']
        cap = request.POST['cap']
        sdate = request.POST['sdate']
        about = request.POST['about']
        image = request.FILES.get('p')
        video_file = request.FILES.get('video')
        vdo = videolibrary(title=tit,caption=cap,stdate=sdate,img=image,video=video_file,moreinfo=about)
        vdo.save()
        return redirect('videoform')
def videolist(request):
    adconts=videolibrary.objects.all()
    return render(request,'admin/resources/videolist.html',{'adconts': adconts})

#content2
def content2form(request):
    # if 'cmp' in request.session:
    return render(request,'admin/resources/content2form.html')
    # return render(request,'index.html')
def content2list(request):
    adcont=ccontent.objects.all()
    return render(request,'admin/resources/content2list.html',{'adcont': adcont})

def content2(request):
      if request.method == 'POST':
        cname = request.POST['cname']
        name = request.POST['name']
        udate = request.POST['udate']        
        img = request.FILES.get('p')
        pdf = request.FILES.get('pdf')
        price = request.POST.get('price')
        price = Decimal(price) if price else None

        member = ccontent(cname=cname,name=name,udate=udate,img=img,pdf=pdf, price=price)
        member.save()
        return redirect('content2form')
      
def searchcontent(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        # Filter the data based on the search query
        content_list = internship.objects.filter(title__icontains=search_query)
        
        if not content_list.exists():
            # If the list is empty, render a "Not Found" template
            return render(request, 'admin/resources/not_found.html', {'search_query': search_query})
        
        context = {'adconts': content_list}
        return render(request, 'admin/resources/contentlist.html', context)
    
    return render(request, 'admin/resources/contentlist.html')

def searchvideo(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        print("Search Query:", search_query)  # Add this line to print the search query
        # Filter the data based on the search query
        video_list = videolibrary.objects.filter(title__icontains=search_query)
        print(video_list)
        
        if not video_list.exists():
            # If the list is empty, print a message for debugging
            print("No videos found for the search query:", search_query)
            return render(request, 'admin/resources/videolist.html', {'search_query': search_query})
        
        context = {'adconts': video_list}
        return render(request, 'admin/resources/videolist.html', context)
    
    return render(request, 'admin/resources/videolist.html')


def content2form(request):
    return render(request,'admin/resources/content2form.html')


def aptform(request, aptitude_id=None):
    # Fetch the company profile related to the logged-in user
    company_profile = CompanyProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            date_and_time = request.POST.get('date_and_time')
            link = request.POST.get('link')
            login_id = request.POST.get('login_id')
            password = request.POST.get('password')
            steps = request.POST.get('steps')
            regulations = request.POST.get('regulations')
            
            if aptitude_id:
                # Update existing instance if aptitude_id is provided
                aptitude = AddAptitude.objects.get(pk=aptitude_id)
            else:
                # Create new instance if aptitude_id is not provided
                aptitude = AddAptitude()

            # Assign values to the fields
            aptitude.title = title
            aptitude.description = description
            aptitude.date_and_time = date_and_time
            aptitude.link = link
            aptitude.login_id = login_id
            aptitude.password = password
            aptitude.steps = steps
            aptitude.regulations = regulations
            aptitude.company_profile = company_profile  # Associate CompanyProfile with AddAptitude
            aptitude.companyname = company_profile.companyname  # Set companyname from company_profile

            aptitude.save()  # Save the instance

            # Redirect to the form page with the newly created/updated instance
            return redirect('aptform', aptitude_id=aptitude.id)  
        except Exception as e:
            print(e)  # Print the exception for debugging purposes
            # You might want to render a form with error messages here
            # For simplicity, we'll just return a generic error response
            return redirect('aptform')  # Redirect to the form page

    if aptitude_id:
        aptitude = AddAptitude.objects.get(pk=aptitude_id)
    else:
        aptitude = None
    
    context = {
        'aptitude': aptitude,
        'company_profile': company_profile,  # Pass the company profile to the template context
    }
    return render(request, 'company/add_aptitude.html', context)


def aptform2(request):
    return render(request,'company/add_aptitude.html')

#studentcontent2
from decimal import Decimal

def scontent2list(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    adcon=ccontent.objects.all()
    liked_content_ids = LikedContent.objects.filter(user=request.user).values_list('adcon__id', flat=True)
    return render(request, 'admin/resources/scontent2list.html', {'studentprofile': studentprofile, 'adcon': adcon, 'liked_content_ids':liked_content_ids})

def scontent1list(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    adcont = internship.objects.all()

    # Get the values of selected checkboxes
    cpp_filter = request.GET.get('cpp', False)
    java_filter = request.GET.get('java', False)
    python_filter = request.GET.get('python', False)
    php_filter = request.GET.get('php', False)

    # Apply filters based on checkbox values
    if cpp_filter:
        adcont = adcont.filter(title__icontains='cpp')

    if java_filter:
        adcont = adcont.filter(title__icontains='java')

    if python_filter:
        adcont = adcont.filter(title__icontains='python')

    if php_filter:
        adcont = adcont.filter(title__icontains='php')

    return render(request, 'admin/resources/scontent1list.html', {'studentprofile': studentprofile, 'adcont': adcont})


def svideolist(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    adcont=videolibrary.objects.all()
    # liked_content_ids = LikedContent.objects.filter(user=request.user).values_list('adcon__id', flat=True)
    return render(request, 'admin/resources/svideolist.html', {'studentprofile': studentprofile, 'adcont': adcont})

# views.py
from django.db.models import Q

def s_searchvideo(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    query = request.GET.get('q', '')  # Get the search query from the URL parameter

    # Search for video content based on the title
    adcont = videolibrary.objects.filter(Q(title__icontains=query))

    return render(request, 'admin/resources/svideolist.html', {'studentprofile': studentprofile, 'adcont': adcont, 'search_query': query})

# views.py
from django.http import JsonResponse

def s_searchvideo_ajax(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    query = request.GET.get('q', '')  # Get the search query from the AJAX request

    # Search for video content based on the title
    adcont = videolibrary.objects.filter(title__icontains=query)

    # Convert the queryset to a list of dictionaries for JSON response
    video_list = [{'title': video.title, 'moreinfo': video.moreinfo} for video in adcont]

    return JsonResponse({'videos': video_list})


def search_content2(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    
    # Fetch the search query from the GET parameters
    search_query = request.GET.get('search', '')

    # Filter ccontent objects by company name
    adcon = ccontent.objects.filter(cname__icontains=search_query)

    # You may need to adjust the filtering logic based on your requirements

    # Add any additional context data you need for your template
    context = {
        'studentprofile': studentprofile,
        'adcon': adcon,
        'search_query': search_query,
        # 'liked_content_ids': LikedContent.objects.filter(user=request.user).values_list('adcon__id', flat=True),
    }
    return render(request, 'admin/resources/scontent2list.html', context)


def search_content1(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    search_query = request.GET.get('search', '')
    
    # Perform the search based on the title field
    adcont = internship.objects.filter(title__icontains=search_query)
    
    return render(request, 'admin/resources/scontent1list.html', {'studentprofile': studentprofile, 'adcont': adcont, 'search_query': search_query})
# def payconfirm(request):
#     return render(request, 'registration.html')

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import LikedContent
from django.contrib.auth.decorators import login_required
@csrf_exempt  # This decorator is used for simplicity; consider using a more secure approach in production
@require_POST
@login_required
def save_liked_content(request):
    adcon_id = request.POST.get('adcon_id')

    if adcon_id:
        user = request.user
        adcon = ccontent.objects.get(id=adcon_id)

        # Check if the user already liked this content
        if not LikedContent.objects.filter(user=user, adcon=adcon).exists():
            # If not, save the liked content
            LikedContent.objects.create(user=user, adcon=adcon)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid parameters'})
def save_liked_content1(request):
    adcont_id = request.POST.get('adcont_id')

    if adcont_id:
        user = request.user
        adcon = ccontent.objects.get(id=adcont_id)

        # Check if the user already liked this content
        if not LikedContent1.objects.filter(user=user, adcont=adcont).exists():
            # If not, save the liked content
            LikedContent1.objects.create(user=user, adcon=adcon)

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid parameters'})

@csrf_exempt
def toggle_like1(request):
    if request.method == 'POST':
        adcont_id = request.POST.get('adcont_id')
        status = request.POST.get('status')
        
        user = request.user
        adcont = internship.objects.get(id=adcont_id)

        # Check if LikedContent entry already exists
        liked_content, created = LikedContent1.objects.get_or_create(user=user, adcont=adcont)

        # Toggle the like status
        liked_content.status = not liked_content.status if status == 'true' else True
        liked_content.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})



# def likedcontent2(request, studentprofile_id):
#     studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
#     return render(request,'admin/resources/likedcontent2.html', {'studentprofile': studentprofile})
def likedcontent2(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    liked_contents = LikedContent.objects.filter(user=request.user)  # Assuming you are using the user attribute for the filter
    return render(request, 'admin/resources/likedcontent2.html', {'studentprofile': studentprofile, 'liked_contents': liked_contents})
from django.http import JsonResponse

@csrf_exempt
def toggle_like(request):
    if request.method == 'POST':
        adcon_id = request.POST.get('adcon_id')
        status = request.POST.get('status')
        
        user = request.user
        adcon = ccontent.objects.get(id=adcon_id)

        # Check if LikedContent entry already exists
        liked_content, created = LikedContent.objects.get_or_create(user=user, adcon=adcon)

        # Toggle the like status
        liked_content.status = not liked_content.status if status == 'true' else True
        liked_content.save()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def adcontent2(request):
    return render(request, 'admin/resources/ad_content2view.html')
# def editcontent2(request):
#     return render(request, 'admin/resources/editcontent2.html')
def editcontent2(request, content_id):
    # Assuming you pass the content_id in the URL (e.g., /editcontent2/1/)
    content_instance = get_object_or_404(ccontent, id=content_id)

    if request.method == 'POST':
        # Handle form submission to update the content instance
        # You'll need to implement the update logic based on your form fields
        content_instance.cname = request.POST['cname']
        content_instance.name = request.POST['name']
        content_instance.udate = request.POST['udate']
        content_instance.img = request.FILES.get('p')
        content_instance.pdf = request.FILES.get('pdf')
        content_instance.price = Decimal(request.POST.get('price')) if request.POST.get('price') else None

        content_instance.save()

        # Redirect to the content list or another page
        return redirect('content2list')

    # For GET requests, render the edit form
    return render(request, 'admin/resources/editcontent2.html', {'content_instance': content_instance})

def dlt_content2(request):
    if request.method == 'GET':
        content_id = request.GET.get('id')
        content_instance = get_object_or_404(ccontent, id=content_id)
        content_instance.delete()
        return redirect('content2list')
    

def dlt_content1(request, id):  # Use the same parameter name as in the URL pattern
    if request.method == 'GET':
        adcont_instance = get_object_or_404(internship, id=id)
        adcont_instance.delete()
        return redirect('contentlist')
     
def alumnilist(request):
    alumni_list = Alumni.objects.all()
    return render(request, 'admin/student/alumnilist.html', {'alumni_list': alumni_list})

def toggle_alumni_status(request, student_profile_id):
    student_profile = get_object_or_404(StudentProfile, id=student_profile_id)

    # Toggle alumni status
    student_profile.is_alumni = not student_profile.is_alumni
    student_profile.save()

    if student_profile.is_alumni:
        # If the student is marked as alumni, create an Alumni instance
        alumni_instance = Alumni.objects.create(
            user=student_profile.user,
            adminstu=student_profile.adminstu,
            admission_no=student_profile.admission_no,
            is_alumni=True,
            first_name=student_profile.first_name,
            last_name=student_profile.last_name,
            dob=student_profile.dob,
            gender=student_profile.gender,
            nationality=student_profile.nationality,
            religion=student_profile.religion,

            email=student_profile.email,
            phone=student_profile.phone,
            present_address=student_profile.present_address,
            permanent_address=student_profile.permanent_address,

            course=student_profile.course,
            department=student_profile.department,
            academic_year=student_profile.academic_year,
            passout_year=student_profile.passout_year,
            current_semester=student_profile.current_semester,
            c_cgpa=student_profile.c_cgpa,
            c_backlog=student_profile.c_backlog,

            twelfth_institution=student_profile.twelfth_institution,
            twelfth_cgpa=student_profile.twelfth_cgpa,
            twelfth_course=student_profile.twelfth_course,

            tenth_institution=student_profile.tenth_institution,
            tenth_cgpa=student_profile.tenth_cgpa,
            tenth_course=student_profile.tenth_course,

            ug_institution=student_profile.ug_institution,
            ug_cgpa=student_profile.ug_cgpa,
            ug_course=student_profile.ug_course,
        )

        # Check if profile_photo exists and update the profile_photo
        profile_photo = request.FILES.get('profile_photo')
        if profile_photo:
            alumni_instance.profile_photo = profile_photo
            student_profile.profile_photo = profile_photo

        # Check if twelfth_certificate_upload exists and update the field
        twelfth_certificate_upload = request.FILES.get('twelfth_certificate_upload')
        if twelfth_certificate_upload:
            alumni_instance.twelfth_certificate_upload = twelfth_certificate_upload

        # Add other fields as needed

        alumni_profile.save()  # Save the Alumni instance after updating all fields

    return redirect('ad_studentlist')


#resume
from django.shortcuts import render 
def home(request): 
	return render(request, 'resume/index.html') 
 # Assuming your models.py is in the same directory

def gen_resume(request):
    if request.method == 'POST':
        # Retrieve data from the form
        name = request.POST.get('name', '')
        about = request.POST.get('about', '')
        age = request.POST.get('age', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        career_objective = request.POST.get('career_objective', '')
        address = request.POST.get('address', '')
        linkedin_profile = request.POST.get('linkedin_profile', '')
        git_profile = request.POST.get('git_profile', '')
        soft_skills = request.POST.get('soft_skills', '')
        skill1 = request.POST.get('skill1', '')
        skill2 = request.POST.get('skill2', '')
        skill3 = request.POST.get('skill3', '')
        skill4 = request.POST.get('skill4', '')
        skill5 = request.POST.get('skill5', '')
        degree1 = request.POST.get('degree1', '')
        college1 = request.POST.get('college1', '')
        cgpa1 = request.POST.get('cgpa1', '')
        year1 = request.POST.get('year1', '')
        degree2 = request.POST.get('degree2', '')
        college2 = request.POST.get('college2', '')
        cgpa2 = request.POST.get('cgpa2', '')
        year2 = request.POST.get('year2', '')
        college3 = request.POST.get('college3', '')
        cgpa3 = request.POST.get('cgpa3', '')
        year3 = request.POST.get('year3', '')
        lang1 = request.POST.get('lang1', '')
        lang2 = request.POST.get('lang2', '')
        lang3 = request.POST.get('lang3', '')
        project1 = request.POST.get('project1', '')
        durat1 = request.POST.get('duration1', '')
        desc1 = request.POST.get('desc1', '')
        project2 = request.POST.get('project2', '')
        durat2 = request.POST.get('duration2', '')
        desc2 = request.POST.get('desc2', '')
        company1 = request.POST.get('company1', '')
        post1 = request.POST.get('post1', '')
        duration1 = request.POST.get('duration1', '')
        lin11 = request.POST.get('lin11', '')
        company2 = request.POST.get('company2', '')
        post2 = request.POST.get('post2', '')
        duration2 = request.POST.get('duration2', '')
        lin21 = request.POST.get('lin21', '')
        ach1 = request.POST.get('ach1', '')
        ach2 = request.POST.get('ach2', '')
        ach3 = request.POST.get('ach3', '')
        internship1 = request.POST.get('internship1', '')
        internship2 = request.POST.get('internship2', '')
        internship3 = request.POST.get('internship3', '')
        certification1 = request.POST.get('certification1', '')
        certification2 = request.POST.get('certification2', '')
        certification3 = request.POST.get('certification3', '')
        image = request.FILES.get('image') 
        
        # Create an instance of the Resume model
        resume_instance = ResumeBuilder(
            name=name,
            about=about,
            age=age,
            email=email,
            phone=phone,
            career_objective=career_objective,
            address=address,
            linkedin_profile=linkedin_profile,
            git_profile=git_profile,
            soft_skills=soft_skills,
            skill1=skill1,
            skill2=skill2,
            skill3=skill3,
            skill4=skill4,
            skill5=skill5,
            degree1=degree1,
            college1=college1,
            cgpa1=cgpa1,
            year1=year1,
            degree2=degree2,
            college2=college2,
            cgpa2=cgpa2,
            year2=year2,
            college3=college3,
            cgpa3=cgpa3,
            year3=year3,
            lang1=lang1,
            lang2=lang2,
            lang3=lang3,
            project1=project1,
            durat1=durat1,
            desc1=desc1,
            project2=project2,
            durat2=durat2,
            desc2=desc2,
            company1=company1,
            post1=post1,
            duration1=duration1,
            lin11=lin11,
            company2=company2,
            post2=post2,
            duration2=duration2,
            lin21=lin21,
            ach1=ach1,
            ach2=ach2,
            ach3=ach3,
            internship1=internship1,
            internship2=internship2,
            internship3=internship3,
            certification1=certification1,
            certification2=certification2,
            certification3=certification3,
            image=image 
        )

        # Save the instance to the database
        resume_instance.save()

        # Pass the data to the template or redirect to another view
        return render(request, 'resume/resume.html', {'resume_instance': resume_instance})

    return render(request, 'resume/index.html')


def editcontent1(request, adcont_id):
    adcont = get_object_or_404(internship, pk=adcont_id)

    if request.method == 'POST':
        # Update the fields based on your model structure
        adcont.title = request.POST.get('title', adcont.title)
        adcont.caption = request.POST.get('caption', adcont.caption)
        adcont.moreinfo = request.POST.get('moreinfo', adcont.moreinfo)
        adcont.stdate = request.POST.get('stdate', adcont.stdate)

        # Handle file uploads for PDF and img
        pdf_file = request.FILES.get('pdf')
        img_file = request.FILES.get('img')

        if pdf_file:
            adcont.pdf = pdf_file

        if img_file:
            adcont.img = img_file

        # Parse the date string into a valid date object
        try:
            adcont.stdate = datetime.strptime(adcont.stdate, '%b. %d, %Y').date()
        except ValueError:
            # Handle the case when the date format is incorrect
            # You may want to redirect the user to an error page or show a validation message
            pass

        adcont.save()
        return redirect('contentlist')

    return render(request, 'admin/resources/editcontent1.html', {'adcont': adcont})
def editcontent2(request, content_id):
    # Assuming you pass the content_id in the URL (e.g., /editcontent2/1/)
    content_instance = get_object_or_404(ccontent, id=content_id)

    if request.method == 'POST':
        # Handle form submission to update the content instance
        # You'll need to implement the update logic based on your form fields
        content_instance.cname = request.POST['cname']
        content_instance.name = request.POST['name']
        content_instance.udate = request.POST['udate']
        content_instance.img = request.FILES.get('p')
        content_instance.pdf = request.FILES.get('pdf')
        content_instance.price = Decimal(request.POST.get('price')) if request.POST.get('price') else None

        content_instance.save()

        # Redirect to the content list or another page
        return redirect('content2list')

    # For GET requests, render the edit form
    return render(request, 'admin/resources/editcontent2.html', {'content_instance': content_instance})

# def alumni_index(request):
#     return render(request,'admin/alumni/alumni_index.html')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .models import Alumni

@login_required
def alumni_index(request):
    try:
        alumni_profile = request.user.alumni
        return render(request, 'admin/alumni/alumni_index.html', {'alumni_profile': alumni_profile})
    except Alumni.DoesNotExist:
        try:
            admin_student = request.user.adminstudent
            alumni_profile = Alumni.objects.create(user=request.user, adminstu=admin_student)
            return redirect(reverse('alumni_profile', kwargs={'alumni_id': alumni_profile.id}))
        except AdminStudent.DoesNotExist:
            messages.error(request, 'Alumni profile creation failed. Please contact admin.')
            return redirect(reverse('admin_index'))  # Redirect to home or any appropriate URL


@login_required
def acontact(request):
    try:
        alumni_profile = request.user.alumni
        return render(request, 'admin/alumni/acontact.html', {'alumni_profile': alumni_profile})
    except Alumni.DoesNotExist:
        try:
            admin_student = request.user.adminstudent
            alumni_profile = Alumni.objects.create(user=request.user, adminstu=admin_student)
            return redirect(reverse('alumni_profile', kwargs={'alumni_id': alumni_profile.id}))
        except AdminStudent.DoesNotExist:
            messages.error(request, 'Alumni profile creation failed. Please contact admin.')
            return redirect(reverse('admin_index'))  # Redirect to home or any appropriate URL
        

@login_required
def aabout(request):
    try:
        alumni_profile = request.user.alumni
        return render(request, 'admin/alumni/aabout.html', {'alumni_profile': alumni_profile})
    except Alumni.DoesNotExist:
        try:
            admin_student = request.user.adminstudent
            alumni_profile = Alumni.objects.create(user=request.user, adminstu=admin_student)
            return redirect(reverse('alumni_profile', kwargs={'alumni_id': alumni_profile.id}))
        except AdminStudent.DoesNotExist:
            messages.error(request, 'Alumni profile creation failed. Please contact admin.')
            return redirect(reverse('admin_index'))  # Redirect to home or any appropriate URL

# Add a view for the alumni profile if it doesn't exist
@login_required
def alumni_profile(request, alumni_id):
    try:
        alumni_profile = Alumni.objects.get(id=alumni_id, user=request.user)
        student_profile = StudentProfile.objects.get(user=request.user)  # Assuming user is linked to StudentProfile
        return render(request, 'admin/alumni/alumni_profile.html', {'alumni_profile': alumni_profile, 'student_profile': student_profile})
    except Alumni.DoesNotExist:
        messages.error(request, 'Alumni profile not found.')
        return redirect(reverse('admin_index'))


from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import ResumeBuilder  # Import the ResumeBuilder model

def generate_pdf(request):
    # Fetch the latest data from the ResumeBuilder model
    resume_data = ResumeBuilder.objects.latest('id')

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="sample.pdf"'

    # Create the PDF content
    p = canvas.Canvas(response)

    # Populate the PDF with data from the ResumeBuilder model
    p.drawString(100, 800, f"Name: {resume_data.name}")
    p.drawString(100, 780, f"About: {resume_data.about}")
    p.drawString(100, 760, f"Age: {resume_data.age}")
    p.drawString(100, 740, f"Email: {resume_data.email}")
    p.drawString(100, 720, f"Phone: {resume_data.phone}")

    # Skills
    p.drawString(100, 700, f"Skills:")
    p.drawString(120, 680, f"1. {resume_data.skill1}")
    p.drawString(120, 660, f"2. {resume_data.skill2}")
    p.drawString(120, 640, f"3. {resume_data.skill3}")
    p.drawString(120, 620, f"4. {resume_data.skill4}")
    p.drawString(120, 600, f"5. {resume_data.skill5}")

    # Education
    p.drawString(100, 580, f"Education:")
    p.drawString(120, 560, f"{resume_data.degree1}, {resume_data.college1}, {resume_data.year1}")
    p.drawString(120, 540, f"{resume_data.degree2}, {resume_data.college2}, {resume_data.year2}")
    p.drawString(120, 520, f"{resume_data.degree3}, {resume_data.college3}, {resume_data.year3}")

    # Languages
    p.drawString(100, 500, f"Languages:")
    p.drawString(120, 480, f"1. {resume_data.lang1}")
    p.drawString(120, 460, f"2. {resume_data.lang2}")
    p.drawString(120, 440, f"3. {resume_data.lang3}")

    # Projects
    p.drawString(100, 420, f"Projects:")
    p.drawString(120, 400, f"{resume_data.project1}, {resume_data.durat1}")
    p.drawString(120, 380, f"{resume_data.desc1}")
    p.drawString(120, 360, f"{resume_data.project2}, {resume_data.durat2}")
    p.drawString(120, 340, f"{resume_data.desc2}")

    # Work Experience
    p.drawString(100, 320, f"Work Experience:")
    p.drawString(120, 300, f"{resume_data.company1}, {resume_data.post1}, {resume_data.duration1}")
    p.drawString(120, 280, f"{resume_data.lin11}")
    p.drawString(120, 260, f"{resume_data.company2}, {resume_data.post2}, {resume_data.duration2}")
    p.drawString(120, 240, f"{resume_data.lin21}")

    # Achievements
    p.drawString(100, 220, f"Achievements:")
    p.drawString(120, 200, f"1. {resume_data.ach1}")
    p.drawString(120, 180, f"2. {resume_data.ach2}")
    p.drawString(120, 160, f"3. {resume_data.ach3}")

    # Close the PDF object cleanly, and return the response
    p.showPage()
    p.save()

    return response


from .models import BlogContent

def create_blog_content(request, alumni_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        # Get the alumni instance based on the provided ID or return 404 if not found
        alumni_instance = get_object_or_404(Alumni, id=alumni_id)
        
        # Create a new BlogContent instance with the retrieved alumni instance
        blog_content = BlogContent.objects.create(title=title, content=content, image=image, alumni=alumni_instance)

        # Redirect to a success page or do other actions
        return redirect('display_blog_content', alumni_id=alumni_id)

    return render(request, 'admin/alumni/blogform.html', {'alumni_id': alumni_id})

from django.shortcuts import render, get_object_or_404
from .models import BlogContent, Alumni

def display_blog_content(request, alumni_id):
    if request.user.is_authenticated:
        try:
            # Get the alumni instance based on the provided ID or return 404 if not found
            alumni_instance = get_object_or_404(Alumni, id=alumni_id)
            # Ensure the alumni_instance contains the profile_photo attribute
            if not hasattr(alumni_instance, 'profile_photo'):
                raise AttributeError("Alumni instance does not have 'profile_photo' attribute.")
            # Filter blog contents based on the retrieved alumni instance
            blog_contents = BlogContent.objects.filter(alumni=alumni_instance)
            return render(request, 'admin/alumni/bloglist.html', {'alumni_instance': alumni_instance, 'blog_contents': blog_contents})
        except Alumni.DoesNotExist:
            messages.error(request, 'Alumni profile not found.')
            return redirect(reverse('admin_index'))
    else:
        return redirect('loginn')
    
from django.shortcuts import render, get_object_or_404
from .models import BlogContent, StudentProfile

def alumni_blog(request, studentprofile_id):
    # Fetch data from BlogContent and StudentProfile models
    blog_contents = BlogContent.objects.filter(is_approved=True)
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    
    user = studentprofile.user
    alumni = None
    try:
        alumni = user.alumni  # Fetch Alumni object associated with User
    except AttributeError:
        pass  # Alumni attribute does not exist on User object
    except user.alumni.RelatedObjectDoesNotExist:
        pass  # Alumni object does not exist

    context = {
        'blog_contents': blog_contents,
        'studentprofile': studentprofile,
        'alumni': alumni,  # Pass Alumni object to context
    }

    return render(request, 'admin/alumni/alumni_blog.html', context)



from .models import Interview  # Import the Interview model

from django.contrib.auth.decorators import login_required

@login_required
def sinter(request, studentprofile_id):
    try:
        studentprofile = StudentProfile.objects.get(id=studentprofile_id)
    except StudentProfile.DoesNotExist:
        return HttpResponse("Student profile does not exist", status=404)

    # Retrieve AptdResult details related to the studentprofile_id
    aptd_results = AptdResult.objects.filter(student_id=studentprofile_id)

    # Retrieve interviews related to the AptdResult objects
    interviews = Interview.objects.filter(shortlist__in=aptd_results)

    if aptd_results.exists():
        company_profile = aptd_results.first().company_id
    else:
        # Handle the case where no AptdResult objects are found
        company_profile = None

    context = {
        'studentprofile': studentprofile,
        'aptd_results': aptd_results,
        'company_profile': company_profile,
        'interviews': interviews,  # Pass the interviews to the template context
    }
    return render(request, 'student/interview.html', context)




# def apt_notification(request, studentprofile_id):
#     # Your logic to fetch the student profile based on the studentprofile_id
#     studentprofile = StudentProfile.objects.get(id=studentprofile_id)
    
#     # Retrieve instances of AddAptitude where status is True
#     filtered_aptitudes = AddAptitude.objects.filter(is_approved=True)
    
#     # Pass the studentprofile and filtered_aptitudes to the template context
#     context = {
#         'studentprofile': studentprofile,
#         'filtered_aptitudes': filtered_aptitudes,
        
#     } 
#     return render(request, 'student/apt_notification.html', context)

from django.shortcuts import get_object_or_404

def apt_notification(request, studentprofile_id):
    try:
        # Fetch the student profile based on the studentprofile_id
        studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
        
        # Check if the student has any job applications
        job_applications = JobApplication.objects.filter(stuprof=studentprofile)
        
        if job_applications.exists():
            # Retrieve the job IDs for which the student has applied
            job_ids = job_applications.values_list('job_id', flat=True)
            
            # Retrieve aptitude notifications related to the jobs applied by the student
            # filtered_aptitudes = AddAptitude.objects.filter(job__id__in=job_ids, is_approved=True)
            filtered_aptitudes = AddAptitude.objects.filter(is_approved=True)
            # Pass the student profile and filtered aptitudes to the template context
            context = {
                'studentprofile': studentprofile,
                'filtered_aptitudes': filtered_aptitudes,
            } 
            return render(request, 'student/apt_notification.html', context)
        else:
            # Handle the case where the student has not applied for any jobs
            return HttpResponse("You haven't applied for any jobs yet.")
    except StudentProfile.DoesNotExist:
        # Handle the case where the student profile does not exist
        return HttpResponse("Student profile does not exist.")


from .models import JobApplication


@login_required  # Ensure user is logged in to access this view
def apt_list_company(request):
    # Fetch the company profile related to the logged-in user
    company_profile = CompanyProfile.objects.get(user=request.user)

    # Filter aptitudes based on the company_profile
    filtered_aptitudes = AddAptitude.objects.filter(company_profile=company_profile, status=True)

    return render(request, 'company/apt_list.html', {'filtered_aptitudes': filtered_aptitudes})


from .forms import AptitudeTestForm  # Create a form for conducting aptitude tests



from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

# def conduct_aptitude_test(request):
#     if request.method == 'POST':
#         exam_schedule_id = request.POST.get('exam_schedule')
#         try:
#             exam_schedule = ExamSchedule.objects.get(id=exam_schedule_id)
#         except ExamSchedule.DoesNotExist:
#             return HttpResponseNotFound("Exam Schedule does not exist.")

#         question_count = int(request.POST.get('question_count'))

#         for i in range(1, question_count + 1):
#             question_text = request.POST.get(f'question{i}')
#             question = Question.objects.create(exam_schedule=exam_schedule, question_text=question_text)

#             for j in range(1, 5):
#                 option_text = request.POST.get(f'question{i}_option{j}')
#                 is_correct = (j == int(request.POST.get(f'question{i}_answer')))
#                 Option.objects.create(question=question, option_text=option_text, is_correct=is_correct)

#         return redirect('cfirstround', exam_schedule_id=exam_schedule_id)
#     else:
#         # Fetch all exam schedules to populate the dropdown
#         exam_schedules = ExamSchedule.objects.all()
#         return render(request, 'company/create_apt.html', {'exam_schedules': exam_schedules})

# def conduct_aptitude_test(request):
#     return render(request, 'company/create_apt.html')

def conduct_aptitude_test(request):
    # Retrieve CompanyProfile data
    company_profiles = CompanyProfile.objects.all()  # You can filter this queryset as needed

    # Pass CompanyProfile data to the template context
    context = {
        'company_profiles': company_profiles,
    }

    return render(request, 'company/create_apt.html', context)

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
@login_required
def q_preview(request):
    # Retrieve the company profile associated with the logged-in user
    company_profile = request.user.companyprofile

    # Retrieve questions associated with the company profile
    questions = Questionn.objects.filter(company_profile=company_profile, status=True)

    # Calculate the sum of marks of the questions
    total_marks = questions.aggregate(total_marks=Sum('marks'))['total_marks']

    # Print out the total marks for debugging
    print("Total Marks:", total_marks)

    return render(request, 'company/q_preview.html', {'questions': questions, 'total_marks': total_marks})



@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Questionn, pk=question_id)
    if request.method == 'POST':
        # Update the question fields with the submitted data
        question.exam_title = request.POST.get('exam_title')
        # question.company_name = request.POST.get('company_name')
        question.question = request.POST.get('question')
        question.option1 = request.POST.get('option1')
        question.option2 = request.POST.get('option2')
        question.option3 = request.POST.get('option3')
        question.option4 = request.POST.get('option4')
        question.correct_option = request.POST.get('correct_option')
        question.marks = request.POST.get('marks')  # Update marks value
        question.save()
        return redirect('q_preview')  # Redirect to the question list page
    return render(request, 'company/edit_question.html', {'question': question})


def delete_question(request, question_id):
    question = get_object_or_404(Questionn, pk=question_id)
    # Update the status of the question
    question.status = False  # Set status to False to indicate it's not active
    question.save()
    return redirect('q_preview')

from django.shortcuts import render, redirect
from .models import Questionn

# def create_question(request):
#     if request.method == 'POST':

#         exam_title = request.POST.get('exam_title')
       
#         question = request.POST.get('question')
#         option1 = request.POST.get('option1')
#         option2 = request.POST.get('option2')
#         option3 = request.POST.get('option3')
#         option4 = request.POST.get('option4')
#         correct_option = request.POST.get('correct_option')
#         # status = request.POST.get('status') == 'on'  # Convert checkbox value to boolean

#         # Create a new Questionn instance
#         questionn = Questionn.objects.create(
#             exam_title=exam_title,
           
#             question=question,
#             option1=option1,
#             option2=option2,
#             option3=option3,
#             option4=option4,
#             correct_option=correct_option,
#             # company_profile_id=companyprofile_id
#             # status=status
#         )

#         # Redirect to a success page or any other page
#         return redirect('conduct_aptitude_test')
#     else:
#         # Render the form template
#         return redirect('conduct_aptitude_test')
@login_required
def create_question(request):
    if request.method == 'POST':
        # Retrieve the company profile associated with the logged-in user
        company_profile = request.user.companyprofile
        
        # Retrieve form data including marks
        exam_title = request.POST.get('exam_title')
        question_text = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')
        correct_option = request.POST.get('correct_option')
        marks = request.POST.get('marks')  # Retrieve marks from the form

        # Create a new Question instance associated with the company profile
        question = Questionn.objects.create(
            exam_title=exam_title,
            company_profile=company_profile,  # Associate with the logged-in company profile
            question=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_option=correct_option,
            marks=marks,  # Save marks along with the question
        )

        # Redirect to a success page or any other page
        return redirect('conduct_aptitude_test')
    else:
        # Render the form template
        return redirect('conduct_aptitude_test')
@login_required

def attend_exam(request, studentprofile_id, company_profile_id):
    try:
        # Fetch the student profile
        student_profile = StudentProfile.objects.get(id=studentprofile_id)

        # Fetch the company profile associated with the student profile
        comp_prof = CompanyProfile.objects.get(id=company_profile_id)

        # Get the company's aptitude IDs
        company_aptitude_ids = AddAptitude.objects.filter(company_profile=comp_prof).values_list('company_profile', flat=True)

        # Fetch questions associated with the company profile
        questions = Questionn.objects.filter(company_profile_id__in=company_aptitude_ids, status=True)

        # Calculate total marks obtained by the student
        total_marks = ExamResponse.objects.filter(student=student_profile, company=comp_prof).aggregate(total_marks=Sum('marks'))['total_marks'] or 0

        return render(request, 'student/attend_test.html', {'questions': questions, 'studentprofile_id': studentprofile_id, 'company_profile_id': company_profile_id, 'company_profile': comp_prof, 'total_marks': total_marks})
    except (Questionn.DoesNotExist, CompanyProfile.DoesNotExist):
        questions = None
        return render(request, 'student/attend_test.html', {'questions': questions, 'studentprofile_id': studentprofile_id, 'company_profile_id': company_profile_id})

from .models import ResultAptitude

def store_result(student_profile, comp_prof, total_marks):
    ResultAptitude.objects.create(student=student_profile, company=comp_prof, total_marks=total_marks)


from django.shortcuts import render, redirect

from .models import ExamResponse, Question
from django.http import HttpResponseBadRequest

from .models import ExamResponse

from django.shortcuts import redirect
from .models import ExamResponse, Questionn



def submit_exam(request):
    if request.method == 'POST':
        # Extract data from the POST request
        question_id = request.POST.get('question_id')
        selected_option = request.POST.get('answer')
        student_profile_id = request.POST.get('studentprofile_id')
        company_profile_id = request.POST.get('company_profile_id')

        # Validate the question ID
        question = Questionn.objects.get(pk=question_id)
        
        # Calculate marks based on the correctness of the selected option
        if selected_option == str(question.correct_option):
            marks = question.marks
        else:
            marks = 0.0  # Set marks to 0 if the selected option is incorrect

        # Get the current student (assuming the user is authenticated)
        student = request.user.studentprofile  # Adjust this according to your actual model structure
        
        # Create an instance of ExamResponse
        exam_response = ExamResponse.objects.create(
            student=student,
            question=question,
            company_id=company_profile_id,
            selected_option=selected_option,
            marks=marks  # Store the calculated marks
        )

        # Redirect to the confirmation page or any other page
        return redirect('attend_exam', studentprofile_id=student.id, company_profile_id=company_profile_id)
        
    else:
        # Handle GET requests or other HTTP methods
        return redirect('error')





from django.core.serializers import serialize
import json

@csrf_exempt
def quiz_form(request):
    
    if request.method == 'POST':
        try:
            # Check if the form is for updating an existing question
            question_id = request.POST.get('question_id')
            if question_id:
                question = Question.objects.get(pk=question_id)
                question.title = request.POST.get('question-title')
                question.save()

                # Delete existing options for the question
                question.options.all().delete()

                # Update options for the question
                for key, value in request.POST.items():
                    if key.startswith('option-'):
                        option = Option(question=question, text=value)
                        option.save()
                        is_correct = request.POST.get('marked')

                        option.is_correct = 1 if key.endswith(is_correct) else 0
                        option.save()


                return JsonResponse({'success': True})
            # If it's a new question, create it
            else:
                question_title = request.POST.get('question-title')
                new_question = Question.objects.create(title=question_title)
                for key, value in request.POST.items():
                    if key.startswith('option-'):
                        is_correct = request.POST.get('marked')
                        Option.objects.create(
                            question=new_question,
                            text=value,
                            is_correct=1 if key.endswith(is_correct) else 0
                        )
                return redirect('quiz_form')
        except Exception as e:
            print(f"Error in quiz_form view (Form Submission): {e}")
            return render(request, 'company/cfirstround.html', {'error_message': f'An error occurred: {e}'})
    
    # Fetch existing questions for the course
    questions = Question.objects.all()
    
    # Serialize questions and options to JSON
    questions_json = json.dumps([
        {
            'pk': q.pk,
            'title': q.title,
            'options': [{'pk': option.pk, 'text': option.text, 'is_correct': option.is_correct} for option in q.options.all()]
        }
        for q in questions
    ])
    # print(course.id)
    return render(request, 'company/set_question.html', {'questions': questions,'questions_json' : questions_json})




def list_questions_and_answers(request, exam_schedule_id):
    exam_schedule = get_object_or_404(ExamSchedule, id=exam_schedule_id)
    questions = exam_schedule.question_set.all()  # Assuming a reverse relation from ExamSchedule to Question model
    context = {
        'exam_schedule': exam_schedule,
        'questions': questions,
    }
    return render(request, 'company/list_questions_and_answers.html', context)

def schedule_exam(request,exam_schedule_id):
    exam_schedule = ExamSchedule.objects.get(pk=exam_schedule_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            question_text = form.cleaned_data['question_text']
            option1_text = form.cleaned_data['option1']
            option2_text = form.cleaned_data['option2']
            option3_text = form.cleaned_data['option3']
            option4_text = form.cleaned_data['option4']
            correct_option_index = int(form.cleaned_data['correct_option'])
            
            # Create the question
            question = Question.objects.create(exam_schedule=exam_schedule, question_text=question_text)
            
            # Create options
            options_data = [
                (option1_text, 1),
                (option2_text, 2),
                (option3_text, 3),
                (option4_text, 4)
            ]
            for option_text, option_index in options_data:
                is_correct = (option_index == correct_option_index)
                Option.objects.create(question=question, option_text=option_text, is_correct=is_correct)
            
            # Redirect to a success page or another view
            return redirect('success_page')  # Replace 'success_page' with the actual URL name of your success page
    else:
        form = QuestionForm()
    
    context = {
        'form': form,
        'exam_schedule': exam_schedule,
    }
    return render(request, 'company/create_apt.html', context)

def error(request):
    return render(request,'error.html')

# new

def save_quiz(request):
    if request.method == 'POST':
        quiz_title = request.POST.get('quiz_title')
        questions_count = int(request.POST.get('question_count'))

        # Create a new Quiz instance
        quiz = Quiz3.objects.create(title=quiz_title)

        for question_number in range(1, questions_count + 1):
            question_text = request.POST.get(f'question{question_number}')
            question = Question.objects.create(quiz=quiz, text=question_text)

            for option_number in range(1, 5):
                option_text = request.POST.get(f'question{question_number}_option{option_number}')
                is_correct = request.POST.get(f'question{question_number}_answer') == str(option_number)
                Option.objects.create(question=question, text=option_text, is_correct=is_correct)

        return render(request, 'company/create_apt.html')  # Redirect or render success page
    else:
        return render(request, 'error.html')  # Handle non-POST requests










def ad_alumniblog(request):
    blog_contents = BlogContent.objects.all()
    return render(request, 'admin/alumni/ad_alumninote.html', {'blog_contents': blog_contents})

def payconfirm(request, content_id, studentprofile_id=None):
    # Your existing code to retrieve studentprofile and content_instance
    studentprofile = None
    if studentprofile_id:
        studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    content_instance = get_object_or_404(ccontent, id=content_id)

    # Razorpay payment details
    currency = 'INR'
    amount = int(content_instance.price)*100  # Rs. 200
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # Pass Razorpay payment details to the template
    context = {
        'studentprofile': studentprofile,
        'content_instance': content_instance,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
    }

    return render(request, 'admin/resources/payconfirm.html', context)

from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
 
 
# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
 
            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:
 
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
 
                    # render success page on successful caputre of payment
                    return render(request, 'admin/resources/scontent2list.html')
                except:
 
                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:
 
                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
from django.shortcuts import render, get_object_or_404
from .models import ccontent

def content_details(request):
    # Get the content ID from the query parameter in the URL
    content_id = request.GET.get('id')
    content_name = request.GET.get('cname')
    
    # Retrieve content details based on the content ID (Replace this with your logic)
    content = get_object_or_404(ccontent, id=content_id)
    
    # Retrieve reviews related to the content
    reviews = Review.objects.filter(prod=content_id)
    
    # Render the content details page with the retrieved content details and reviews
    return render(request, 'contentmore.html', {'content': content, 'reviews': reviews})

from .models import Review
# import nltk
# nltk.download('vader_lexicon')
# from nltk.sentiment import SentimentIntensityAnalyzer
# def submit_review(request):
#     if request.method == 'POST':
#         prod = request.POST.get('content_id')
#         print(prod)
#         prod = ccontent.objects.get(id=prod)
#         description = request.POST.get('comment')
#         sentiment_analyzer = SentimentIntensityAnalyzer()
#         sentiment_score = sentiment_analyzer.polarity_scores(description)['compound']
#         print("Sentiment Score:", sentiment_score)
#         # studentprofile = request.user.studentprofile
#         # Calculate the rating based on the number of stars selected
#         rating = int(request.POST.get('rating', 0))

#         # Create a new review associated with the product and the authenticated user
#         Review.objects.create(
#             user=request.user,
#             description=description,
#             sentiment_score=sentiment_score,
#             prod=prod,
#             # studentprofile=studentprofile,
#         )
        
#         # Redirect to a success page or the product detail page
#         return redirect('content_details')
    
def bloglist2(request, alumni_id):
    alumni_instance = get_object_or_404(Alumni, id=alumni_id)

    return render(request,'admin/alumni/bloglist2.html', {'alumni_instance': alumni_instance})

def dlt_blog(request, id):  # Use the same parameter name as in the URL pattern
    if request.method == 'GET':
        adcont_instance = get_object_or_404(BlogContent, id=id)
        adcont_instance.delete()
        return redirect('display_blog_content')
    

from django.utils import timezone

def eventform(request, alumni_id):
    alumni_instance = get_object_or_404(Alumni, id=alumni_id)

    if request.method == 'POST':
        # Process the form data here
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        image = request.FILES.get('image')
        event_type = request.POST.get('event_type')
        link = request.POST.get('link')
        
        # Create a new Event object and set its status to True
        event = AlumniEvent(
            title=title,
            description=description,
            date=date,
            image=image,
            event_type=event_type,
            link=link,
            status=True,  # Set the status to True
            alumni=alumni_instance  # Associate the event with the corresponding alumni
        )
        event.save()
        
        # Update event statuses
        update_event_status()
        
        # Redirect to a success page or wherever you want
        return redirect(reverse('eventform', kwargs={'alumni_id': alumni_id}))        
    else:
        return render(request, 'admin/alumni/eventform.html', {'alumni_instance': alumni_instance})


from django.contrib.auth.decorators import login_required

@login_required
def company_event_form(request):
    company_profile = CompanyProfile.objects.get(user=request.user)
    if request.method == 'POST':
        # Process the form data here
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        image = request.FILES.get('image')
        event_type = request.POST.get('event_type')
        link = request.POST.get('link')
        
        # Retrieve the CompanyProfile associated with the logged-in user
        company_profile = request.user.companyprofile
        
        # Create a new CompanyEvent object associated with the CompanyProfile
        event = CompanyEvent(
            title=title,
            description=description,
            date=date,
            image=image,
            event_type=event_type,
            link=link,
            company=company_profile  # Associate the CompanyProfile with the CompanyEvent
        )
        event.save()
        
        # Redirect to a success page or wherever you want
        return redirect(reverse('company_event_form'))  # Replace 'event_list' with the URL name of your event list page        
    else:
        return render(request, 'company/ceventform.html')


from .models import Event

def sevent(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    
    # Fetch events associated with the student profile and with status=True
    events = AlumniEvent.objects.filter(status=True)
    
    return render(request, 'admin/student/alumni_events.html', {'studentprofile': studentprofile, 'events': events})


def scevent(request, studentprofile_id):
    studentprofile = get_object_or_404(StudentProfile, id=studentprofile_id)
    
    # Fetch events associated with the student profile and with status=True
    events = CompanyEvent.objects.filter(status=True)
    
    return render(request, 'student/companyevents.html', {'studentprofile': studentprofile, 'events': events})


# 
from datetime import date

def editevent(request, alumni_id, event_id):
    # Retrieve the alumni instance
    alumni_instance = get_object_or_404(Alumni, id=alumni_id)

    # Retrieve the specific event instance
    event = get_object_or_404(AlumniEvent, id=event_id)

    if request.method == 'POST':
        # Retrieve the form data from the request
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        image = request.FILES.get('image') if 'image' in request.FILES else None
        event_type = request.POST.get('event_type')
        link = request.POST.get('link')
        
        # Update the event fields
        event.title = title
        event.description = description
        event.date = date
        if image:
            event.image = image
        event.event_type = event_type
        event.link = link
        # Save the updated event to the database
        event.save()
        
        # Redirect to the eventlist view or another page
        return redirect('eventlist', alumni_id=alumni_id)
    
    return render(request, 'admin/alumni/editevent.html', {'alumni_instance': alumni_instance, 'event': event})


def edit_company_event(request, event_id):
    # Fetch the event object
    event = get_object_or_404(CompanyEvent, pk=event_id)

    if request.method == 'POST':
        # Process the form data here
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        image = request.FILES.get('image')
        event_type = request.POST.get('event_type')
        link = request.POST.get('link')
        
        # Update the event object with new data
        event.title = title
        event.description = description
        event.date = date
        if image:
            event.image = image
        event.event_type = event_type
        event.link = link
        event.save()
        
        # Redirect to a success page or wherever you want
        return redirect('company_event_form')  # Assuming 'company_event_form' is the URL name of your form page
    else:
        # Render the edit form with the event data pre-filled
        return render(request, 'company/editcevent.html', {'event': event})
def ceventlist(request):
    company_profile = CompanyProfile.objects.get(user=request.user)
    events = CompanyEvent.objects.filter(status=True)
    return render(request,'company/ceventlist.html',{'events': events,'company_profile':company_profile})

from datetime import datetime


def eventlist(request, alumni_id):
    alumni_instance = get_object_or_404(Alumni, id=alumni_id)
    events = AlumniEvent.objects.filter(alumni=alumni_instance, status=True)  # Filter by status=1
    
    # Check event dates and update status accordingly
    current_date = datetime.now().date()
    for event in events:
        if event.date < current_date:  # Check if the event date is in the past
            event.status = False  # Set status to False (0)
            event.save()  # Save the updated event
    
    return render(request, 'admin/alumni/eventlist.html', {'alumni_instance': alumni_instance,'events': events,'alumni_id': alumni_id})







from django.utils import timezone

def update_event_status():
    today = timezone.now().date()
    events_to_update = Event.objects.filter(date__lt=today)
    events_to_update.update(status=False)

def delete_event(request):
    event_id = request.POST.get('event_id')
    
    try:
        event = Event.objects.get(id=event_id)
        # Instead of deleting the event, set its status to False (0)
        event.status = False
        event.save()
        return JsonResponse({'success': True})
    except Event.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Event does not exist'})

def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            return JsonResponse({'success': True})
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    

def delete_blog_content(request, content_id):
    if request.method == 'POST':
        # Retrieve the BlogContent instance
        blog_content = get_object_or_404(BlogContent, pk=content_id)
        # Delete the instance
        blog_content.delete()
        # Redirect to a success page or wherever you want
        return redirect('success_url_name')
    else:
        # Handle GET request if necessary
        pass

def import_excel_data(file_path):
    try:
        # Read the Excel file using pandas
        excel_data = pd.read_csv(file_path)

        # Iterate through each row in the DataFrame
        for index, row in excel_data.iterrows():
            # Check if a record with the same admission_no already exists
            if not ExcelData.objects.filter(admission_no=row['admission_no']).exists():
                # Create an instance of ExcelData model and assign values from the DataFrame
                excel_entry = ExcelData(
                    admission_no=row['admission_no'],
                    email=row['email'],
                    phone=row['phone'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    status=False  # Assuming all entries are initially set to False (Pending)
                )
                # Save the ExcelData instance to the database
                excel_entry.save()

        print("Data imported successfully.")
    except Exception as e:
        print(f"Error occurred while importing data: {str(e)}")

import pandas as pd
def import_excel_data_view(request):
    data_list = None  # Initialize data_list as None

    if request.method == 'POST':
        file = request.FILES.get('excel_file')
        if file:
            try:
                # Read the Excel file using pandas
                excel_data = pd.read_csv(file)

                # Initialize an empty list to store ExcelData objects
                data_list = []

                # Iterate through each row in the DataFrame
                for index, row in excel_data.iterrows():
                    # Create an instance of ExcelData model and assign values from the DataFrame
                    excel_entry = ExcelData(
                        admission_no=row['admission_no'],
                        email=row['email'],
                        phone=row['phone'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        status=False  # Assuming all entries are initially set to False (Pending)
                    )
                    # Append the ExcelData instance to the data_list
                    data_list.append(excel_entry)

                # Save all ExcelData instances to the database
                ExcelData.objects.bulk_create(data_list)

                # Fetch all ExcelData objects from the database
                data_list = ExcelData.objects.all()

            except Exception as e:
                # Print the exception message for debugging
                print(e)

    return render(request, 'exceldata.html', {'data_list': data_list})

from django.shortcuts import render, redirect
from .models import Question

def exam_view(request):
    question = Questionn.objects.first()  # Get the first question for now, you can implement logic to fetch random questions
    return render(request, 'company/setq.html', {'question': question})

def save_and_next(request):
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_option = request.POST.get('option')
        # Save the answer to the database or perform any other necessary actions
        # For demonstration purpose, let's assume you save it to the session
        request.session[f'question_{question_id}_answer'] = selected_option
    return redirect('exam')

def apt_approve(request):
    aptitudes = AddAptitude.objects.all()
    context = {'aptitudes': aptitudes}
    print(context)  # Add this line for debugging
    return render(request, 'admin/alumni/apt_approve.html', context)

def approved_aptitude(request, aptitude_id):
    # approveapt = get_object_or_404(AddAptitude, id=aptitude_id)
    aptitude = get_object_or_404(AddAptitude, aptitude=aptitude_id)
    aptitude.is_approved = True
    aptitude.save()       
        # Redirect back to the list of approved appointments
    return redirect('apt_approve')


def admin_cevent(request):
    cevent = CompanyEvent.objects.all()
    context = {'cevent': cevent}
    return render(request, 'admin/companyevents.html', context)


def alumni_job_approve(request):
    jobopen = BlogContent.objects.all()
    context = {'jobopen': jobopen}
    return render(request, 'admin/alumni/alumni_job_approve.html', context)

def approved_alumnijob(request, blog_id):
    alumnijob = get_object_or_404(BlogContent, id=blog_id)
    alumnijob.is_approved = True
    alumnijob.save()
    return redirect('alumni_job_approve')

from .models import ExamResponse

def test_response(request):
    company_id = request.user.companyprofile.id  

    exam_responses = ExamResponse.objects.filter(company_id=company_id)
    
    context = {'exam_responses': exam_responses}
    
    return render(request, 'company/test_response.html', context)

# def test_result(request):
#     # Assuming you have calculated total_marks correctly in your view
#     total_marks = 7  # Replace this with the actual calculation of total marks
    
#     # Assuming you have retrieved exam_responses from the database
#     exam_responses = ExamResponse.objects.all()  # Replace this with your actual queryset
#     total_marks_by_student = exam_responses.values('student__user__first_name', 'student__user__last_name', 'student__user__email', 'student__department', 'student__phone').annotate(total_marks=Sum('marks'))

#     return render(request, 'company/test_result.html', {'total_marks_by_student': total_marks_by_student})

from django.db.models import Sum
from django.shortcuts import render

def test_result(request):
    # Retrieve the cutoff mark from the GET request; default to None if not provided
    cutoff_mark = request.GET.get('cutoff_mark', None)
    try:
        cutoff_mark = float(cutoff_mark) if cutoff_mark is not None else None
    except ValueError:
        cutoff_mark = None  # In case of invalid input, ignore the cutoff
    company_id = request.user.companyprofile
    # Assuming exam_responses are retrieved as before
    exam_responses_query = ExamResponse.objects.filter(company_id=company_id).values(
        'student_id',
        'student__user__first_name',
        'student__user__last_name',
        'student__user__email',
        'student__department',
        'student__phone'
    ).annotate(total_marks=Sum('marks'))
    
    # If a valid cutoff mark is provided, filter the queryset accordingly
    if cutoff_mark is not None:
        exam_responses_query = exam_responses_query.filter(total_marks__gte=cutoff_mark)
    for response in exam_responses_query:
        student_id = response['student_id']
        student_first_name = response['student__user__first_name']
        student_last_name = response['student__user__last_name']
        student_email = response['student__user__email']
        student_department = response['student__department']
        student_phone = response['student__phone']
        total_marks = response['total_marks']

        # Check if the entry already exists
        existing_entry = AptdResult.objects.filter(
            student_id=student_id,
            student_first_name=student_first_name,
            student_last_name=student_last_name,
            student_email=student_email,
            student_department=student_department,
            student_phone=student_phone,
            total_marks=total_marks,
            company_id=company_id
        ).exists()

        if not existing_entry:
            student_profile = StudentProfile.objects.get(id=student_id)
            # Create AptdResult instance
            AptdResult.objects.create(
                student_id=student_profile,
                student_first_name=student_first_name,
                student_last_name=student_last_name,
                student_email=student_email,
                student_department=student_department,
                student_phone=student_phone,
                total_marks=total_marks,
                company_id=company_id
            )

    return render(request, 'company/test_result.html', {
        'total_marks_by_student': exam_responses_query,
        'cutoff_mark': cutoff_mark,  # Pass the cutoff mark to the template, even if it's None
        'company_id': company_id, 
    })


def shortlist2(request):
    company_id = request.user.companyprofile.id  # Assuming you can access the company profile associated with the logged-in user
    aptd_results = AptdResult.objects.filter(company_id=company_id, status=True)
    return render(request, 'company/shortlist2.html', {'aptd_results': aptd_results})

from datetime import datetime

from .models import ShortlistedStudent

from django.http import HttpResponseNotFound

from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from .models import AptdResult

from django.shortcuts import redirect, HttpResponse
from django.contrib import messages
from .models import AptdResult

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import AptdResult, Interview

# def schedule_interview(request):
#     if request.method == 'POST':
#         # Extract form data
#         student_id = request.POST.get('student_id')
#         interview_date = request.POST.get('interview_date')
#         interview_time = request.POST.get('interview_time')
#         ampm = request.POST.get('ampm')
#         interview_type = request.POST.get('interview_type')
#         interview_mode = request.POST.get('interview_mode')
#         interview_link_location = request.POST.get('interview_link_location')
#         interview_duration = request.POST.get('interview_duration')
#         interviewer_info = request.POST.get('interviewer_info')
#         instruction_requirements = request.FILES.get('instruction_requirements')
        
#         try:
#             # Get the student object with the provided ID
#             student = AptdResult.objects.get(id=student_id)
            
#             # Get the company profile
#             company = request.user.companyprofile

#             # Create the Interview object and associate it with the student
#             interview = Interview.objects.create(
#                 # student=student,  # Use the AptdResult object directly
#                 shortlist=AptdResult.objects.get(id=student_id),
#                 company=company,
#                 interview_date=interview_date,
#                 interview_time=interview_time,
#                 ampm=ampm,
#                 interview_type=interview_type,
#                 interview_mode=interview_mode,
#                 interview_link_location=interview_link_location,
#                 interview_duration=int(interview_duration),
#                 interviewer_info=interviewer_info,
#                 instruction_requirements=instruction_requirements
#             )

#             # Optionally, you can add a success message
#             messages.success(request, 'Interview scheduled successfully.')

#             # Redirect to a success page or the same page
#             return redirect('shortlist2')  # Redirect to the interview list page
        
#         except AptdResult.DoesNotExist:
#             # Handle the case where the AptdResult object does not exist
#             return HttpResponse("The specified student does not exist.")

#     else:
#         # Handle GET requests if needed
#         pass

def schedule_interview(request):
    if request.method == 'POST':
        # Extract form data
        student_id = request.POST.get('student_id')
        interview_date = request.POST.get('interview_date')
        interview_time = request.POST.get('interview_time')
        ampm = request.POST.get('ampm')
        interview_type = request.POST.get('interview_type')
        interview_mode = request.POST.get('interview_mode')
        interview_link_location = request.POST.get('interview_link_location')
        interview_duration = request.POST.get('interview_duration')
        interviewer_info = request.POST.get('interviewer_info')
        instruction_requirements = request.FILES.get('instruction_requirements')
        
        try:
            # Get the AptdResult object with the provided ID
            aptd_result = AptdResult.objects.get(id=student_id)
            
            # Get the company profile
            company = request.user.companyprofile

            # Create the Interview object and associate it with the AptdResult object
            interview = Interview.objects.create(
                shortlist=aptd_result,  # Associate it directly with the AptdResult object
                company=company,
                interview_date=interview_date,
                interview_time=interview_time,
                ampm=ampm,
                interview_type=interview_type,
                interview_mode=interview_mode,
                interview_link_location=interview_link_location,
                interview_duration=int(interview_duration),
                interviewer_info=interviewer_info,
                instruction_requirements=instruction_requirements
            )

            # Optionally, you can add a success message
            messages.success(request, 'Interview scheduled successfully.')

            # Redirect to a success page or the same page
            return redirect('shortlist2')  # Redirect to the interview list page
        
        except AptdResult.DoesNotExist:
            # Handle the case where the AptdResult object does not exist
            return HttpResponse("The specified student does not exist.")

    else:
        # Handle GET requests if needed
        pass


from django.shortcuts import render
from .models import Interview


def get_interview_details(request):
    if request.method == 'GET':
        student_id = request.GET.get('student_id')
        try:
            interview_details = Interview.objects.get(shortlist_id=student_id)
        except Interview.DoesNotExist:
            interview_details = None
        
        return render(request, 'company/shortlist2.html', {'interview_details': interview_details})






def get_student_profile(user):
    try:
        return StudentProfile.objects.get(user=user)
    except StudentProfile.DoesNotExist:
        # Handle the case where the student profile does not exist for the user
        return None
    
# Import necessary modules if required
from .models import CompanyProfile  # Import your CompanyProfile model if needed

# Define the get_company_profile function
def get_company_profile(company_id):
    try:
        # Retrieve the company profile based on the provided company_id
        company = CompanyProfile.objects.get(id=company_id)
        return company
    except CompanyProfile.DoesNotExist:
        # Handle the case where the company profile does not exist
        return None



def delete_aptd_result(request, result_id):
    aptd_result = get_object_or_404(AptdResult, id=result_id)
    aptd_result.status = False
    aptd_result.save()
    return redirect('shortlist2')

# views.py

from django.shortcuts import render


import json



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ShortlistedStudent
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
@csrf_exempt
def shortlist_selected_students(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            selected_students = data.get('selected_students', [])

            print('Received selected student IDs:', selected_students)  # Print selected student IDs

            # Process the selected students
            for student_id in selected_students:
                # Your logic to create ShortlistedStudent objects here
                print(f'Shortlisting student with ID {student_id}')

            return JsonResponse({'message': 'Selected students shortlisted successfully'}, status=200)
        except Exception as e:
            print('Error processing request:', str(e))
            return JsonResponse({'error': 'Error processing request'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# def webscrap(request, studentprofile_id):
#     studentprofile = StudentProfile.objects.get(id=studentprofile_id)
#     return render(request,'admin/student/webscrap.html',{'studentprofile':studentprofile})

from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

# Import necessary modules
from django.shortcuts import render
from .models import StudentProfile
import requests
from bs4 import BeautifulSoup

# views.py

# def webscrap(request, studentprofile_id):
#     studentprofile = StudentProfile.objects.get(id=studentprofile_id)
#     # URL of the website you want to scrape
#     url = 'https://www.techopedia.com/top-in-demand-tech-jobs'

#     # Send a GET request to the URL
#     response = requests.get(url)

#     # Parse the HTML content of the page
#     soup = BeautifulSoup(response.text, 'html.parser')
#     sections = soup.find_all('section', class_='ddo-section focus-section')

#     data = []
#     for section in sections:
#         # Extract headline
#         headline = section.find('h3', class_='card-title').text.strip()

#         # Extract content
#         content = section.find('div', class_='card-text').text.strip()

#         data.append({'headline': headline, 'content': content})

#     # Pass the scraped data to the template
#     return render(request, 'admin/student/webscrap.html', {'data': data,'studentprofile':studentprofile})

def webscrap(request, studentprofile_id):
    studentprofile = StudentProfile.objects.get(id=studentprofile_id)
    # URL of the website you want to scrape
    url = 'https://www.cio.com/article/230935/hiring-the-most-in-demand-tech-jobs-for-2021.html'
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all <div> elements
    paragraphs = soup.find_all('p')
    
    # Extract the text content of each <div> element
    paragraph_texts = [p.get_text() for p in paragraphs]    
    # Pass the extracted information to the template
    return render(request, 'admin/student/webscrap.html', {'paragraph_texts': paragraph_texts,'studentprofile':studentprofile})

import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import PlacementRecord

def department_wise_placements(request):
    departments = ['CS', 'IT', 'ECE', 'MCA']
    years = ['2019', '2020', '2021', '2022', '2023']
    placement_data = {}

    for department in departments:
        placement_data[department] = [PlacementRecord.objects.filter(department=department, year=year).count() for year in years]

    # Generate bar graph
    plt.figure(figsize=(10, 6))
    for department in departments:
        plt.bar(years, placement_data[department], label=department)
    plt.xlabel('Year')
    plt.ylabel('Number of Placements')
    plt.title('Department Wise Placements')
    plt.legend()
    plt.savefig('media/department_wise_placements.png')  # Save the plot as an image file
    plt.close()

    return render(request, 'admin/index-2.html')

