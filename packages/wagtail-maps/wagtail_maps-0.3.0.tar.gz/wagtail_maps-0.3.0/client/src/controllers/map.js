import * as L from 'leaflet/dist/leaflet-src.esm';
import { Controller } from '@hotwired/stimulus';

const TileProvider = {
  url: '//{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png',
  options: {
    attribution:
      'donn&eacute;es &copy; <a href="//osm.org/copyright">OpenStreetMap</a>/ODbL - rendu <a href="//openstreetmap.fr">OSM France</a>',
    minZoom: 1,
    maxZoom: 20,
  },
};

export default class extends Controller {
  static values = {
    apiUrl: String,
    center: Array,
    height: {
      type: Number,
      default: 400,
    },
    mapPadding: {
      type: Number,
      default: 10,
    },
    minZoom: Number,
    maxZoom: Number,
    popupOptions: {
      type: Object,
      default: {
        minWidth: 80,
      },
    },
    tooltipOptions: {
      type: Object,
      default: {
        opacity: 1,
      },
    },
    zoom: {
      type: Number,
      default: 8,
    },
  };

  connect() {
    this.element.style.height = `${this.heightValue}px`;

    this.map = L.map(this.element, {
      center: this.centerValue,
      layers: [L.tileLayer(TileProvider.url, TileProvider.options)],
      zoom: this.zoomValue,
    });

    if (this.maxZoomValue) {
      this.map.setMaxZoom(this.maxZoomValue);
    }

    if (this.minZoomValue) {
      this.map.setMinZoom(this.minZoomValue);
    }

    this.featureGroup = L.featureGroup();
    this.featureGroup.addTo(this.map);

    this.fetch();
  }

  /**
   * Clears all the markers from the map.
   */
  clear() {
    this.featureGroup.clearLayers();
  }

  /**
   * Fetches the points from the API and adds them to the map.
   */
  fetch() {
    if (!this.apiUrlValue) {
      throw new Error('No apiUrl value has been defined.');
    }

    this.clear();

    return fetch(this.apiUrlValue)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Unable to fetch data from the API.');
        }

        return response.json();
      })
      .then(({ points }) => {
        points.forEach(this.addMarker.bind(this));
      });
  }

  /**
   * Adds a marker on the map for the given point.
   */
  addMarker(point) {
    const marker = L.marker([point.latitude, point.longitude]);

    if (point.content) {
      marker.bindPopup(point.content, {
        maxHeight: this.heightValue - this.mapPaddingValue * 2,
        ...this.popupOptionsValue,
      });
    } else {
      const content = point.url
        ? `<a href="${point.url}" rel="noopener">${point.title}</a>`
        : point.title;

      marker.bindTooltip(content, this.tooltipOptionsValue);
      marker.off().on('click', () => marker.toggleTooltip());
    }

    this.featureGroup.addLayer(marker);
  }
}
