# Generated by Django 4.1.6 on 2023-02-15 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner_app', '0003_alter_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='productinrecipe',
            name='quantity_categories',
            field=models.IntegerField(choices=[(1, 'Glass'), (2, 'Tea Spoon'), (3, 'Table Spoon'), (4, 'Piece')], default=None),
        ),
    ]
