from django.db import models
from uuid import uuid4
from django.core.files import File
from PIL import Image
from io import BytesIO
from django_extensions.db.models import TitleSlugDescriptionModel,AutoSlugField,TimeStampedModel
# Create your models here.


class Category(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,null=False,default=uuid4)
    title = models.CharField(max_length=225)
    slug = AutoSlugField(populate_from='title')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    
class Subcategory(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,null=False,default=uuid4)
    title = models.CharField(max_length=225)
    slug = AutoSlugField(populate_from='title')
    category = models.ForeignKey(Category,related_name='subCategories',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Sub Categories'
        verbose_name = 'subCategory'

    def __str__(self):
        return self.title


class Product(TitleSlugDescriptionModel,TimeStampedModel,models.Model):
    id = models.UUIDField(primary_key=True,editable=False,null=False,default=uuid4)
    subcategory = models.ForeignKey(Subcategory,related_name='products',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.title
    
    
    @property
    def category(self):
        return self.sub_category.category


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True,editable=False,null=False,default=uuid4)
    image = models.ImageField(blank=True,null=True)
    thumbnail = models.ImageField(blank=True,null=True)
    product = models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
    def make_thumbnail(self,size=(300,200)):
        img = Image.open(self.image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG',quality=90)

        thumbnail = File(thumb_io,name=self.image.name)
        self.thumbnail = thumbnail