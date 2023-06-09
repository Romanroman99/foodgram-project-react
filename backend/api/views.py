from django.http import HttpResponse
from djoser.views import UserViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.response import Response
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .serializers import (CustomUserSerializer, SubscriptionSerializer,
                          TagSerializer, ShoppingCartSerializer,
                          IngredientSerializer, RecipeSerializer,
                          RecipeListSerializer, FavoriteSerializer)
from users.models import User, Subscribers
from recipes.models import (Tag, Recipe, Ingredient,
                            IngredientQuantity, ShoppingCart, Favorites)
from backend.settings import MEDIA_ROOT
from .filters import RecipeFilter, IngredientFilter
from .permissions import IsAuthorOrReadOnly
from .pagination import CustomPageNumberPagination


class CustomUserViewSet(UserViewSet):
    """ViewSet для работы с полбзователями"""
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class SubscribersView(APIView):
    """Управление подписками"""
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'error': 'Нельзя подписаться на себя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscribers.objects.filter(
                user=request.user,
                author_id=user_id
        ).exists():
            return Response(
                {'error': 'Вы уже подписаны на автора!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = get_object_or_404(User, id=user_id)
        Subscribers.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Subscribers.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на автора'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SubscriptionView(ListAPIView):
    """Список подписок"""
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(subscribe__user=self.request.user)


class TagsViewSet(ReadOnlyModelViewSet):
    """Работает с тэгами"""
    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Работает с тегами"""
    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = IngredientSerializer
    filter_backends = (IngredientFilter, )
    search_fields = ('^name',)
    pagination_class = None


class RecipesViewSet(ModelViewSet):
    """Управления рецептами"""
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthorOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        recipe_obj = get_object_or_404(model, user=user, recipe=recipe)
        recipe_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorites
        )

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if ShoppingCart.objects.filter(
            user=request.user,
            recipe=pk
        ).exists():
            return Response(
                {'error': 'Рецепт уже в списке покупок!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return self.post_method_for_actions(
            request=request,
            pk=pk,
            serializers=ShoppingCartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        item_list = {}
        ingredients = IngredientQuantity.objects.filter(
            recipe__carts__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount'
        )
        for item in ingredients:
            name = item[0]
            if name not in item_list:
                item_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                item_list[name]['amount'] += item[2]

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_cart.pdf"')
        return create_pdf(response, item_list)


def create_pdf(obj, item_list):
    """Создание pdf со списком покупок"""
    pdfmetrics.registerFont(TTFont(
        'TimesNewRoman', MEDIA_ROOT + '/data/TimesNewRoman.ttf', 'UTF-8'
    ))
    page = canvas.Canvas(obj)
    page.setFont('TimesNewRoman', size=20)
    page.drawString(250, 780, 'Список покупок')
    page.setFont('TimesNewRoman', size=12)
    height = 725
    for i, (name, data) in enumerate(item_list.items(), 1):
        page.drawString(70, height, (f'{i}. {name}: {data["amount"]} '
                                     f'{data["measurement_unit"]}'))
        height -= 25
    page.showPage()
    page.save()
    return obj
