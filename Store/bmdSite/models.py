from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator
# Create your models here.


class Store(models.Model):
    name=models.CharField(null=False, max_length=100)
    image=models.ImageField(upload_to="images", null=True)
    address=models.CharField(null=False, max_length=200)
    slug= models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return f"{self.name}"


class Type_Article(models.Model):
    name=models.CharField(null=False, max_length=100)
    price=models.FloatField(null=True, validators=[MinValueValidator(0.1)])
    image=models.ImageField(upload_to="images", null=True)
    text=models.TextField(validators=[MinLengthValidator(10)] )


    def __str__(self):
        return f"{self.name}"


class Article(models.Model):
    store=models.ForeignKey(Store,null=True,on_delete=models.SET_NULL, related_name="store")
    type_arttcle=models.ForeignKey(Type_Article,on_delete=models.CASCADE, null=False, related_name="type_article")
    quantity=models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.type_arttcle}"
    
    def get_store(self):
        return self.sotore.name
    
    def get_type_article(self):
        return self.type_arttcle.name


