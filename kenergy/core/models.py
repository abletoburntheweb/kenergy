from django.db import models

class Inventory(models.Model):
    id_i = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Groups(models.Model):
    id_g = models.AutoField(primary_key=True)
    id_i = models.ForeignKey(Inventory, on_delete=models.CASCADE, db_column='id_i')
    name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('id_i', 'name')

    def __str__(self):
        return self.name


class Object(models.Model):
    id_o = models.AutoField(primary_key=True)
    id_g = models.ForeignKey(Groups, on_delete=models.CASCADE, db_column='id_g')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('id_g', 'name')

    def __str__(self):
        return self.name


class FactsDefects(models.Model):
    id_def = models.AutoField(primary_key=True)
    id_o = models.ForeignKey(Object, on_delete=models.CASCADE, db_column='id_o')
    fact = models.TextField()
    criticality = models.BooleanField(default=False)
    recommendation = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fact


class FactsStandards(models.Model):
    id_s = models.AutoField(primary_key=True)
    id_o = models.ForeignKey(Object, on_delete=models.CASCADE, db_column='id_o')
    fact = models.TextField()

    def __str__(self):
        return self.fact


class FactsDetermination(models.Model):
    id_d = models.AutoField(primary_key=True)
    id_o = models.ForeignKey(Object, on_delete=models.CASCADE, db_column='id_o')
    fact_name = models.CharField(max_length=255)

    def __str__(self):
        return self.fact_name

class Defect(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
