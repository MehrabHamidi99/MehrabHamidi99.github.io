'use strict';
document.body.classList.add('js');
const themeToggle = document.querySelector('.theme-toggle');
const systemTheme = window.matchMedia('(prefers-color-scheme: dark)');
const savedTheme = () => {
  try { return localStorage.getItem('mehrab-theme'); } catch (_) { return null; }
};
const applyTheme = theme => {
  document.documentElement.dataset.theme = theme;
  document.querySelector('meta[name="theme-color"]').content = theme === 'dark' ? '#131c19' : '#f8f8f3';
  if (themeToggle) {
    const label = theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    themeToggle.setAttribute('aria-label', label);
    themeToggle.title = label;
  }
};
if (themeToggle) {
  themeToggle.hidden = false;
  applyTheme(document.documentElement.dataset.theme || (systemTheme.matches ? 'dark' : 'light'));
  themeToggle.addEventListener('click', () => {
    const theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('mehrab-theme', theme); } catch (_) {}
    applyTheme(theme);
  });
  systemTheme.addEventListener('change', event => {
    if (!['light', 'dark'].includes(savedTheme())) applyTheme(event.matches ? 'dark' : 'light');
  });
}
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
