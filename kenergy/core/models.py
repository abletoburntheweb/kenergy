from django.db import models

class Inventory(models.Model):
    id_i = models.AutoField(primary_key=True)
    название = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.название


class Groups(models.Model):
    id_g = models.AutoField(primary_key=True)
    id_i = models.ForeignKey(Inventory, on_delete=models.CASCADE, db_column="id_i_id")
    название = models.CharField(max_length=255, null=False)

    objects = models.Manager()  # Убедитесь, что эта строка присутствует

    class Meta:
        unique_together = ('id_i', 'название')

    def __str__(self):
        return f"{self.название} (Группа)"

class Object(models.Model):
    id_o = models.AutoField(primary_key=True)
    название = models.CharField(max_length=255)
    id_g = models.ForeignKey(Groups, on_delete=models.CASCADE, db_column='id_g_id')

    class Meta:
        unique_together = ('id_g', 'название')

    def __str__(self):
        return f"{self.название} (Объект)"

class Tests(models.Model):
    id_def = models.AutoField(primary_key=True)
    id_o = models.ForeignKey(Object, on_delete=models.CASCADE, db_column='id_o_id')
    испытание = models.TextField(null=False)
    метрика = models.FloatField(null=False)
    рекомендация = models.TextField(null=False)

    def __str__(self):
        return f"Испытание: {self.испытание}"

class Standards(models.Model):
    id_s = models.AutoField(primary_key=True)
    id_o = models.ForeignKey(Object, on_delete=models.CASCADE, db_column='id_o_id')
    стандарт = models.TextField(null=False)
    требование = models.TextField(null=False)

    def __str__(self):
        return f"Стандарт: {self.стандарт}"