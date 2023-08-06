from django.core.exceptions import ValidationError

import pytest
from pytest_django.asserts import assertHTMLEqual

from wagtail_maps.blocks import MapBlock

from .factories import MapFactory


@pytest.mark.django_db
class TestMapBlock:
    @pytest.fixture(autouse=True)
    def setup_block(self):
        self.block = MapBlock()
        self.block.set_name('test_mapblock')

    def render(self, data):
        return self.block.render(self.block.to_python(data))

    def test_form_response_map(self):
        maps = MapFactory.create_batch(2)

        value = self.block.value_from_datadict({'p-map': maps[1].pk}, {}, 'p')
        assert value['map'] == maps[1]

    @pytest.mark.parametrize('value', ('', None, '10'))
    def test_form_response_map_none(self, value):
        MapFactory.create_batch(2)

        value = self.block.value_from_datadict({'p-map': value}, {}, 'p')
        assert value['map'] is None

    def test_get_form_state(self):
        assert self.block.get_form_state(
            {'map': 1, 'height': 400, 'zoom': 1}
        ) == {'height': '400', 'map': ['1'], 'zoom': '1'}

    def test_render(self):
        assertHTMLEqual(
            self.render(
                {
                    'map': MapFactory(
                        center_latitude=0.0, center_longitude=1.0
                    ).id
                }
            ),
            """
            <div class="map" data-controller="map"
              data-map-api-url-value="/maps/api/v1/1/"
              data-map-center-value="[0.0, 1.0]">
            </div>
            """,
        )

    def test_render_with_attrs(self):
        assertHTMLEqual(
            self.render(
                {
                    'map': MapFactory(
                        center_latitude=0.0, center_longitude=1.0
                    ).id,
                    'min_zoom': '2',
                    'max_zoom': '10',
                    'zoom': '1',
                    'height': '10',
                }
            ),
            """
            <div class="map" data-controller="map"
              data-map-api-url-value="/maps/api/v1/1/"
              data-map-center-value="[0.0, 1.0]"
              data-map-height-value="10"
              data-map-min-zoom-value="2"
              data-map-max-zoom-value="10"
              data-map-zoom-value="1">
            </div>
            """,
        )

    def test_render_unknown(self):
        assert self.render({'map': '100'}) == ''

    def test_clean_min_max_zoom(self):
        data = {'map': MapFactory().id}

        self.block.clean(data)

        data['min_zoom'] = 10
        self.block.clean(data)

        data['max_zoom'] = 15
        self.block.clean(data)

        with pytest.raises(ValidationError):
            data['max_zoom'] = 5
            self.block.clean(data)
