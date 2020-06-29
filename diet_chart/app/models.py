from django.db import models

# Create your models here.
class Myfooddata(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=200, blank=True, null=True)  # Field name made lowercase.
    food_group = models.CharField(db_column='Food_Group', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fat = models.DecimalField(db_column='Fat', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    protein = models.DecimalField(db_column='Protein', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    carbohydrate = models.DecimalField(db_column='Carbohydrate', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MyFoodData'