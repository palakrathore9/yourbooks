from django.db import models

# Create your models here.
class popular(models.Model):
    Book_Title	= models.CharField(max_length=150)
    Book_Author	= models.CharField(max_length=150)
    Image_URL_M	= models.URLField()
    num_ratings	= models.IntegerField()
    avg_rating = models.DecimalField(decimal_places=10,max_digits=30)
