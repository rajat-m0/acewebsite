from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Setting(models.Model):

    TYPE_INT = 1
    TYPE_FLOAT = 2
    TYPE_CHAR = 3
    TYPE_ARRAY = 4
    TYPE_OBJECT = 5

    VALUE_TYPES = (
        (TYPE_INT, "Integer"),
        (TYPE_FLOAT, "Float"),
        (TYPE_CHAR, "Char/String"),
        (TYPE_ARRAY, "Array"),
        (TYPE_OBJECT, "Object"),
    )

    key_name = models.CharField(_("Property Name"), max_length=50, unique=True)
    key_val = models.CharField(_("Property Value"), max_length=500)
    # val_type = models.IntegerField(_("Type of Value"), max_length=10, choices=VALUE_TYPES, default=TYPE_CHAR)

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)
