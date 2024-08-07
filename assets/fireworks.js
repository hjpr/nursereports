const duration = 4 * 1000,
animationEnd = Date.now() + duration,
defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

function randomInRange(min, max) {
return Math.random() * (max - min) + min;
}

const interval = setInterval(function() {
const timeLeft = animationEnd - Date.now();

if (timeLeft <= 0) {
    return clearInterval(interval);
}

const particleCount = 50 * (timeLeft / duration);

// since particles fall down, start a bit higher than random
confetti(
    Object.assign({}, defaults, {
    particleCount,
    origin: { x: randomInRange(0.1, 0.4), y: Math.random() - 0.2 },
    startVelocity: 20,
    gravity: 0.1,
    decay: 0.8,
    ticks: 200
    })
);
confetti(
    Object.assign({}, defaults, {
    particleCount,
    origin: { x: randomInRange(0.6, 0.9), y: Math.random() - 0.2 },
    startVelocity: 40,
    gravity: 0.1,
    decay: 0.8,
    ticks: 200
    })
);
}, 250);