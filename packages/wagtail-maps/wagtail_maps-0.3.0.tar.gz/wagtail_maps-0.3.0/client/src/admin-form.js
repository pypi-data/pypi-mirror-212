import { Application } from '@hotwired/stimulus';

import GeoCoordinatesController from './controllers/geo-coordinates';
import MapCenterCoordinatesController from './controllers/map-center-coordinates';

window.Stimulus = Application.start();

window.Stimulus.register('geo-coordinates', GeoCoordinatesController);
window.Stimulus.register('map-center-coordinates', MapCenterCoordinatesController);
