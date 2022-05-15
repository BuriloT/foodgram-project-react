# Generated by Django 2.2.16 on 2022-05-04 13:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_recipe_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipe', through='recipes.RecipeIngredient', to='recipes.Ingredient'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipe', to='recipes.Tag'),
        ),
    ]
