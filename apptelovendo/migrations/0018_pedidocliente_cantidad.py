# Generated by Django 4.2.4 on 2023-09-10 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apptelovendo', '0017_remove_pedidocliente_usuario_pedidocliente_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedidocliente',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
