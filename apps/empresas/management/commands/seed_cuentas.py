"""Da a CADA empresa de la demo una cuenta de reclutador con la que iniciar sesión.

Para poder probar el flujo completo de empresa (publicar, ver alcance, etc.) de la
forma más realista posible, cada empresa necesita "existir" como cuenta. Este comando:

  - Crea/actualiza el usuario reclutador de cada empresa con nombre y email realistas.
  - Fija el rol del Perfil a «reclutador» y vincula el Reclutador a la empresa.
  - Registra el email como verificado (allauth) para que el login por email funcione.
  - Restablece la contraseña a la contraseña de demo, para credenciales predecibles.

Es idempotente y, al final, imprime la tabla de credenciales.

Uso:
    python manage.py seed_cuentas
"""

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.empresas.models import ESTADO_ACTIVA, Empresa, Reclutador
from apps.usuarios.models import ROL_RECLUTADOR
from apps.usuarios.services import asegurar_perfil

User = get_user_model()

PASSWORD_DEMO = "demo12345"

# ruc -> (email_login, nombres, ap_paterno, ap_materno, cargo, dni, telefono)
# Emails con el dominio real de cada empresa (ver seed_imagenes). Demo: cualquiera
# entra con la contraseña común; no se envía correo real.
RECLUTADORES = {
    "20100000011": ("talento@globant.com", "Diego", "Salas", "Vargas",
                    "Talent Acquisition Lead", "45123678", "987112233"),
    "20100000012": ("seleccion@unacem.pe", "Patricia", "Núñez", "Flores",
                    "Jefa de RR. HH.", "29876543", "987223344"),
    "20100000013": ("rrhh@danper.com", "Rodrigo", "Cáceres", "Linares",
                    "Coordinador de Personal", "70345612", "987334455"),
    "20100000014": ("seleccion@clinicainternacional.com.pe", "Claudia", "Mendoza", "Rojas",
                    "Jefa de Gestión Humana", "41258963", "987445566"),
    "20100000015": ("reclutamiento@echecopar.com.pe", "Fernando", "Delgado", "Ríos",
                    "Director de Talento", "29541236", "987556677"),
    "20100000016": ("empleos@cerroverde.pe", "Sandra", "Apaza", "Choque",
                    "Especialista de Reclutamiento", "44789512", "987667788"),
    "20100000017": ("convocatorias@pronabec.gob.pe", "Miguel", "Torres", "Béjar",
                    "Coordinador de Programas", "42365897", "987778899"),
    "20100000018": ("careers@pwc.pe", "Andrea", "Gutiérrez", "Pinto",
                    "Consultora de Talento", "70912345", "987889900"),
    "20100000100": ("rrhh@acerosarequipa.com", "Carlos", "Rivera", "Núñez",
                    "Jefe de Recursos Humanos", "44556677", "987654321"),
}


class Command(BaseCommand):
    help = "Crea una cuenta de reclutador (login por email) para cada empresa de la demo."

    def handle(self, *args, **options):
        filas = []
        for ruc, datos in RECLUTADORES.items():
            email, nombres, ap_pat, ap_mat, cargo, dni, tel = datos
            empresa = Empresa.objects.filter(ruc=ruc).first()
            if not empresa:
                self.stdout.write(self.style.WARNING(f"  RUC {ruc} no existe; omito."))
                continue

            # Usuario (login por email; username estable por RUC).
            username = f"empresa_{ruc[-3:]}"
            existente = getattr(empresa, "reclutador", None)
            user = existente.usuario if existente else User.objects.filter(username=username).first()
            if user is None:
                user = User(username=username)
            user.email = email
            user.first_name = nombres
            user.last_name = f"{ap_pat} {ap_mat}".strip()
            user.is_active = True
            user.set_password(PASSWORD_DEMO)
            user.save()

            # Email verificado y primario → login por email fiable. Se degrada cualquier
            # primario previo antes de fijar el nuevo (evita chocar con unique_primary_email).
            EmailAddress.objects.filter(user=user).update(primary=False)
            EmailAddress.objects.update_or_create(
                user=user, email=email,
                defaults={"verified": True, "primary": True},
            )

            # Rol reclutador.
            perfil = asegurar_perfil(user)
            if perfil.rol != ROL_RECLUTADOR:
                perfil.rol = ROL_RECLUTADOR
                perfil.save(update_fields=["rol"])

            # Vínculo Reclutador ↔ Empresa.
            Reclutador.objects.update_or_create(
                empresa=empresa,
                defaults={
                    "usuario": user, "dni": dni, "nombres": nombres,
                    "ap_paterno": ap_pat, "ap_materno": ap_mat,
                    "cargo": cargo, "email": email, "telefono": tel,
                },
            )

            # Una empresa con reclutador debe estar activa para verse «verificada».
            if empresa.estado != ESTADO_ACTIVA:
                empresa.estado = ESTADO_ACTIVA
                empresa.save(update_fields=["estado"])

            filas.append((empresa.nombre_comercial or empresa.razon_social, email))

        self.stdout.write(self.style.SUCCESS(
            f"\n{len(filas)} cuentas de empresa listas (contraseña: «{PASSWORD_DEMO}»):"
        ))
        ancho = max((len(n) for n, _ in filas), default=10)
        for nombre, email in filas:
            self.stdout.write(f"  {nombre.ljust(ancho)}  →  {email}")
