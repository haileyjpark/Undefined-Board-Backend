# Generated by Django 4.0.2 on 2022-03-09 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0006_alter_post_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='viewer',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddConstraint(
            model_name='commentlike',
            constraint=models.UniqueConstraint(fields=('user', 'comment'), name='unique comment likes'),
        ),
        migrations.AddConstraint(
            model_name='postlike',
            constraint=models.UniqueConstraint(fields=('user', 'post'), name='unique post likes'),
        ),
    ]
