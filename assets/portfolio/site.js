'use strict';
document.body.classList.add('js');
const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
if (menu && navigation) {
  menu.hidden = false;
  const closeMenu = () => {
    navigation.classList.remove('is-open');
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', 'Open navigation');
  };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    navigation.classList.toggle('is-open', open);
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      closeMenu(); menu.focus();
    }
  });
  navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
}
const controls = document.querySelector('.publication-controls');
if (controls) {
  controls.hidden = false;
  const search = document.querySelector('#paper-search');
  const papers = [...document.querySelectorAll('[data-paper]')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  let selected = 'All';
  const update = () => {
    const query = search.value.trim().toLocaleLowerCase();
    let count = 0;
    papers.forEach(paper => {
      const visible = (selected === 'All' || paper.dataset.type === selected) && paper.dataset.search.includes(query);
      paper.hidden = !visible;
      count += Number(visible);
    });
    document.querySelector('#paper-count').textContent = `${count} publication${count === 1 ? '' : 's'}`;
    document.querySelector('#no-results').hidden = count !== 0;
  };
  search.addEventListener('input', update);
  filters.forEach(button => button.addEventListener('click', () => {
    selected = button.dataset.filter;
    filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
    update();
  }));
}
const printButton = document.querySelector('.print-button');
if (printButton) { printButton.hidden = false; printButton.addEventListener('click', () => window.print()); }
