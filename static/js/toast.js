(function(){
  const icons = {
    success: '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>',
    error: '<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.29 3.86L1.82 18a1 1 0 00.89 1.5h18.59a1 1 0 00.88-1.5L13.71 3.86a1 1 0 00-1.71 0zM12 9v4m0 4h.01"/></svg>'
  };

  window.showToast = function(type, message){
    const container = document.getElementById('toast-container');
    if(!container) return;

    const variant = type === 'success' ? 'border-green-500 dark:border-green-400' : 'border-red-500 dark:border-red-400';
    const toast = document.createElement('div');
    toast.className = `relative flex items-start p-4 pr-10 rounded-lg shadow-lg backdrop-blur-sm bg-white dark:bg-gray-800 border-l-4 ${variant} transform transition-transform duration-500 translate-x-full opacity-0`;
    toast.innerHTML = `${icons[type] || ''}<div class="ml-3 text-sm flex-1">${message}</div><button class="absolute top-2 right-2 text-green-900 dark:text-green-400 hover:text-green-700 dark:hover:text-green-300 transition-colors cursor-pointer" aria-label="Close">&times;</button>`;

    const btn = toast.querySelector('button');
    btn.addEventListener('click', () => removeToast(toast));

    container.appendChild(toast);
    requestAnimationFrame(() => {
      toast.classList.remove('translate-x-full','opacity-0');
    });
    setTimeout(() => removeToast(toast), 10000);
  };

  function removeToast(toast){
    toast.classList.add('translate-x-full','opacity-0');
    toast.addEventListener('transitionend', () => toast.remove(), { once: true });
  }
})();
