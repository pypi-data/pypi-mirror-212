import { Application } from '@hotwired/stimulus';

import MapController from './controllers/map';

if (!window.Stimulus) {
  window.Stimulus = Application.start();
}

window.Stimulus.register('map', MapController);
