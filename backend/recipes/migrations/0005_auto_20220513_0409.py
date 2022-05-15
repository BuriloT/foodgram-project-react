# Generated by Django 2.2.16 on 2022-05-13 01:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20220504_1617'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'избранное', 'verbose_name_plural': 'избранные'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'ингредиент', 'verbose_name_plural': 'ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-id'], 'verbose_name': 'рецепт', 'verbose_name_plural': 'рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'рецепт и ингредиент', 'verbose_name_plural': 'рецепты и ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='shopping_cart',
            options={'verbose_name': 'корзина покупок', 'verbose_name_plural': 'корзины покупок'},
        ),
        migrations.AlterModelOptions(
            name='subscribe',
            options={'verbose_name': 'подписка', 'verbose_name_plural': 'подписки'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'тег', 'verbose_name_plural': 'теги'},
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipe', to='recipes.Recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_user', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=200, verbose_name='единица измерения'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.IntegerField(verbose_name='время приготовления'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='media/recipe', verbose_name='картинка'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipe', through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(db_index=True, max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipe', to='recipes.Tag', verbose_name='теги'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='text',
            field=models.TextField(verbose_name='текст'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.IntegerField(verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='shopping_cart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_cart', to='recipes.Recipe', verbose_name='рецепт'),
        ),
        migrations.AlterField(
            model_name='shopping_cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_cart', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe', to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AlterField(
            model_name='subscribe',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriber', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, verbose_name='цвет'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, verbose_name='слаг'),
        ),
    ]
