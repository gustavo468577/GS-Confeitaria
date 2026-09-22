'use strict';

// A failed external image should not leave a broken product card.
document.querySelectorAll('img[data-fallback]').forEach(function (img) {
    function useFallback() {
        const fallback = img.dataset.fallback;
        if (fallback) {
            delete img.dataset.fallback;
            img.src = fallback;
        }
    }
    img.addEventListener('error', useFallback, { once: true });
    if (img.complete && img.naturalWidth === 0) useFallback();
});
