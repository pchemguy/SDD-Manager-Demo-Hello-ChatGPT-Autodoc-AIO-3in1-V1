(function () {
  'use strict';
  const controller = window.HelloColorApp.mount(document);
  window.addEventListener('pageshow', () => controller.reset());
}());
