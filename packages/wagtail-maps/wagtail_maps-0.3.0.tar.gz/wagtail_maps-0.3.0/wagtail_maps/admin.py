from django.utils.translation import gettext_lazy as _

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.panels import FieldPanel, InlinePanel, PageChooserPanel
from wagtail.contrib.modeladmin.options import ModelAdmin

from .models import Map
from .panels import MapCenterCoordinatesPanel, PointCoordinatesPanel


class MapAdmin(ModelAdmin):
    model = Map
    menu_icon = 'map'
    list_display = ('name', 'points_count')
    form_view_extra_css = ['wagtail_maps/css/admin-form.css']
    form_view_extra_js = [
        'wagtail_maps/js/admin-form.js'
        if WAGTAIL_VERSION[0] < 5
        else 'wagtail_maps/js/admin-form_controllers.js'
    ]

    panels = [
        FieldPanel('name', classname='title'),
        MapCenterCoordinatesPanel(
            [
                FieldPanel('center_latitude', heading=_("Latitude")),
                FieldPanel('center_longitude', heading=_("Longitude")),
            ],
            heading=_("Center of the map"),
        ),
        InlinePanel(
            'points',
            panels=[
                FieldPanel('title'),
                FieldPanel('content'),
                PageChooserPanel('page_link'),
                FieldPanel('external_link'),
                PointCoordinatesPanel(
                    [FieldPanel('latitude'), FieldPanel('longitude')]
                ),
            ],
            heading=_("Points"),
            label=_("Point"),
            min_num=1,
        ),
    ]

    def points_count(self, obj):
        return obj.points.count()

    points_count.short_description = _("Points")
