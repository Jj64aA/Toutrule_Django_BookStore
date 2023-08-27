# Generated by Django 4.1.7 on 2023-08-22 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookstore', '0003_tag_order_book_order_customer_book_tags_order_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Physique', 'Physique'), ('Math', 'Math'), ('Science and Technology', 'Science and Technology'), ('Computer science', 'Computer science'), ('Artificial intelligence', 'Artificial intelligence'), ('Space science', 'Space science'), ('Programming', 'Programming')], max_length=190, null=True),
        ),
    ]
