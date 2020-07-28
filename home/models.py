from django.db import models

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    subcategory = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    img = models.ImageField(upload_to='home/images')
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.product_name
    

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=50)

    def __str__(self):
        return f'{self.name} by {self.email}'




class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=14)
    email = models.EmailField(max_length=70, default="")
    amount = models.CharField(max_length=10)
    address = models.CharField(max_length=150, default="")
    address2 = models.CharField(max_length=150, default="")
    city = models.CharField(max_length=50, default="")
    state = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=5)

    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
    