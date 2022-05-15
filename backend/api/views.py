from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Recipe, Shopping_Cart, Tag

from .filters import IngredientSearchFilter, RecipeFilter
from .pagination import LimitPageNumberPagination
from .permissions import AuthorOrReadOnly
from .serializers import (IngredientSerializer, RecipeFollowSerializer,
                          RecipeSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = (AuthorOrReadOnly,)
    filterset_class = RecipeFilter

    @action(
        url_path='download_shopping_cart',
        detail=False,
        permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        ingredients = Shopping_Cart.objects.filter(
            user=request.user
        ).values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(amount=Sum('recipe__recipe_ingredient__amount'))
        shopping_cart = 'Ваш список покупок: \n'
        for ingredient in ingredients:
            shopping_cart += (
                f'{ingredient["recipe__ingredients__name"]} '
                f'({ingredient["recipe__ingredients__measurement_unit"]}) - '
                f'{ingredient["amount"]} \n\n'
            )
        shopping_cart += '@Продуктовый помощник'
        filename = "Список_покупок.txt"
        response = HttpResponse(shopping_cart, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeFollowSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if Favorite.objects.filter(user=request.user, recipe=recipe).exists():
            return Response(
                data={'detail': 'Вы уже подписаны на этого автора!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Favorite.objects.create(user=request.user, recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                data={'detail': 'Вы ещё не подписаны на этот рецепт!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite = Favorite.objects.filter(user=user, recipe=recipe)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Shopping_CartViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeFollowSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if Shopping_Cart.objects.filter(
            user=request.user, recipe=recipe
        ).exists():
            return Response(
                data={'detail': 'Вы уже добавили этот рецепт!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Shopping_Cart.objects.create(user=request.user, recipe=recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if not Shopping_Cart.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                data={'detail': 'Вы ещё не добавили этот рецепт!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        cart = Shopping_Cart.objects.filter(user=user, recipe=recipe)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
