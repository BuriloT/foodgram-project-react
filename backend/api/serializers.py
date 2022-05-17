from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            Shopping_Cart, Subscribe, Tag, User)
from users.serializers import UserSerializer


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True,)
    password = serializers.CharField(write_only=True)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'name', 'color', 'slug'
        )
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(write_only=True)

    class Meta:
        fields = (
            'id', 'name', 'measurement_unit', 'amount'
        )
        read_only_fields = ['name', 'measurement_unit']
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        default=Ingredient.objects.all(),
        source='ingredient_id'
    )
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', 'name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    author = UserSerializer(default=serializers.CurrentUserDefault())
    image = Base64ImageField()
    ingredients = IngredientSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart')
        model = Recipe

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["tags"] = TagSerializer(instance.tags.all(), many=True).data
        rep["ingredients"] = RecipeIngredientSerializer(
            instance.recipe_ingredient.all(), many=True).data
        return rep

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return user.is_anonymous and Favorite.objects.filter(
            user=user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return user.is_anonymous and Shopping_Cart.objects.filter(
            user=user, recipe=obj.id
        ).exists()

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.filter(
                id=ingredient['id'].id).first()
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.tags.set(tags)
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.filter(
                id=ingredient['id'].id).first()
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=instance,
                amount=ingredient['amount']
            )
        return super().update(instance, validated_data)


class RecipeFollowSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class FavoriteSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )
        model = User

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return request.user.is_anonymous and Subscribe.objects.filter(
            user=request.user, author=obj
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj)
        if recipes_limit:
            queryset = queryset[:int(recipes_limit)]
        return RecipeFollowSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()
