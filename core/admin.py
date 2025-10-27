from django.contrib import admin
from .models import Evento, Registro 

class RegistroEnlinea(admin.TabularInline):
    model = Registro
    extra = 0
    readonly_fields = ('usuario', 'fecha_registro') 

    def get_usuario(self, obj):
        return obj.usuario.username
    get_usuario.short_description = "Asistente"

    fields = ('usuario', 'fecha_registro')
    can_delete = False

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tiempo', 'plazas_disponibles', 'plazas_totales', 'get_asistentes_totales','get_cantidad_recaudada')
    fields = ('titulo', 'tiempo', 'lugar', 'imagen', 'valor', 'plazas_totales', 'plazas_disponibles')
    search_fields = ('titulo', 'lugar')

    inlines = [RegistroEnlinea]

    def get_asistentes_totales(self, obj):
        return obj.registro_set.count()
    get_asistentes_totales.short_description = "Total de Asistentes"

    def get_cantidad_recaudada(self, obj):
        total_asistentes = obj.registro_set.count()
        cantidad_recaudada = total_asistentes * obj.valor
        recaudado_int = int(cantidad_recaudada)

        formato_us = f'{recaudado_int:,}'
        formato_clp = formato_us.replace(',', '.')

        return f'CLP ${formato_clp}'
    
    get_cantidad_recaudada.short_description = "Cantidad Recaudada"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.registro_set.exists():
            readonly_fields = readonly_fields + ('plazas_disponibles',)
        return readonly_fields

    def save_model(self, request, obj, form, change):
        if obj.pk:
            evento_ant = Evento.objects.get(pk=obj.pk)
            if obj.plazas_totales > evento_ant.plazas_totales:
                diferencia = obj.plazas_totales - evento_ant.plazas_totales
                obj.plazas_disponibles += diferencia
            elif obj.plazas_totales < evento_ant.plazas_totales:
                diferencia = evento_ant.plazas_totales - obj.plazas_totales
                obj.plazas_disponibles = max(0, obj.plazas_disponibles - diferencia)
        else:
            obj.plazas_disponibles = obj.plazas_totales
        super().save_model(request, obj, form, change)


class RegistroAdmin(admin.ModelAdmin):
    list_display = ('evento', 'usuario', 'fecha_registro')
    list_filter = ('evento', 'fecha_registro')
    search_fields = ('evento__titulo', 'usuario__username')
    readonly_fields = ('evento', 'usuario', 'fecha_registro')
