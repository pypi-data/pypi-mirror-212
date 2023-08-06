import GeoCoordinatesController from './controllers/geo-coordinates';
import MapCenterCoordinatesController from './controllers/map-center-coordinates';

if (!window.Stimulus) {
  throw new Error("You must instantiate a Stimulus application at first.");
}

window.Stimulus.register('geo-coordinates', GeoCoordinatesController);
window.Stimulus.register('map-center-coordinates', MapCenterCoordinatesController);
