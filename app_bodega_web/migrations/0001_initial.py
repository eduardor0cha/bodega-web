# Generated by Django 4.2.5 on 2023-09-29 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.TextField()),
                ('descricao', models.TextField()),
                ('valor', models.FloatField()),
                ('desconto', models.FloatField()),
                ('estoque', models.PositiveIntegerField()),
                ('criadoEm', models.DateTimeField(auto_now_add=True)),
                ('atualizadoEm', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
