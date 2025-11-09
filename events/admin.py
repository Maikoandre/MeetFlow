from django.contrib import admin

from .models import Usuario, Evento, Inscricao, Presenca, Relatorio

admin.site.register(Usuario)
admin.site.register(Evento)
admin.site.register(Inscricao)
admin.site.register(Presenca)
admin.site.register(Relatorio)
