# Generated by Django 4.2.4 on 2023-08-22 16:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apptelovendo', '0006_customuser_role_detallepedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='asignado_a',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pedidos_asinados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='usuario',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to=settings.AUTH_USER_MODEL),
        ),
    ]
