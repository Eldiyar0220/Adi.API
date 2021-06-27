from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) #это после запятой decimal
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')

    image = models.ImageField(upload_to='products', blank=True, null=True) #blank=True, null=True делаем необезательным

    def __str__(self):
        return self.title

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    ######
    # only one comment
    class Meta:
        unique_together = ['author', 'product']


# class OrderItems(models.Model):
#     order = models.ForeignKey(Order, )
#

class statusChoices(models.TextChoices):
    new = ('new', 'Новый')
    in_progress = ('in_progress', 'В обработке')
    done = ('done', 'выполнено')
    canceled = ('canceled', 'отменён')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItems')

    status = models.CharField(max_length=50, choices=statusChoices.choices)

    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='order_items')

    quantity = models.PositiveSmallIntegerField(default=1)


    #для количество
    class Meta:
        unique_together = ['order', 'product']
#Лайк бл
class WishList(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    #при нажатии лайкает и удаляется
    is_liked = models.BooleanField(default=False)