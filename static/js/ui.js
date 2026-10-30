document.querySelectorAll('[data-menu-toggle]').forEach((button) => {
    const menu = document.getElementById(button.getAttribute('aria-controls'));
    if (!menu) return;
    button.addEventListener('click', () => {
        const expanded = button.getAttribute('aria-expanded') !== 'true';
        menu.classList.toggle('hidden', !expanded);
        button.setAttribute('aria-expanded', String(expanded));
    });
});

document.querySelectorAll('[data-dismiss-alert]').forEach((button) => {
    button.addEventListener('click', () => button.closest('[role="alert"]').remove());
});
