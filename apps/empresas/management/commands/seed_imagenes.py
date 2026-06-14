"""Da identidad e imágenes REALISTAS a las empresas de la demo. Idempotente.

Para que el demo se vea lo más realista posible, las empresas se mapean a
**empresas reales** que operan en Arequipa / Perú por sector, y se descargan:

  - Logo: el logotipo real de la empresa (vía unavatar.io / favicons de Google /
    DuckDuckGo, eligiendo la mejor resolución disponible) compuesto sobre una
    tarjeta blanca redondeada, al estilo de los avatares de empresa de LinkedIn.
    Se emite como SVG con el logo embebido en base64 → archivo autocontenido.
  - Banner: fotografía sectorial real (Unsplash).

Se guardan en `static/img/empresas/` y se sirven vía STATIC_URL, de modo que el
demo no depende de la red en tiempo de render.

Nota: los logos son marcas registradas de sus titulares; se usan aquí solo con
fines de demostración / prototipo académico (no comercial).

Uso:
    python manage.py seed_imagenes            # descarga lo que falte
    python manage.py seed_imagenes --force     # vuelve a descargar todo
"""

import base64
import struct
from pathlib import Path
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.empresas.models import Empresa

DEST = Path(settings.BASE_DIR) / "static" / "img" / "empresas"
STATIC_PREFIX = "/static/img/empresas"
UA = "Mozilla/5.0 (ConectaUNSA demo seeder)"

# Fotografías sectoriales (Unsplash). IDs verificados, libres para uso.
BANNER = {
    "tech": "photo-1518770660439-4636190af475",
    "construccion": "photo-1541888946425-d81bb19240f5",
    "agro": "photo-1500382017468-9049fed747ef",
    "salud": "photo-1538108149393-fbbd81895907",
    "legal": "photo-1589829545856-d10d557cf95f",
    "mineria": "photo-1578319439584-104c94d37305",
    "educacion": "photo-1497486751825-1233686d5d80",
    "consultoria": "photo-1497215728101-856f4ea42174",
    "industrial": "photo-1581091226825-a6a2a5aee158",
}

# ruc -> empresa real (sector, dominio para el logo, y datos a fijar).
EMPRESAS = {
    "20100000011": ("tech", "globant.com", {
        "razon_social": "Globant Perú S.A.C.", "nombre_comercial": "Globant",
        "tipo": "sac", "ciiu": "6201 — Programación informática y servicios de TI",
        "telefono": "01-7009000", "direccion": "Av. El Derby 254, Santiago de Surco, Lima",
        "web": "https://www.globant.com",
        "linkedin": "https://www.linkedin.com/company/globant",
        "descripcion": "Compañía global de ingeniería de software y productos digitales. "
                       "Equipos de desarrollo, datos, QA y experiencia digital.",
    }),
    "20100000012": ("construccion", "unacem.pe", {
        "razon_social": "Unión Andina de Cementos S.A.A.", "nombre_comercial": "UNACEM",
        "tipo": "sa", "ciiu": "2394 — Fabricación de cemento; construcción",
        "telefono": "01-2173300", "direccion": "Av. Atocongo 2440, Villa María del Triunfo, Lima",
        "web": "https://www.unacem.pe",
        "linkedin": "https://www.linkedin.com/company/unacem",
        "descripcion": "Mayor productora de cemento del Perú e impulsora de proyectos de "
                       "construcción e infraestructura a nivel nacional.",
    }),
    "20100000013": ("agro", "danper.com", {
        "razon_social": "Danper Trujillo S.A.C.", "nombre_comercial": "Danper",
        "tipo": "sac", "ciiu": "0113 — Cultivo de hortalizas y agroexportación",
        "telefono": "044-208250", "direccion": "Carretera Industrial s/n, Moche, La Libertad",
        "web": "https://danper.com",
        "linkedin": "https://www.linkedin.com/company/danper",
        "descripcion": "Agroindustrial peruana exportadora de conservas y frescos, con "
                       "operaciones en la costa y sur del país y prácticas sostenibles.",
    }),
    "20100000014": ("salud", "clinicainternacional.com.pe", {
        "razon_social": "Clínica Internacional S.A.", "nombre_comercial": "Clínica Internacional",
        "tipo": "sa", "ciiu": "8610 — Actividades de hospitales y clínicas",
        "telefono": "01-6196161", "direccion": "Av. Garcilaso de la Vega 1420, Lima",
        "web": "https://www.clinicainternacional.com.pe",
        "linkedin": "https://www.linkedin.com/company/clinica-internacional",
        "descripcion": "Red de clínicas con sedes a nivel nacional; servicios de "
                       "especialidades médicas, emergencias y atención ambulatoria.",
    }),
    "20100000015": ("legal", "echecopar.com.pe", {
        "razon_social": "Estudio Echecopar S.R.L.", "nombre_comercial": "Estudio Echecopar",
        "tipo": "srl", "ciiu": "6910 — Actividades jurídicas",
        "telefono": "01-6188500", "direccion": "Av. de la Floresta 497, San Borja, Lima",
        "web": "https://www.echecopar.com.pe",
        "linkedin": "https://www.linkedin.com/company/estudio-echecopar",
        "descripcion": "Firma legal full-service miembro de Baker McKenzie; práctica "
                       "corporativa, laboral, tributaria y de recursos naturales.",
    }),
    "20100000016": ("mineria", "cerroverde.pe", {
        "razon_social": "Sociedad Minera Cerro Verde S.A.A.", "nombre_comercial": "Cerro Verde",
        "tipo": "sa", "ciiu": "0729 — Extracción de minerales metalíferos no ferrosos",
        "telefono": "054-381500", "direccion": "Asiento Minero Cerro Verde s/n, Uchumayo, Arequipa",
        "web": "https://www.cerroverde.pe",
        "linkedin": "https://www.linkedin.com/company/sociedad-minera-cerro-verde",
        "descripcion": "Una de las principales productoras de cobre del Perú, operadora "
                       "del complejo minero Cerro Verde en Arequipa.",
    }),
    "20100000017": ("educacion", "pronabec.gob.pe", {
        "razon_social": "Programa Nacional de Becas y Crédito Educativo",
        "nombre_comercial": "Pronabec",
        "tipo": "publica", "ciiu": "8430 — Administración pública / educación",
        "telefono": "01-6125300", "direccion": "Av. Arequipa 1935, Lince, Lima",
        "web": "https://www.gob.pe/pronabec",
        "linkedin": "https://www.linkedin.com/company/pronabec",
        "descripcion": "Organismo del Estado peruano que otorga becas y crédito educativo "
                       "para estudios de pregrado y posgrado.",
    }),
    "20100000018": ("consultoria", "pwc.com", {
        "razon_social": "PricewaterhouseCoopers S.C.R.L.", "nombre_comercial": "PwC Perú",
        "tipo": "srl", "ciiu": "7020 — Consultoría de gestión y auditoría",
        "telefono": "01-2116500", "direccion": "Av. Santo Toribio 143, San Isidro, Lima",
        "web": "https://www.pwc.pe",
        "linkedin": "https://www.linkedin.com/company/pwc-peru",
        "descripcion": "Firma global de auditoría, consultoría y asesoría tributaria y "
                       "financiera; programas de trainees y primeras experiencias.",
    }),
    "20100000100": ("industrial", "acerosarequipa.com", {
        "razon_social": "Corporación Aceros Arequipa S.A.", "nombre_comercial": "Aceros Arequipa",
        "tipo": "sa", "ciiu": "2410 — Industrias básicas de hierro y acero",
        "telefono": "054-495000", "direccion": "Av. Jenaro Castro Olachea s/n, Pachacútec, Arequipa",
        "web": "https://www.acerosarequipa.com",
        "linkedin": "https://www.linkedin.com/company/corporacion-aceros-arequipa",
        "descripcion": "Principal siderúrgica del Perú; fabricación de acero para "
                       "construcción e industria, con planta en Arequipa.",
    }),
}


# --- Descarga de logos ------------------------------------------------------
def _bajar(url: str) -> bytes:
    return urlopen(Request(url, headers={"User-Agent": UA}), timeout=20).read()


def _dims(b: bytes) -> tuple[int, int]:
    """Dimensiones de PNG/JPEG/ICO/GIF (sin dependencias externas)."""
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", b[16:24])
    if b[:3] == b"\xff\xd8\xff":
        i = 2
        while i < len(b) - 9:
            if b[i] != 0xFF:
                i += 1
                continue
            if 0xC0 <= b[i + 1] <= 0xC3:
                h, w = struct.unpack(">HH", b[i + 5:i + 9])
                return w, h
            i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
        return 0, 0
    if b[:4] == b"\x00\x00\x01\x00":  # ICO
        best = (0, 0)
        for k in range(b[4]):
            w = b[6 + k * 16] or 256
            h = b[7 + k * 16] or 256
            if w * h > best[0] * best[1]:
                best = (w, h)
        return best
    if b[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", b[6:10])
    if b.lstrip()[:4] == b"<svg" or b"<svg" in b[:300]:
        return 512, 512  # vectorial: tamaño nominal grande
    return 0, 0


def _mime(b: bytes) -> str:
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if b[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if b[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if b[:4] == b"\x00\x00\x01\x00":
        return "image/x-icon"
    if b"<svg" in b[:300]:
        return "image/svg+xml"
    return "application/octet-stream"


def _mejor_logo(dominio: str) -> bytes | None:
    """Descarga el logo de mayor resolución disponible para el dominio."""
    fuentes = [
        f"https://unavatar.io/{dominio}?fallback=false",
        f"https://www.google.com/s2/favicons?domain={dominio}&sz=256",
        f"https://icons.duckduckgo.com/ip3/{dominio}.ico",
    ]
    mejor, area = None, 0
    for src in fuentes:
        try:
            data = _bajar(src)
        except Exception:  # noqa: BLE001
            continue
        w, h = _dims(data)
        if w * h > area:
            area, mejor = w * h, data
    return mejor


def _tarjeta_svg(logo: bytes) -> str:
    """Compone el logo centrado sobre una tarjeta blanca redondeada (256×256)."""
    b64 = base64.b64encode(logo).decode("ascii")
    href = f"data:{_mime(logo)};base64,{b64}"
    # El logo se ajusta dentro de un recuadro de 176px con padding, centrado.
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" '
        'viewBox="0 0 256 256">'
        '<rect width="256" height="256" rx="52" fill="#ffffff"/>'
        '<rect x="1.5" y="1.5" width="253" height="253" rx="50.5" fill="none" '
        'stroke="#e5e7eb" stroke-width="3"/>'
        f'<image x="40" y="40" width="176" height="176" '
        f'preserveAspectRatio="xMidYMid meet" href="{href}"/>'
        '</svg>'
    )


def _descargar_banner(url: str, destino: Path, force: bool) -> bool:
    if destino.exists() and destino.stat().st_size > 0 and not force:
        return False
    destino.write_bytes(_bajar(url))
    return True


class Command(BaseCommand):
    help = "Mapea las empresas de la demo a empresas reales con su logo y banner."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Vuelve a descargar todo.")

    def handle(self, *args, **options):
        force = options["force"]
        DEST.mkdir(parents=True, exist_ok=True)

        bajados = actualizadas = 0
        for ruc, (sector, dominio, datos) in EMPRESAS.items():
            empresa = Empresa.objects.filter(ruc=ruc).first()
            if not empresa:
                self.stdout.write(self.style.WARNING(f"  RUC {ruc} no existe; omito."))
                continue

            banner_file = DEST / f"{ruc}-banner.jpg"
            logo_file = DEST / f"{ruc}-logo.svg"
            banner_url = f"https://images.unsplash.com/{BANNER[sector]}?w=1200&h=400&fit=crop&q=72"

            try:
                if _descargar_banner(banner_url, banner_file, force):
                    bajados += 1
                if force or not (logo_file.exists() and logo_file.stat().st_size > 0):
                    logo = _mejor_logo(dominio)
                    if not logo:
                        raise RuntimeError(f"sin logo para {dominio}")
                    logo_file.write_text(_tarjeta_svg(logo), encoding="utf-8")
                    bajados += 1
            except Exception as exc:  # noqa: BLE001
                self.stdout.write(self.style.ERROR(f"  {datos['nombre_comercial']}: error ({exc})"))
                continue

            # Fija identidad real + rutas de imagen (sobrescribe los datos ficticios).
            datos = {
                **datos,
                "logo_url": f"{STATIC_PREFIX}/{logo_file.name}",
                "banner_url": f"{STATIC_PREFIX}/{banner_file.name}",
            }
            for campo, valor in datos.items():
                setattr(empresa, campo, valor)
            empresa.save()
            actualizadas += 1
            self.stdout.write(f"  ✓ {empresa.nombre_comercial} ({sector})")

        self.stdout.write(self.style.SUCCESS(
            f"Empresas reales listas: {actualizadas} actualizadas, "
            f"{bajados} archivos descargados en {DEST}."
        ))
