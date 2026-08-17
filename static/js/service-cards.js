(function () {
    const container = document.getElementById('ff-cards-scroll-container');
    const deck = document.getElementById('ff-cards-deck');
    if (!container || !deck) return;

    const cards = Array.from(deck.querySelectorAll('.ff-service-card-3d'));
    const prevBtn = document.getElementById('ff-deck-prev');
    const nextBtn = document.getElementById('ff-deck-next');
    const dots = Array.from(document.querySelectorAll('.ff-deck-dot'));
    const counterCurrent = document.getElementById('ff-counter-current');

    const N = cards.length;
    if (N === 0) return;

    // Set scroll container height based on card count
    container.style.height = `calc(100vh * ${N + 0.5})`;

    let currentCardIndex = 0;

    function updateCardTransforms() {
        const rect = container.getBoundingClientRect();
        const totalScrollable = container.offsetHeight - window.innerHeight;

        let progress = 0;
        if (totalScrollable > 0) {
            progress = Math.max(0, Math.min(1, -rect.top / totalScrollable));
        }

        const exactIndex = progress * (N - 1);
        const roundedIndex = Math.round(exactIndex);

        if (roundedIndex !== currentCardIndex) {
            currentCardIndex = roundedIndex;
            updateControls(currentCardIndex);
        }

        cards.forEach((card, i) => {
            const diff = i - exactIndex;

            if (diff < -0.05) {
                // Card has been scrolled past (moves up, rotates out)
                const away = Math.abs(diff);
                const translateY = -away * 320;
                const translateZ = -away * 100;
                const rotateX = away * 40;
                const rotateY = -away * 15;
                const scale = Math.max(0.6, 1 - away * 0.15);
                const opacity = Math.max(0, 1 - away * 1.2);

                card.style.transform = `translate3d(0, ${translateY}px, ${translateZ}px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(${scale})`;
                card.style.opacity = opacity;
                card.style.zIndex = N - Math.floor(away);
                card.style.pointerEvents = 'none';

            } else if (Math.abs(diff) <= 0.05) {
                // Active card front and center
                card.style.transform = `translate3d(0, 0px, 0px) rotateX(0deg) rotateY(0deg) scale(1)`;
                card.style.opacity = '1';
                card.style.zIndex = N + 10;
                card.style.pointerEvents = 'auto';

            } else {
                // Upcoming card in stack waiting underneath
                const stack = Math.min(diff, 4);
                const translateY = stack * 22;
                const translateZ = -stack * 70;
                const rotateX = -stack * 4;
                const scale = Math.max(0.7, 1 - stack * 0.06);
                const opacity = Math.max(0, 1 - (stack - 1) * 0.35);

                card.style.transform = `translate3d(0, ${translateY}px, ${translateZ}px) rotateX(${rotateX}deg) scale(${scale})`;
                card.style.opacity = opacity;
                card.style.zIndex = N - Math.floor(diff);
                card.style.pointerEvents = 'none';
            }
        });
    }

    function updateControls(index) {
        dots.forEach((dot, idx) => {
            dot.classList.toggle('active', idx === index);
        });
        if (counterCurrent) {
            const num = index + 1;
            counterCurrent.textContent = num < 10 ? `0${num}` : `${num}`;
        }
    }

    function scrollToIndex(targetIdx) {
        const idx = Math.max(0, Math.min(N - 1, targetIdx));
        const totalScrollable = container.offsetHeight - window.innerHeight;
        const containerTop = container.offsetTop;
        const targetScroll = containerTop + (idx / (N - 1)) * totalScrollable;

        window.scrollTo({
            top: targetScroll,
            behavior: 'smooth'
        });
    }

    if (prevBtn) {
        prevBtn.addEventListener('click', () => scrollToIndex(currentCardIndex - 1));
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', () => scrollToIndex(currentCardIndex + 1));
    }

    dots.forEach((dot, idx) => {
        dot.addEventListener('click', () => scrollToIndex(idx));
    });

    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                updateCardTransforms();
                ticking = false;
            });
            ticking = true;
        }
    });

    // Touch swipe support for mobile
    let touchStartY = 0;
    container.addEventListener('touchstart', (e) => {
        touchStartY = e.touches[0].clientY;
    }, { passive: true });

    container.addEventListener('touchend', (e) => {
        const touchEndY = e.changedTouches[0].clientY;
        const deltaY = touchStartY - touchEndY;

        if (Math.abs(deltaY) > 50) {
            if (deltaY > 0 && currentCardIndex < N - 1) {
                scrollToIndex(currentCardIndex + 1);
            } else if (deltaY < 0 && currentCardIndex > 0) {
                scrollToIndex(currentCardIndex - 1);
            }
        }
    }, { passive: true });

    // Initial positioning
    updateCardTransforms();
})();
