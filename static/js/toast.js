(function(){
  function getStyle(category){
    switch(category){
      case 'success':
        return 'bg-green-100 text-green-800 dark:bg-green-800 dark:text-green-100 ring-green-300 dark:ring-green-600';
      case 'error':
        return 'bg-red-100 text-red-800 dark:bg-red-800 dark:text-red-100 ring-red-300 dark:ring-red-600';
      default:
        return 'bg-blue-100 text-blue-800 dark:bg-blue-800 dark:text-blue-100 ring-blue-300 dark:ring-blue-600';
    }
  }

  window.showToast = function(message, category='message'){
    const container = document.getElementById('toast-container');
    if(!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast pointer-events-auto max-w-xs w-full ring-1 rounded-md shadow-soft dark:shadow-soft-dark transform transition-all duration-500 ease-in-out translate-x-full opacity-0 ' + getStyle(category);
    toast.innerHTML = '<div class="p-4 flex items-start"><div class="flex-1 text-sm">'+message+'</div><button class="ml-4 text-xl leading-none focus:outline-none" aria-label="Close">&times;</button></div>';

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
