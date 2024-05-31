"""
URL configuration for Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('event-register/',views.register),
    path('event-login/',views.sign_in),
    path('adminUserView/',views.adminUserView),
    path('user_update/',views.user_update),
    path('user_delete/',views.user_delete),
    path('add_event/',views.add_event),
    path('event_view/',views.event_view),
    path('tickets/',views.tickets),
    path('user_index/',views.user_index),
    path('company-register/',views.company_register),
    path('company-index/',views.company_index),
    path('logout/',views.sign_out),
    path('userEventView/',views.user_eventView),
    path('booking_success/',views.booking_success),
    path('user_bookings/',views.user_bookings),
    path('event_update/',views.event_update),
    path('admin_index/',views.admin_index),
    path('adminEventView/',views.adminEventView),
    path('adminBookingsView/',views.adminBookingsView),
    path('adminBookDelete/',views.adminBookDelete),
    path('adminEventDelete/',views.adminEventDelete),
    path('adminCompanyView/',views.adminCompanyView),
    path('requests/',views.requests),
    path('approve/',views.approve),
    path('adminUserDelete/',views.adminUserDelete),
    path('companyBookView/',views.companyBookView),
    path('export-to-excel/',views.export_to_excel),
    path('export_users_to_excel/',views.export_users_to_excel),
    path('export_users_to_pdf/',views.export_users_to_pdf),
]
