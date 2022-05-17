from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'название',
        max_length=200
    )
    color = models.CharField(
        'цвет',
        max_length=50
    )
    slug = models.SlugField(
        'слаг',
        unique=True, max_length=200
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name[:50]


class Ingredient(models.Model):
    name = models.CharField(
        'название',
        max_length=200
    )
    measurement_unit = models.CharField(
        'единица измерения',
        max_length=200
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name[:50]


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='автор'
    )
    name = models.CharField(
        'название',
        max_length=200,
        db_index=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipe',
        verbose_name='теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipe',
        verbose_name='ингредиенты'
    )
    image = models.ImageField('картинка', upload_to='recipe/images')
    text = models.TextField('текст')
    cooking_time = models.IntegerField('время приготовления')

    class Meta:
        ordering = ['-id']
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name[:50]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='ингредиент'
    )
    amount = models.IntegerField('количество')

    class Meta:
        verbose_name = 'рецепт и ингредиент'
        verbose_name_plural = 'рецепты и ингредиенты'

    def __str__(self):
        return f'{self.ingredient} - {self.amount}'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='пользователь'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribe',
        verbose_name='автор'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'

    def __str__(self):
        return f'{self.user} - {self.author}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_user',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'избранные'

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_cart',
        verbose_name='пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_cart',
        verbose_name='рецепт'
    )

    class Meta:
        verbose_name = 'корзина покупок'
        verbose_name_plural = 'корзины покупок'

    def __str__(self):
        return f'{self.user} - {self.recipe}'
