# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 0.3.0 - 2023-06-07

*Breaking changes:* the JavaScript code to render a `MapBlock` in your frontend
must be updated or replaced by the one which is now provided by this module. As
it uses a Stimulus controller to render the map, the HTML data attributes have
changed - see the [MapController](client/src/controllers/map.js) for all the
expected values.

### Added
- Provide some JavaScript code to render a `MapBlock` in the frontend with
  Leaflet

### Changed
- Add support for Wagtail 4.1 LTS & 5.0 and remove other unmaintained Wagtail
  and Django versions
- Remove `min_zomm` and `max_zoom` from the `Map` model and define them in
  `MapBlock` instead to regroup properties which are related to the rendering

## 0.2.0 - 2021-10-15
### Added
- Set the coordinates of a point from a geo URI

### Changed
- Use Webpack to bundle and minify the JavaScript code

## 0.1.0 - 2021-10-14

This is the initial release which provides the basis - e.g. the models, admin
integration and a block. The frontend part to display a map on your site is
currently not provided, but you can find an example.
