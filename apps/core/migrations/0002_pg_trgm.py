from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    """Habilita pg_trgm para búsqueda por similitud (la usa 06-flujo-admin)."""

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        TrigramExtension(),
    ]
