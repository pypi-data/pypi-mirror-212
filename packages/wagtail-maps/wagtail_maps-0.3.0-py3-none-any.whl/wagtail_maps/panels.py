from wagtail.admin.panels import PanelGroup


class MapCenterCoordinatesPanel(PanelGroup):
    class BoundPanel(PanelGroup.BoundPanel):
        template_name = 'wagtail_maps/panels/map_center_coordinates.html'


class PointCoordinatesPanel(PanelGroup):
    class BoundPanel(PanelGroup.BoundPanel):
        template_name = 'wagtail_maps/panels/point_coordinates.html'

        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)
            context['dialog_id'] = '%s-dialog' % self.prefix
            return context
