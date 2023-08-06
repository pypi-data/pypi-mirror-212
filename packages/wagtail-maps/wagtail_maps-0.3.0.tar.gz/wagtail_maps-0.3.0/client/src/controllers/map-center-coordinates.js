import { Controller } from '@hotwired/stimulus';

function isNumber(value) {
  return value === Number(value).toString();
}

function add(accumulator, a) {
  return accumulator + a;
}

export default class extends Controller {
  static values = {
    pointSelector: {
      type: String,
      default: '#id_points-FORMS > :not(.deleted)',
    },
  };

  connect() {
    this.latInput = this.element.querySelector('[name="center_latitude"]');
    this.lngInput = this.element.querySelector('[name="center_longitude"]');
  }

  // Targets

  static targets = ['errorMessage'];

  errorMessageTargetConnected(element) {
    element.setAttribute('hidden', '');
  }

  // Actions

  calculate() {
    const lat = [];
    const lng = [];

    this.errorMessageTarget.setAttribute('hidden', '');

    // iterate over points and append its latitude and longitude
    document.querySelectorAll(this.pointSelectorValue).forEach((child) => {
      const latitude = child.querySelector('[name$=-latitude]').value;
      const longitude = child.querySelector('[name$=-longitude]').value;

      if (isNumber(latitude) && isNumber(longitude)) {
        lat.push(Number(latitude));
        lng.push(Number(longitude));
      }
    });

    if (!lat.length) {
      this.errorMessageTarget.removeAttribute('hidden');
      return;
    }

    this.latInput.value = lat.reduce(add) / lat.length;
    this.lngInput.value = lng.reduce(add) / lng.length;
  }
}
