from django.db import models
from PIL import Image

# Create your models here.
class Member(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='名')
    last_name = models.CharField(max_length=50, verbose_name='姓')
    username = models.CharField(max_length=50, unique=True, verbose_name='帳號')
    password = models.CharField(max_length=128, verbose_name='密碼')
    def __str__(self):
        return self.username

class Restaurant(models.Model):
    name = models.CharField(max_length=100, verbose_name='店名')
    address = models.CharField(max_length=255, verbose_name='地址')
    img = models.ImageField(upload_to='restaurant_images/', verbose_name='圖片')
    def __str__(self):
        return self.name
    def get_rating(self):
        star = 0
        sale = 0
        for i in self.menu_items.all():
            star += i.stars
            sale += i.sales
        if sale == 0:
            return 0
        return round(star / sale, 1)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.img.path)
        aspect_ratio = 7 / 5
        img_width, img_height = img.size

        if img_width / img_height != aspect_ratio:
            if img_width / img_height > aspect_ratio:
                new_width = int(img_height * aspect_ratio)
                new_height = img_height
            else:
                new_width = img_width
                new_height = int(img_width / aspect_ratio)

            left = (img_width - new_width) / 2
            top = (img_height - new_height) / 2
            right = (img_width + new_width) / 2
            bottom = (img_height + new_height) / 2

            img = img.crop((left, top, right, bottom))
            img.save(self.img.path)

class Food(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items', verbose_name='店家')
    name = models.CharField(max_length=100, verbose_name='菜名')
    price = models.IntegerField(default=0, verbose_name='售價')
    stars = models.IntegerField(default=0, verbose_name='總星數')
    sales = models.IntegerField(default=0, verbose_name='總銷售量')
    img = models.ImageField(upload_to='food_images/', verbose_name='圖片')
    def __str__(self):
        return self.name
    def get_rating(self):
        if self.sales == 0:
            return 0
        else:
            return round(self.stars / self.sales, 1)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.img.path)
        aspect_ratio = 7 / 5
        img_width, img_height = img.size

        if img_width / img_height != aspect_ratio:
            if img_width / img_height > aspect_ratio:
                new_width = int(img_height * aspect_ratio)
                new_height = img_height
            else:
                new_width = img_width
                new_height = int(img_width / aspect_ratio)

            left = (img_width - new_width) / 2
            top = (img_height - new_height) / 2
            right = (img_width + new_width) / 2
            bottom = (img_height + new_height) / 2

            img = img.crop((left, top, right, bottom))
            img.save(self.img.path)

class CartItem(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='cart_items', null=True, verbose_name='會員')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name='品項')
    quantity = models.IntegerField(verbose_name='數量')
    def __str__(self):
        return f"{self.member.username} {self.food.name} {self.quantity}"

class OrderItem(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='order_items', null=True, verbose_name='會員')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name='品項')
    quantity = models.IntegerField(verbose_name='數量')
    def __str__(self):
        return f"{self.member.username} {self.food.name} {self.quantity}"