// static/js/toast.js

// SVG icons (you can swap these for your Lucide imports if you bundle them)
const ICONS = {
  success: `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M9 12l2 2l4-4m6 2a9 9 0 11-18 0a9 9 0 0118 0z" />
            </svg>`,
  error:   `<svg xmlns="http://www.w3.org/2000/svg" class="h-[20px] w-[20px] text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M12 9v2m0 4h.01M5.93 19.07A10 10 0 1119.07 5.93A10 10 0 015.93 19.07z" />
            </svg>`,
  close:   `<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 cursor-pointer transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M6 18L18 6M6 6l12 12" />
            </svg>`
};

export function showToast({ message, type = 'success', duration = 2000 }) {
  const container = document.getElementById('toast-container');
  if (!container) return;

  // build the toast element
  const toast = document.createElement('div');
  toast.className = [
    'flex items-start space-x-3',
    'rounded-lg border-l-4',
    type === 'success' ? 'border-green-500' : 'border-red-500',
    'bg-white dark:bg-gray-800',
    'p-4 shadow-lg backdrop-blur-sm',
    'max-w-sm',
    'opacity-0 translate-y-2 transform transition-all duration-200'
  ].join(' ');

  toast.innerHTML = `
    <div class="flex-shrink-0">${ICONS[type]}</div>
    <div class="flex-1 text-surface-900 dark:text-surface-100">${message}</div>
    <div class="flex-shrink-0 close-btn">${ICONS.close}</div>
  `;

  container.appendChild(toast);
  // trigger the enter animation
  requestAnimationFrame(() => {
    toast.classList.replace('opacity-0', 'opacity-100');
    toast.classList.replace('translate-y-2', 'translate-y-0');
  });

  // close on click
  toast.querySelector('.close-btn')
       .addEventListener('click', () => removeToast(toast));

  // auto-dismiss
  setTimeout(() => removeToast(toast), duration);

  function removeToast(el) {
    el.classList.replace('opacity-100', 'opacity-0');
    el.classList.replace('translate-y-0', 'translate-y-2');
    el.addEventListener('transitionend', () => el.remove());
  }
}

// expose globally if you're not using ES modules:
window.showToast = showToast;
