from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField('Тег', max_length=200)
    color = models.CharField(
        'Цвет', max_length=7, default='#000000'
    )
    slug = models.SlugField(max_length=200)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        ordering = ('name', )
        constraints = (
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique ingredient',
            ),)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField('Картика', upload_to='recipes/')
    text = models.TextField('Описание')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientQuantity',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class IngredientQuantity(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='quantity'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='quantity'
    )
    quantity = models.PositiveSmallIntegerField()


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='carts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='carts'
    )
