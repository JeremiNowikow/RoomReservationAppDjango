from django.urls import path, re_path
from . import views as views

urlpatterns = [
    path('', views.render_base_page),
    path('room/new/', views.AddRoom.as_view()),
    path('room/', views.show_rooms),
    re_path(r'^room/delete/(?P<id>\d+)/$', views.delete_room),
    re_path(r'^room/modify/(?P<id>\d+)/$', views.Modify_Room.as_view()),
    re_path(r'^room/reserve/(?P<id>\d+)/$', views.Make_Reservation.as_view()),
    re_path(r'^room/(?P<id>\d+)/$', views.individual_room_view),

]