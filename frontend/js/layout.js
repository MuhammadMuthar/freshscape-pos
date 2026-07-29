// FreshScape Market POS -- shared app shell
// Renders the sidebar into #sidebar-root so nav/user-info/logout
// logic lives in one place instead of copy-pasted per page.
// Relies on pathToRoot() and api/auth/toast from api.js, which
// must be loaded before this file.

const NAV_ITEMS = [
  { key: 'dashboard', label: 'Dashboard', href: '{root}index.html' },
  { key: 'products', label: 'Products', href: '{root}pages/products.html' },
  { key: 'categories', label: 'Categories', href: '{root}pages/categories.html' },
  { key: 'inventory', label: 'Inventory', href: '{root}pages/inventory.html' },
  { key: 'purchase-orders', label: 'Purchase Orders', href: '{root}pages/purchase-orders.html' },
  { key: 'suppliers', label: 'Suppliers', href: '{root}pages/suppliers.html' },
  { key: 'sales', label: 'Sales / POS', href: '{root}pages/sales.html' },
  { key: 'customers', label: 'Customers', href: '{root}pages/customers.html' },
  { key: 'returns', label: 'Returns', href: '{root}pages/returns.html' },
];

function renderShell(activeKey) {
  const root = pathToRoot();

  const navHtml = NAV_ITEMS.map(item => {
    const href = item.href.replace('{root}', root);
    const activeClass = item.key === activeKey ? ' is-active' : '';
    return `<a class="sidebar__link${activeClass}" href="${href}">${item.label}</a>`;
  }).join('');

  const shellHtml = `
    <aside class="sidebar">
      <div class="sidebar__brand">
        FreshScape
        <span>Market POS</span>
      </div>
      <nav class="sidebar__nav">${navHtml}</nav>
      <div class="sidebar__footer">
        <div class="sidebar__user" id="sidebar-user">
          <strong>&hellip;</strong>
        </div>
        <button class="sidebar__logout" onclick="auth.logout()">Log out</button>
      </div>
    </aside>
  `;

  document.getElementById('sidebar-root').outerHTML = shellHtml;

  api.get('/auth/me').then(user => {
    const el = document.getElementById('sidebar-user');
    if (el) {
      el.innerHTML = `
        <strong>${user.username}</strong>
        <span class="sidebar__role">${user.role}</span>
      `;
    }
  }).catch(() => {});
}

document.addEventListener('DOMContentLoaded', () => {
  auth.requireAuth();
  const page = document.body.dataset.page;
  if (page) renderShell(page);
});
