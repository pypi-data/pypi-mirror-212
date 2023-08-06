import { Controller } from '@hotwired/stimulus';

const RE_GEO_URI =
  /^geo:([-+]?\d+(?:\.\d+)?),([-+]?\d+(?:\.\d+)?)(?:\?z=(\d{1,2}))?$/;

const HIDE_EVENT = new Event('wagtail:hide');

export default class extends Controller {
  static values = {
    dialogId: String,
    prefix: String,
  };

  // Targets

  static targets = ['errorMessage', 'input'];

  errorMessageTargetConnected(element) {
    element.setAttribute('hidden', '');
  }

  // Actions

  set() {
    this.errorMessageTarget.setAttribute('hidden', '');

    const geoMatch = this.inputTarget.value.match(RE_GEO_URI);

    if (!geoMatch) {
      this.errorMessageTarget.removeAttribute('hidden');
      return;
    }

    const latInput = document.querySelector(`[name="${this.prefixValue}-latitude"]`);
    const lngInput = document.querySelector(`[name="${this.prefixValue}-longitude"]`);

    latInput.value = Number(geoMatch[1]);
    lngInput.value = Number(geoMatch[2]);

    if (this.dialogIdValue) {
      document.getElementById(this.dialogIdValue).dispatchEvent(HIDE_EVENT);
    }
  }
}
