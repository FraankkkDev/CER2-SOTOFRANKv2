from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import login
from .models import Evento, Registro

class EventListView(ListView):
    model = Evento
    template_name = 'evento/event_list.html' 
    context_object_name = 'events' 

class EventDetailView(DetailView):
    model = Evento
    template_name = 'evento/event_detail.html'
    context_object_name = 'event' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_registered'] = Registro.objects.filter(evento=self.object, usuario=self.request.user).exists()
        return context
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Registro exitoso. ¡Bienvenido/a! {user.username}")
            return redirect('event_list')
    else:
        form = UserCreationForm()
        
    return render(request, 'registro/signup.html', {'form': form})

@login_required
def register_event(request, event_id):
    evento = get_object_or_404(Evento, id=event_id)
    usuario = request.user

    if Registro.objects.filter(evento=evento, usuario=usuario).exists():
        messages.warning(request, "Ya estás inscrito en este evento.")
        return redirect('event_detail', pk=event_id)

    if evento.plazas_disponibles > 0:
        try:
            Registro.objects.create(evento=evento, usuario=usuario)
            evento.plazas_disponibles -= 1
            evento.save()

            messages.success(request, f"Inscripción exitosa en {evento.titulo}.") 
            return redirect('my_events')
        except Exception:
            messages.error(request, "Error al inscribirse en el evento. Inténtalo de nuevo.")
    else:
        messages.error(request, "No hay plazas disponibles para este evento.")
    return redirect('event_detail', pk=event_id)

class MyEventsListView(LoginRequiredMixin, ListView):
    model = Registro
    template_name = 'evento/my_events.html' 
    context_object_name = 'registrations' 

    def get_queryset(self):
        return Registro.objects.filter(usuario=self.request.user).select_related('evento')
    
@login_required
def unregister_event(request, registration_id):
    registro = get_object_or_404(Registro, id=registration_id, usuario=request.user)
    evento = registro.evento

    registro.delete()

    evento.plazas_disponibles += 1
    evento.save()

    messages.info(request, f"Te has dado de baja del evento {evento.titulo}.")
    return redirect('my_events')