# Generated by Django 4.2.1 on 2024-05-31 20:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_isbn_mysite_isbn'),
    ]

    operations = [
        migrations.RenameField(
            model_name='isbn',
            old_name='name',
            new_name='book_name',
        ),
    ]