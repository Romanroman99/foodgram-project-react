from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, SubscribersView, SubscriptionView,
                    RecipesViewSet, IngredientsViewSet, TagsViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', CustomUserViewSet, basename='users')
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionView.as_view(),
        name='subscriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        SubscribersView.as_view(),
        name='subscribe'
    ),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
