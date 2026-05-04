/* ─── Dorjivers global JS ─── */

document.addEventListener('DOMContentLoaded', () => {

  // Smooth reveal on scroll
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('opacity-100', 'translate-y-0');
          entry.target.classList.remove('opacity-0', 'translate-y-4');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  document.querySelectorAll('[data-reveal]').forEach(el => {
    el.classList.add('opacity-0', 'translate-y-4', 'transition-all', 'duration-500');
    observer.observe(el);
  });

});
