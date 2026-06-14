"""Seed completo de la demo (seed-demo.md). Idempotente.

Orquesta taxonomía + config + elegibilidad, y siembra empresas y convocatorias de
muestra (ficticias realistas) con cifras que la landing/dashboards calculan de verdad.
Crea además un usuario demo por rol (egresado, administrador, empresa) para mostrar
los flujos al jurado; en producción cada quien entra con su propio Gmail.
"""

from datetime import timedelta
from decimal import Decimal

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.convocatorias.models import (
    CREADA_POR_ADMIN,
    CREADA_POR_EMPRESA,
    ESTADO_PENDIENTE,
    ESTADO_PUBLICADA,
    Convocatoria,
)
from apps.core import constants
from apps.core.models import AdminAllowlist
from apps.empresas.models import ESTADO_ACTIVA, Empresa, Reclutador
from apps.taxonomia.models import Carrera
from apps.usuarios.models import (
    FUENTE_AUTODECLARADO,
    FUENTE_VERIFICADO,
    ROL_ADMIN,
    ROL_EGRESADO,
    ROL_RECLUTADOR,
    Credencial,
)
from apps.usuarios.services import asegurar_perfil, asegurar_perfil_talento

User = get_user_model()

ADMIN_DEMO = "bolsa.trabajo@unsa.edu.pe"

# Usuarios por defecto para la demo (uno por rol). Contraseña común para mostrar los flujos.
PASSWORD_DEMO = "demo12345"

# (ruc, razón social, nombre comercial, registrada?) — empresas reales (Arequipa/Perú).
# La identidad final (nombre, logo, banner, web) la fija `seed_imagenes`; aquí solo
# se crean los registros para que las convocatorias de muestra tengan a quién colgar.
EMPRESAS = [
    ("20100000011", "Globant Perú S.A.C.", "Globant", True),
    ("20100000012", "Unión Andina de Cementos S.A.A.", "UNACEM", True),
    ("20100000013", "Danper Trujillo S.A.C.", "Danper", True),
    ("20100000014", "Clínica Internacional S.A.", "Clínica Internacional", True),
    ("20100000015", "Estudio Echecopar S.R.L.", "Estudio Echecopar", False),
    ("20100000016", "Sociedad Minera Cerro Verde S.A.A.", "Cerro Verde", False),
    ("20100000017", "Programa Nacional de Becas y Crédito Educativo", "Pronabec", False),
    ("20100000018", "PricewaterhouseCoopers S.C.R.L.", "PwC Perú", True),
]

# (empresa_idx, tipo, titulo, carreras, transparencia_alta?, estado)
CONVOCATORIAS = [
    (0, constants.TIPO_PRACTICA_PREPROFESIONAL, "Practicante de Desarrollo de Software",
     ["Ingeniería de Sistemas", "Ciencia de la Computación"], True, ESTADO_PUBLICADA),
    (0, constants.TIPO_EMPLEO, "Desarrollador Backend Python",
     ["Ingeniería de Sistemas"], True, ESTADO_PUBLICADA),
    (0, constants.TIPO_TRAINEE, "Trainee de Datos",
     ["Ingeniería de Sistemas", "Ingeniería Industrial"], False, ESTADO_PUBLICADA),
    (1, constants.TIPO_PRACTICA_PROFESIONAL, "Asistente de Obra",
     ["Ingeniería Civil"], True, ESTADO_PUBLICADA),
    (1, constants.TIPO_EMPLEO, "Ingeniero Civil Residente",
     ["Ingeniería Civil", "Ingeniería Sanitaria"], False, ESTADO_PUBLICADA),
    (2, constants.TIPO_EMPLEO, "Ingeniero Agrónomo de Campo",
     ["Agronomía", "Ingeniería Ambiental"], True, ESTADO_PUBLICADA),
    (2, constants.TIPO_VOLUNTARIADO, "Voluntariado en Proyecto Rural",
     ["Agronomía", "Trabajo Social"], False, ESTADO_PUBLICADA),
    (3, constants.TIPO_EMPLEO, "Enfermero(a) Asistencial",
     ["Enfermería"], True, ESTADO_PUBLICADA),
    (3, constants.TIPO_PRACTICA_PROFESIONAL, "Practicante de Nutrición",
     ["Ciencias de la Nutrición"], False, ESTADO_PUBLICADA),
    (4, constants.TIPO_EMPLEO, "Abogado Corporativo Junior",
     ["Derecho"], True, ESTADO_PUBLICADA),
    (4, constants.TIPO_CONSULTORIA, "Consultoría Legal por Proyecto",
     ["Derecho"], False, ESTADO_PUBLICADA),
    (5, constants.TIPO_EMPLEO, "Ingeniero de Minas Junior",
     ["Ingeniería de Minas", "Ingeniería Geológica"], True, ESTADO_PUBLICADA),
    (5, constants.TIPO_CAS, "Especialista Ambiental (CAS)",
     ["Ingeniería Ambiental"], False, ESTADO_PUBLICADA),
    (6, constants.TIPO_VOLUNTARIADO, "Tutor Voluntario de Matemática",
     ["Educación", "Matemática"], False, ESTADO_PUBLICADA),
    (6, constants.TIPO_BECA, "Beca de Formación Docente",
     ["Educación"], True, ESTADO_PUBLICADA),
    (7, constants.TIPO_EMPLEO, "Analista de Marketing Digital",
     ["Marketing", "Administración"], True, ESTADO_PUBLICADA),
    (7, constants.TIPO_TRAINEE, "Trainee de Finanzas",
     ["Finanzas", "Economía", "Contabilidad"], False, ESTADO_PUBLICADA),
    (7, constants.TIPO_EMPLEO, "Contador Senior",
     ["Contabilidad"], True, ESTADO_PUBLICADA),
    (0, constants.TIPO_EMPLEO, "Analista QA",
     ["Ingeniería de Sistemas"], False, ESTADO_PENDIENTE),
    (1, constants.TIPO_PRACTICA_PREPROFESIONAL, "Practicante de Arquitectura",
     ["Arquitectura"], False, ESTADO_PENDIENTE),
]


class Command(BaseCommand):
    help = "Siembra la demo completa (idempotente)."

    def handle(self, *args, **options):
        call_command("seed_taxonomia")
        call_command("seed_config")
        call_command("seed_elegibilidad")

        AdminAllowlist.objects.get_or_create(
            email=ADMIN_DEMO, defaults={"nota": "Administrativo de demo"}
        )

        empresas = []
        for ruc, razon, comercial, registrada in EMPRESAS:
            empresa, _ = Empresa.objects.get_or_create(
                ruc=ruc,
                defaults={
                    "razon_social": razon,
                    "nombre_comercial": comercial,
                    "estado": ESTADO_ACTIVA,
                    "logo_url": "",
                },
            )
            if registrada and not hasattr(empresa, "reclutador"):
                username = f"empresa_{ruc[-3:]}"
                user, creado = User.objects.get_or_create(
                    username=username, defaults={"email": f"{username}@demo.pe"}
                )
                if creado:
                    user.set_password("demo12345")
                    user.save()
                perfil = asegurar_perfil(user)
                perfil.rol = ROL_RECLUTADOR
                perfil.save(update_fields=["rol"])
                Reclutador.objects.get_or_create(
                    empresa=empresa,
                    defaults={"usuario": user, "nombres": "Reclutador",
                              "ap_paterno": comercial.split()[0]},
                )
            empresas.append(empresa)

        from django.utils.text import slugify

        hoy = timezone.localdate()
        n_conv = 0
        for idx, tipo, titulo, carreras_nombres, alta, estado in CONVOCATORIAS:
            empresa = empresas[idx]
            creada_por = CREADA_POR_EMPRESA if not empresa.es_referencial else CREADA_POR_ADMIN
            # Medio de postulación realista: correo de RR.HH. de la empresa (la vista lo
            # abre como mailto: → funciona en la demo). En producción es la URL/email real.
            dominio = (slugify(empresa.nombre_comercial or empresa.razon_social) or "empresa") + ".pe"
            email_emp = f"rrhh@{dominio}"
            datos = {
                "tipo": tipo,
                "descripcion": (
                    "Buscamos talento agustino comprometido. Funciones, requisitos y "
                    "condiciones detalladas para una postulación informada y transparente."
                ),
                "modalidad": "presencial",
                "ubicacion": "Arequipa",
                "duracion_estimada": "6 meses",
                "fecha_limite": hoy + timedelta(days=30),
                "medio_postulacion": email_emp,
                "email_contacto": email_emp,
                "no_discriminacion": True,
                "regimen": "D.L. 728" if tipo in (
                    constants.TIPO_EMPLEO, constants.TIPO_TRAINEE) else "",
                "creada_por": creada_por,
                "estado": estado,
            }
            if tipo == constants.TIPO_PRACTICA_PREPROFESIONAL:
                datos.update({"requiere_convenio": True, "ciclo_minimo": 6,
                              "subvencion_remuneracion": Decimal("1200")})
            elif tipo == constants.TIPO_PRACTICA_PROFESIONAL:
                datos.update({"requiere_convenio": True, "tiempo_egreso_meses": 12,
                              "subvencion_remuneracion": Decimal("1200")})
            elif tipo == constants.TIPO_BECA:
                datos.update({"entidad_otorgante": "Pronabec"})
            if tipo not in (constants.TIPO_VOLUNTARIADO,) and tipo in (
                constants.TIPO_EMPLEO, constants.TIPO_TRAINEE, constants.TIPO_CAS):
                datos["subvencion_remuneracion"] = Decimal("2500")
            if alta:
                datos.update({
                    "banda_salarial_min": Decimal("2500"),
                    "banda_salarial_max": Decimal("3800"),
                    "vacantes": 3,
                    "beneficios": "EPS, capacitación continua, movilidad.",
                    "discapacidad": True,
                })

            conv, creada = Convocatoria.objects.get_or_create(
                empresa=empresa, titulo=titulo, defaults=datos
            )
            if creada:
                carreras = Carrera.objects.filter(nombre__in=carreras_nombres)
                conv.carreras_objetivo.set(carreras)
                if estado == ESTADO_PUBLICADA:
                    conv.fecha_publicacion = timezone.now()
                conv.recalcular_transparencia(guardar=False)
                conv.save()
                n_conv += 1

        self._crear_usuarios_demo()

        # Cuentas de empresa (login por email) e imágenes realistas (logo + banner).
        call_command("seed_cuentas")
        call_command("seed_imagenes")
        # Notificaciones in-app para que la campana se vea viva.
        call_command("seed_notificaciones")

        self.stdout.write(self.style.SUCCESS(
            f"Demo sembrada: {Empresa.objects.count()} empresas, "
            f"{Convocatoria.objects.count()} convocatorias, 1 administrativo en allowlist."
        ))
        self.stdout.write(self.style.SUCCESS(
            "Usuarios por defecto (contraseña «demo12345»): "
            "demo_egresado · demo_admin · demo_empresa."
        ))

    @staticmethod
    def _email_login(user):
        """Registra el email del usuario como verificado/primario (login por email)."""
        if not user.email:
            return
        EmailAddress.objects.update_or_create(
            user=user, email=user.email, defaults={"verified": True, "primary": True}
        )

    def _crear_usuarios_demo(self):
        """Crea un usuario por rol (egresado, administrador, empresa) con datos completos. Idempotente."""
        # ---- 1) Egresada: Ingeniería Industrial, perfil completo ----
        egresado, _ = User.objects.get_or_create(username="demo_egresado")
        egresado.email = "demo.egresado@unsa.edu.pe"
        egresado.first_name = "María Fernanda"
        egresado.last_name = "Quispe Mamani"
        egresado.set_password(PASSWORD_DEMO)
        egresado.save()
        self._email_login(egresado)

        perfil = asegurar_perfil(egresado)
        perfil.rol = ROL_EGRESADO
        perfil.perfil_completo = True
        perfil.consentimiento_datos = True
        perfil.save()

        talento = asegurar_perfil_talento(egresado)
        talento.carrera = (
            Carrera.objects.filter(nombre="Ingeniería Industrial").first()
            or Carrera.objects.first()
        )
        talento.estado_academico = "egresado"
        # Identidad verificada contra el padrón académico (Eje 2 · interoperabilidad).
        # Coincide con apps.integraciones.padron.PADRON_DEMO["12345678"].
        talento.dni = "12345678"
        talento.identidad_verificada = True
        talento.frecuencia = "semanal"
        talento.tipos_preferidos = ["trainee", "empleo", "practica_profesional"]
        talento.save()
        # Carrera afín de interés (amplía el feed)
        admin_fac = Carrera.objects.filter(nombre="Administración").first()
        if admin_fac:
            talento.carreras_extra.add(admin_fac)

        credenciales = [
            ("idioma", "Inglés B2 — Centro de Idiomas UNSA", FUENTE_VERIFICADO),
            ("tesis", "Optimización de la línea de producción (2025)", FUENTE_VERIFICADO),
            ("practica_convalidada", "Prácticas en planta — sector industrial", FUENTE_VERIFICADO),
            ("representacion", "Delegada de Ingeniería Industrial (2023)", FUENTE_AUTODECLARADO),
            ("voluntariado", "Voluntariado TECHO (2024)", FUENTE_AUTODECLARADO),
        ]
        for tipo, detalle, fuente in credenciales:
            Credencial.objects.get_or_create(
                perfil=talento, tipo=tipo, detalle=detalle,
                defaults={"fuente": fuente, "visible_para_empresas": True},
            )

        # ---- 2) Administrador (rol por allowlist) ----
        AdminAllowlist.objects.get_or_create(
            email="demo.admin@unsa.edu.pe", defaults={"nota": "Administrativo demo"}
        )
        admin, _ = User.objects.get_or_create(username="demo_admin")
        admin.email = "demo.admin@unsa.edu.pe"
        admin.first_name = "Lucía"
        admin.last_name = "Herrera Paredes"
        admin.set_password(PASSWORD_DEMO)
        admin.save()
        self._email_login(admin)
        perfil_admin = asegurar_perfil(admin)
        perfil_admin.rol = ROL_ADMIN
        perfil_admin.perfil_completo = True
        perfil_admin.consentimiento_datos = True
        perfil_admin.save()

        # ---- 3) Empresa (reclutador con empresa verificada) ----
        empresa, _ = Empresa.objects.get_or_create(ruc="20100000100")
        empresa.razon_social = "Soluciones Industriales del Sur S.A.C."
        empresa.nombre_comercial = "SISUR"
        empresa.tipo = "sac"
        empresa.ciiu = "2829 — Fabricación de maquinaria de uso especial"
        empresa.telefono = "054-201020"
        empresa.direccion = "Parque Industrial APIMA, Arequipa"
        empresa.web = "https://sisur.demo.pe"
        empresa.descripcion = (
            "Empresa arequipeña de soluciones industriales y mejora de procesos. "
            "Buscamos talento agustino en ingeniería y gestión."
        )
        empresa.estado = ESTADO_ACTIVA
        empresa.save()

        recl, _ = User.objects.get_or_create(username="demo_empresa")
        recl.email = "rrhh@sisur.demo.pe"
        recl.first_name = "Carlos"
        recl.last_name = "Rivera Núñez"
        recl.set_password(PASSWORD_DEMO)
        recl.save()
        perfil_recl = asegurar_perfil(recl)
        perfil_recl.rol = ROL_RECLUTADOR
        perfil_recl.save(update_fields=["rol"])
        Reclutador.objects.update_or_create(
            empresa=empresa,
            defaults={
                "usuario": recl, "dni": "44556677", "nombres": "Carlos",
                "ap_paterno": "Rivera", "ap_materno": "Núñez",
                "cargo": "Jefe de Recursos Humanos", "email": "rrhh@sisur.demo.pe",
                "telefono": "987654321",
            },
        )
