import json

from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.functional import cached_property
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.blocks.struct_block import StructBlockValidationError
from wagtail.coreutils import resolve_model_string


def build_map_values(**config):
    return {
        f'data-map-{name}-value': value
        for name, value in config.items()
        if value not in (None, '')
    }


class MapChooserBlock(blocks.ChooserBlock):
    class Meta:
        label = _("Map")

    @cached_property
    def target_model(self):
        return resolve_model_string('wagtail_maps.Map')

    @cached_property
    def widget(self):
        return forms.Select()

    def value_from_form(self, value):
        if value == '':
            return None
        return super().value_from_form(value)

    def get_form_state(self, value):
        return blocks.FieldBlock.get_form_state(self, value)


class MapBlock(blocks.StructBlock):
    map = MapChooserBlock()
    height = blocks.IntegerBlock(
        label=_("Height (px)"),
        required=False,
        min_value=10,
    )
    zoom = blocks.IntegerBlock(
        label=_("Initial zoom"),
        required=False,
        min_value=1,
        max_value=20,
    )
    min_zoom = blocks.IntegerBlock(
        label=_("Minimum zoom level"),
        required=False,
        min_value=1,
        max_value=20,
    )
    max_zoom = blocks.IntegerBlock(
        label=_("Maximum zoom level"),
        required=False,
        min_value=1,
        max_value=20,
    )

    class Meta:
        icon = 'map'
        label = _("Map")
        template = 'wagtail_maps/map_block.html'

    def clean(self, value):
        value = super().clean(value)

        min_zoom = value.get('min_zoom')
        max_zoom = value.get('max_zoom')

        if min_zoom and max_zoom and min_zoom > max_zoom:
            # Starting with Wagtail 5, this part can be simplified as only
            # one error is raised - see wagtail.blocks.struct_block
            error_list = ErrorList(
                [
                    ValidationError(
                        gettext(
                            "Minimum zoom level must be smaller than maximum."
                        )
                    )
                ]
            )
            raise StructBlockValidationError(
                {'min_zoom': error_list, 'max_zoom': error_list}
            )

        return value

    def render(self, value, context=None):
        if not value.get('map'):
            return ''
        return super().render(value, context=context)

    def get_context(self, value, **kwargs):
        context = super().get_context(value, **kwargs)
        context['attrs'] = build_map_values(
            **{
                'center': json.dumps(
                    [
                        float(value['map'].center_latitude),
                        float(value['map'].center_longitude),
                    ]
                ),
                'height': value.get('height'),
                'min-zoom': value.get('min_zoom'),
                'max-zoom': value.get('max_zoom'),
                'zoom': value.get('zoom'),
            }
        )
        return context
