from django.db import migrations, models


def normalizar_dni(apps, schema_editor):
    PerfilTalento = apps.get_model("usuarios", "PerfilTalento")
    PerfilTalento.objects.filter(dni__isnull=True).update(dni="")


class Migration(migrations.Migration):

    dependencies = [
        ("usuarios", "0004_perfil_consentimiento_matching_and_more"),
    ]

    operations = [
        migrations.RunPython(normalizar_dni, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="perfiltalento",
            name="dni",
            field=models.CharField(blank=True, default="", max_length=8, verbose_name="DNI"),
        ),
    ]
