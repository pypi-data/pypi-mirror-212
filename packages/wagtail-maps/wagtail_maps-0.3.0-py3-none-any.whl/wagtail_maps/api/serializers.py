from django.template.loader import get_template

from rest_framework import serializers

from ..models import Map, Point


class PointSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = Point
        fields = ['title', 'content', 'url', 'latitude', 'longitude']

    def get_url(self, obj):
        if obj.page_link:
            return obj.page_link.get_full_url(self.context['request'])
        return obj.external_link

    def get_content(self, obj):
        return (
            get_template('wagtail_maps/popup_content.html')
            .render(
                {
                    'title': obj.title,
                    'content': obj.content,
                    'url': self.get_url(obj),
                }
            )
            .strip()
        )


class MapSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Map
        fields = ['id', 'name', 'points']
