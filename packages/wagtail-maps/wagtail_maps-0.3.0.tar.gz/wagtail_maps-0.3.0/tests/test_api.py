from django.urls import reverse

import pytest
from bs4 import BeautifulSoup
from rest_framework.test import APIClient

from wagtail_maps.models import Map, Point

from .factories import PointFactory

MAP_POINT_LAT = '50.9523'
MAP_POINT_LON = '1.8689'


@pytest.fixture
def map_example(root_page):
    return Map.objects.create(
        name="Map example",
        center_latitude=MAP_POINT_LAT,
        center_longitude=MAP_POINT_LON,
        points=[
            Point(
                title="Point 1",
                latitude=MAP_POINT_LAT,
                longitude=MAP_POINT_LON,
            ),
            Point(
                title="Point 2",
                page_link=root_page,
                latitude=MAP_POINT_LAT,
                longitude=MAP_POINT_LON,
            ),
            Point(
                title="Point 3",
                external_link='https://example.org',
                latitude=MAP_POINT_LAT,
                longitude=MAP_POINT_LON,
            ),
        ],
    )


@pytest.mark.django_db
class TestMapsAPIViewSet:
    @classmethod
    def setup_class(cls):
        cls.client = APIClient(enforce_csrf_checks=True)

    def get_detail_url(self, item_id):
        return reverse('wagtail_maps:api:map-detail', args=(item_id,))

    def get_detail_response(self, item_id, data=None):
        return self.client.get(self.get_detail_url(item_id), data)

    # Tests

    def test_detail(self, map_example):
        response = self.get_detail_response(map_example.id)
        assert response.status_code == 200
        assert response.json() == {
            'id': 1,
            'name': 'Map example',
            'points': [
                {
                    'title': 'Point 1',
                    'content': '',
                    'url': '',
                    'latitude': MAP_POINT_LAT,
                    'longitude': MAP_POINT_LON,
                },
                {
                    'title': 'Point 2',
                    'content': '',
                    'url': 'http://localhost/',
                    'latitude': MAP_POINT_LAT,
                    'longitude': MAP_POINT_LON,
                },
                {
                    'title': 'Point 3',
                    'content': '',
                    'url': 'https://example.org',
                    'latitude': MAP_POINT_LAT,
                    'longitude': MAP_POINT_LON,
                },
            ],
        }

    def test_detail_content_expanded(self, map_example, root_page):
        PointFactory(
            title='Point title',
            content='<p>Lorem <a id="{}" linktype="page">ipsum</a></p>'.format(
                root_page.id
            ),
            map_id=map_example.id,
        )
        points = self.get_detail_response(map_example.id).json()['points']
        content = BeautifulSoup(points[-1]['content'], 'html5lib')
        assert content.select_one('h5', text='Point title')
        assert content.select_one('p', text='Lorem')
        link = content.select_one('a', tex_t='ipsum')
        assert link['href'] == root_page.url

    def test_detail_content_with_url(self, map_example):
        PointFactory(
            title='Point with link',
            external_link='https://example.org',
            map_id=map_example.id,
        )
        points = self.get_detail_response(map_example.id).json()['points']
        content = BeautifulSoup(points[-1]['content'], 'html5lib')
        title = content.select_one('a', text='Point with link')
        assert title['href'] == 'https://example.org'
