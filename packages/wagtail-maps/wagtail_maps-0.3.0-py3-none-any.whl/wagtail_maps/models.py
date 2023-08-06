from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from wagtail.fields import RichTextField

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


class Map(ClusterableModel):
    name = models.CharField(verbose_name=_("name"), max_length=30)

    center_latitude = models.DecimalField(
        verbose_name=_("center point's latitude"),
        max_digits=7,
        decimal_places=4,
    )
    center_longitude = models.DecimalField(
        verbose_name=_("center point's longitude"),
        max_digits=7,
        decimal_places=4,
    )

    class Meta:
        verbose_name = _("map")
        verbose_name_plural = _("maps")

    def __str__(self):
        return self.name


class Point(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=50)
    content = RichTextField(
        verbose_name=_("content"),
        blank=True,
        features=['bold', 'italic', 'ol', 'ul', 'link'],
    )
    page_link = models.ForeignKey(
        'wagtailcore.Page',
        verbose_name=_("link to a page"),
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL,
    )
    external_link = models.URLField(
        verbose_name=_("link to an URL"),
        blank=True,
    )

    latitude = models.DecimalField(
        verbose_name=_("latitude"),
        max_digits=7,
        decimal_places=4,
    )
    longitude = models.DecimalField(
        verbose_name=_("longitude"),
        max_digits=7,
        decimal_places=4,
    )

    map = ParentalKey('Map', on_delete=models.CASCADE, related_name='points')

    class Meta:
        verbose_name = _("point")
        verbose_name_plural = _("points")

    def clean(self):
        if self.page_link and self.external_link:
            msg = gettext("Choose between a link to a page or an URL.")
            raise ValidationError({'page_link': msg, 'external_link': msg})
