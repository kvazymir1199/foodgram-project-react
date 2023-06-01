from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name="Тег", help_text="Тег")
    color = models.CharField(
        max_length=7, validators=[RegexValidator(r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")]
    )
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return f"{self.name} --> {self.color} -->{self.slug}"
