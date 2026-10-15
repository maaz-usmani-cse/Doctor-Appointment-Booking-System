from django.urls import path
from . import views
urlpatterns=[
    path('',views.landing_view,name='landing'),
    path('booking_appoinment/',views.booking_appoinment_view,name='book_appointment'),
    path('show_all/',views.show_all_view ,name='show_all'),
    path('cancel_booking/<str:booking_id>/',views.cancel_booking_view,name='cancel_booking')
    

]