from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
import datetime

from room_reservation.models import *

# Create your views here.

# Responsible for rendering the main page of the app
def render_base_page(request):
    return render(request, 'room_reservation/base_site.html')

# Handles adding new Room objects to the database from user input in the form
class AddRoom(View):
    def get(self, request):
        return render(request, 'room_reservation/add_room_form.html')

    def post(self, request):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        has_projector = bool(request.POST.get("has_projector"))

        if name is None:
            return render(request, 'room_reservation/add_room_form.html', {'error': "Name cannot be empty."})
        if int(capacity) < 1:
            return render(request, 'room_reservation/add_room_form.html', {'error': "Capacity must be larger than 0."})
        if Room.objects.filter(name=name).first():
            return render(request, 'room_reservation/add_room_form.html', {'error': "Room with such name already exists."})

        Room.objects.create(name=name, capacity=capacity, projector_available=has_projector)
        return redirect('/')


# shows a site with a table containing all rooms in the database
def show_rooms(request):
    rooms = Room.objects.all()
    for room in rooms:
        reservations = [reservation.date for reservation in room.roomreservation_set.all()]
        room.reserved = datetime.date.today() in reservations
    return render(request, 'room_reservation/all_rooms.html', {'rooms': rooms})


# Deletes the room from the database using its primary key
def delete_room(request, id):
    room = Room.objects.get(pk=id)
    room.delete()
    return redirect('/room/')

# loads a form to modify a room from the database using its id, and saves the changes
class Modify_Room(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        return render(request, 'room_reservation/modify_room.html', {'room': room})
    def post(self,request, id):
        room = Room.objects.get(pk=id)
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        has_projector = bool(request.POST.get("projector"))
        if name is None:
            return render(request, 'room_reservation/modify_room.html', {'error': "Name cannot be empty."})
        if int(capacity) < 1:
            return render(request, 'room_reservation/modify_room.html', {'room': room, 'error': "Capacity must be larger than 0."})
        if (room.name != name) and (Room.objects.filter(name=name)):
            return render(request, 'room_reservation/modify_room.html', {'room': room, 'error': "Room with that name already exists."})

        room.name = name
        room.capacity = capacity
        room.projector_available = has_projector
        room.save()
        return redirect('/room/')


class Make_Reservation(View):
    def get(self, request, id):
        room = Room.objects.get(pk=id)
        reservations = RoomReservation.objects.filter(room_id=room).order_by('date')
        return render(request, 'room_reservation/make_reservation.html', {'room': room, 'reservations': reservations})
    def post(self, request, id):
        date = request.POST.get("date")
        comment = request.POST.get("comment")
        room = Room.objects.get(pk=id)
        reservations = RoomReservation.objects.filter(room_id=room).order_by('date')

        if RoomReservation.objects.filter(room_id=room).filter(date=date):
            return render(request, 'room_reservation/make_reservation.html', {'room': room, 'reservations': reservations, 'error': "Room is already booked for that date"})

        if str(datetime.date.today()) > date:
            return render(request, 'room_reservation/make_reservation.html',
                          {'room': room, 'reservations': reservations, 'error': "Date cannot be from the past"})

        RoomReservation.objects.create(comment=comment, date=date, room_id=room)
        return redirect('/room/')

def individual_room_view(request, id):
    room = Room.objects.get(pk=id)
    reservations = RoomReservation.objects.filter(room_id=room).order_by('date')
    return render(request, 'room_reservation/room_view.html', {'room': room, 'reservations': reservations})






