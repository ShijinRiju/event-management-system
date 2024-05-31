from io import BytesIO
from django.shortcuts import get_object_or_404, render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout
import pycountry
import xlsxwriter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import *

# Create your views here.

def index(request):
    data = AddEvents.objects.all()
    return render(request,"index.html",{"data":data})

def register(request):
    countries = [country.name for country in pycountry.countries]
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        country = request.POST['country']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if not CustomLogin.objects.filter(username = email).exists():
            if password == confirm:
                login_query = CustomLogin.objects.create_user(username = email, password = password, userType = "USER",is_active = 0, viewPass = password)
                login_query.save()
                register_query = UserRegister.objects.create(name = name, email = email, phone = phone, country = country, login_id = login_query)
                register_query.save()
                return redirect("/event-login")
            else:
                return HttpResponse('<script>alert("Password does\'nt match");window.location.href="/event-register"</script>')

        else:
            return HttpResponse('<script>alert("Email already exists");window.location.href="/event-register"</script>')

    return render(request,"event-register.html", {"countries":countries})

def sign_in(request):
    pass_error = None
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        
        if user is not None:
            if not user.check_password(password):
                pass_error = "Wrong Password"
            else:
                login(request, user)
                if user.userType == "USER":
                    request.session['userid'] = user.id
                    return redirect('/user_index')
                elif user.userType == "COMPANY":
                    request.session['userid'] = user.id
                    return redirect('/company-index')
                elif user.userType == "ADMIN":
                    request.session['uid'] = user.id
                    return redirect('/admin_index')
        else:
            # User authentication failed
            # return HttpResponse('<script>alert("Invalid email or password");window.location.href="/event-login"</script>')
            pass_error = "Invalid email or password"

    return render(request, "event-login.html", {"pass_error":pass_error})

def adminUserView(request):
    user = request.session['uid']
    data = UserRegister.objects.filter(login_id__is_active = 1)
    return render(request,"adminUserView.html",{"data":data})

def user_update(request):
    id = request.GET['id']
    data = UserRegister.objects.get(login_id = id) 
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        country = request.POST['country']
        user_update = UserRegister.objects.filter(login_id = id).update(name = name, email = email, phone = phone, country = country)
        return redirect('/user_view')
    return render(request,"user_update.html",{"data":data})

def user_delete(request):
    id = request.GET['id']
    data = CustomLogin.objects.get(id = id).delete()
    return redirect('/user_view')

def add_event(request):
    countries = [country.name for country in pycountry.countries]
    user = request.session['userid']
    data = CompanyRegister.objects.get(login_id = user)
    # print(data)
    if request.POST:
        company = request.POST['company']
        email = request.POST['email']
        phone = request.POST['phone']
        event = request.POST['event']
        date = request.POST['date']
        country = request.POST['country']
        poster = request.FILES['poster']
        price = request.POST['price']
        event_query = AddEvents.objects.create(company = company, email = email, phone = phone, event = event, date = date, country = country, poster = poster, price = price, company_id = data)
        event_query.save()
    return render(request,"add-event.html",{"countries":countries})

def event_view(request):
    user = request.session['userid']
    data = AddEvents.objects.filter(company_id__login_id = user)
    print(data)
    return render(request,"event-view.html",{"data":data})

def tickets(request):
    event_id = request.GET.get('id')
    event = get_object_or_404(AddEvents, id=event_id)
    user_id = request.session.get('userid')
    user = get_object_or_404(UserRegister, login_id=user_id)

    if request.method == 'POST':
        persons = request.POST.get('persons')
        credit = request.POST.get('credit')
        amount = event.price
        total = int(persons)*int(amount)
        booking_query = EventBook.objects.create(
            event_id=event,
            user_id=user,
            company_id = event.company_id,
            persons=persons,
            credit=credit,
            total_amount = total
        )

        context = {
            'event': event,
            'user': user,
            'persons': persons,
            'credit': credit
        }

        return render(request, 'booking_success.html', context)


    return render(request, "ticket-booking.html", {"event": event, "user": user})

def user_index(request):
    data = request.session['userid']
    print(data)
    user = UserRegister.objects.get(login_id = data)
    print(user)
    return render(request,"user-index.html")

def company_register(request):
    countries = [country.name for country in pycountry.countries]
    pass_error = None
    if request.POST:
        company_name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        country = request.POST['country']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if not CustomLogin.objects.filter(username = email).exists():
            if password == confirm:
                login_query = CustomLogin.objects.create_user(username = email, password = password, userType = "COMPANY",is_active = 0, viewPass = password)
                login_query.save()
                register_query = CompanyRegister.objects.create(company = company_name, email = email, phone = phone, country = country, login_id = login_query)
                register_query.save()
                return redirect("/event-login")
            else:
                pass_error = "Password Does'st match"
        else:
            pass_error = "Email already exists"
    return render(request,"company-register.html",{"countries":countries,"pass_error":pass_error})

def company_index(request):
    data = request.session['userid']
    print(data)
    user = CompanyRegister.objects.get(login_id = data)
    print(user)
    return render(request, "company-index.html")

def sign_out(request):
    logout(request)
    request.session.flush()
    return redirect('/event-login')

def user_eventView(request):
    data = AddEvents.objects.all()
    return render(request,"user_EventView.html",{"data":data})

def booking_success(request):
    user_id = request.session.get('userid')
    return render(request, "booking_success.html")

def user_bookings(request):
    user_id = request.session.get('userid')
    bookings = EventBook.objects.filter(user_id__login_id=user_id)
    print(bookings)
    return render(request, "user_bookings.html", {"bookings": bookings})

def event_update(request):
    id = request.GET['id']
    data = AddEvents.objects.get(id = id)
    if request.POST:
        company = request.POST['company']
        email = request.POST['email']
        phone = request.POST['phone']
        event = request.POST['event']
        price = request.POST['price']
        event_update = AddEvents.objects.filter(id=id).update(company = company, email = email, phone = phone, event = event, price = price)
        return redirect('/event_view')
    return render(request,'event_update.html',{"data":data})

def admin_index(request):
    data = request.session['uid']
    print(data)
    user = CustomLogin.objects.get(id = data)
    print(user)
    return render(request, "admin_index.html")

def adminEventView(request):
    user = request.session['uid']
    data = AddEvents.objects.all()
    return render(request, "adminEventView.html",{"data":data})

def adminBookingsView(request):
    user = request.session['uid']
    data = EventBook.objects.all()
    return render(request, "adminBookingsView.html",{"data":data})

def adminBookDelete(request):
    id = request.GET['id']
    data = EventBook.objects.get(id = id).delete()
    return redirect('/adminBookingsView')

def adminEventDelete(request):
    id = request.GET['id']
    data = AddEvents.objects.get(id = id).delete()
    return redirect('/adminEventView')

def adminCompanyView(request):
    user = request.session['uid']
    data = CompanyRegister.objects.all()
    return render(request, 'adminCompanyView.html',{"data":data})

def adminCompanyDelete(request):
    id = request.GET['id']
    data = CustomLogin.objects.get(id = id)
    return redirect('/adminCompanyView')

def requests(request):
    data = CustomLogin.objects.filter(is_active = 0)
    return render(request,'requests.html',{"data":data})

def approve(request):
    id = request.GET['id']
    data = CustomLogin.objects.filter(id=id).update(is_active = 1)
    return redirect('/adminUserView')

def adminUserDelete(request):
    id = request.GET['id']
    data = CustomLogin.objects.get(id = id).delete()
    return redirect('/adminUserView')

def adminCompanyDelete(request):
    id = request.GET['id']
    data = CustomLogin.objects.get(id = id).delete()
    return redirect('/adminCompanyView')

def companyBookView(request):
    user = request.session['userid']
    print(user)
    data = EventBook.objects.filter(company_id__login_id = user)
    print(data)
    return render(request, "companyBookView.html",{"data":data})

def export_to_excel(request):
    data = EventBook.objects.all()

    # Create an in-memory output file for the Excel workbook.
    output = BytesIO()

    # Create a new Excel workbook.
    workbook = xlsxwriter.Workbook(output)

    # Add a worksheet.
    worksheet = workbook.add_worksheet()

    # Write header row.
    header = ['User ID', 'Name', 'E-Mail', 'Phone Number', 'Event', 'Price']
    for col, field in enumerate(header):
        worksheet.write(0, col, field)

    # Write data rows.
    for row, item in enumerate(data, start=1):
        worksheet.write(row, 0, item.user_id.id)
        worksheet.write(row, 1, item.user_id.name)
        worksheet.write(row, 2, item.user_id.email)
        worksheet.write(row, 3, item.user_id.phone)
        worksheet.write(row, 4, item.event_id.event)
        worksheet.write(row, 5, item.total_amount)

    # Close the workbook.
    workbook.close()

    # Set up the response.
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=event_bookings.xlsx'

    # Write the output to the response.
    output.seek(0)
    response.write(output.getvalue())

    return response

def export_users_to_excel(request):
    data = UserRegister.objects.filter(login_id__is_active=1)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="users.xlsx"'

    workbook = xlsxwriter.Workbook(response)
    worksheet = workbook.add_worksheet()

    # Write headers
    headers = ['ID', 'Name', 'E-Mail', 'Phone Number', 'Country']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write data rows
    for row, user in enumerate(data, start=1):
        worksheet.write(row, 0, user.id)
        worksheet.write(row, 1, user.name)
        worksheet.write(row, 2, user.email)
        worksheet.write(row, 3, user.phone)
        worksheet.write(row, 4, user.country)

    workbook.close()

    return response

def export_users_to_pdf(request):
    data = UserRegister.objects.filter(login_id__is_active=1)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="users.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    table_data = []

    # Add table headers
    table_data.append(['ID', 'Name', 'E-Mail', 'Phone Number', 'Country'])

    # Add data rows
    for user in data:
        table_data.append([user.id, user.name, user.email, user.phone, user.country])

    # Create the table
    table = Table(table_data)

    # Add style to the table
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table.setStyle(style)

    # Add the table to the PDF document
    doc.build([table])

    return response
