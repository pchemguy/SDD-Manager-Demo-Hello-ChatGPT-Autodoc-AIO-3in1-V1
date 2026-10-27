(function () {
  'use strict';
  const mounted = new WeakMap();
  const values = ['red', 'blue', 'green'];
  function mount(root) {
    if (mounted.has(root)) return mounted.get(root);
    const message = root.querySelector('#message');
    const group = root.querySelector('#colors');
    const inputs = Array.from(group.querySelectorAll('input[name="color"]'));
    let color = 'red';
    function paint() {
      inputs.forEach(input => { input.checked = input.value === color; });
      message.style.color = color;
    }
    function change(event) {
      if (inputs.includes(event.target) && values.includes(event.target.value)) color = event.target.value;
      paint();
    }
    const controller = {
      reset() { color = 'red'; paint(); },
      dispose() { group.removeEventListener('change', change); mounted.delete(root); }
    };
    group.addEventListener('change', change);
    mounted.set(root, controller);
    controller.reset();
    return controller;
  }
  window.HelloColorApp = Object.freeze({ mount });
}());
