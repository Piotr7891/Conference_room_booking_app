from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from reservation_app.models import ConferenceRoom

# Create your views here.

class AddRoomView(View):
    def get(self, request):
        return render(request, "add_room.html")
#
    def post(self, request):
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "add_room.html", {'error_message': 'Nie podano nawy sali'})
        try:
            capacity = int(capacity)
            if capacity <= 0:
                raise ValueError()
        except ValueError:
            return render(request, "add_room.html", {'error_message': 'Pojemnosc sali musi byc liczba dodatnia.'})

        ConferenceRoom.objects.create(name=name, capacity=capacity, projector=projector)
        return redirect('room-list')
        # if capacity <= 0:
        #     return render(request, "add_room.html", context={"error": "Pojemność sali musi być dodatnia"})
        # if Conference_Room.objects.filter(name=name).first():
        #     return render(request, "add_room.html", context={"error": "Sala o podanej nazwie istnieje"})
#
    # Conference_Room.objects.create(name=name, capacity=capacity, projector_availability=projector)
    # return redirect("room-list")

class RoomListView(View):
    def get(self, request):
        rooms = ConferenceRoom.objects.all()
        return render(request, "rooms.html", context={"rooms": rooms})

class RoomDeleteView(View):
    def get(self, request, id):
        room = get_object_or_404(ConferenceRoom, id=id)
        room.delete()
        return redirect('room-list')

class RoomsEditView(View):
    def get(self, request, id):
        room = get_object_or_404(ConferenceRoom, id=id)
        return render(request, "modify_room.html", context={"room": room})

    def post(self, request, id):
        room = get_object_or_404(ConferenceRoom, id=id)
        name = request.POST.get("name")
        capacity = request.POST.get("capacity")
        projector = request.POST.get("projector") == "on"

        if not name:
            return render(request, "modify_room.html", {'error_message': 'Nie podano nawy sali'})

        try:
            capacity = int(capacity)
            if capacity <= 0:
                raise ValueError()
        except ValueError:
            return render(request, "modify_room.html", {'error_message': 'Pojemnosc sali musi byc liczba dodatnia.'})

        if name != room.name and ConferenceRoom.objects.filter(name=name).first():
            return render(request, "modify_room.html", context={"room": room, "error": "Sala o podanej nazwie istniej"})

        room.name = name
        room.capacity = capacity
        room.projector = projector
        room.save()
        return redirect('room-list')
