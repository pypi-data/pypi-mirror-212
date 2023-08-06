from wagtail.contrib.modeladmin.helpers import AdminURLHelper
from wagtail.test.utils.form_data import inline_formset, nested_form_data

import pytest
from bs4 import BeautifulSoup

from wagtail_maps.models import Map

from .factories import MapFactory


@pytest.mark.django_db
class TestMapAdminViews:
    url_helper = AdminURLHelper(Map)

    @property
    def index_url(self):
        return self.url_helper.index_url

    @property
    def create_url(self):
        return self.url_helper.create_url

    def get_edit_url(self, pk):
        return self.url_helper.get_action_url('edit', instance_pk=pk)

    # Tests

    def test_index(self, admin_client):
        MapFactory.create_batch(2)

        response = admin_client.get(self.index_url)
        assert response.status_code == 200
        soup = BeautifulSoup(response.content, 'html5lib')
        rows = soup.select('[data-object-pk]')
        assert len(rows) == 2
        assert rows[0].select_one('.field-points_count').text == '3'

    def test_create(self, admin_client, root_page):
        response = admin_client.get(self.create_url)
        assert response.status_code == 200

        data = nested_form_data(
            {
                'name': "Map example",
                'center_latitude': '50.9523',
                'center_longitude': '1.8689',
                'points': inline_formset(
                    [
                        {
                            'title': "Foo",
                            'latitude': '50.9523',
                            'longitude': '1.8689',
                            'page_link': root_page.id,
                        }
                    ]
                ),
            }
        )
        response = admin_client.post(self.create_url, data)
        assert response.status_code == 302

        instance = Map.objects.get(name="Map example")
        points = instance.points.all()
        assert len(points) == 1
        assert points[0].page_link == root_page

        response = admin_client.get(self.get_edit_url(instance.pk))
        assert response.status_code == 200

    def test_create_multiple_link_error(self, admin_client, root_page):
        data = nested_form_data(
            {
                'name': "Map example",
                'center_latitude': '50.9523',
                'center_longitude': '1.8689',
                'points': inline_formset(
                    [
                        {
                            'title': "Foo",
                            'latitude': '50.9523',
                            'longitude': '1.8689',
                            'page_link': root_page.id,
                            'external_link': 'https://example.org',
                        }
                    ]
                ),
            }
        )
        response = admin_client.post(self.create_url, data)
        assert response.status_code == 200
        formset = response.context['form'].formsets['points']
        assert set(formset.errors[0].keys()) == {'page_link', 'external_link'}
