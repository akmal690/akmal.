// Enhanced Browser Analytics (PostHog + Typing Metrics)
posthog.init('phc_yourPostHogKey', {
    api_host: 'https://app.posthog.com',
    capture_pageview: false
});

let sessionStart = Date.now();
let keystrokeTimestamps = [];
let fieldFocusTimes = {};

// Track typing dynamics
document.querySelectorAll('input').forEach(input => {
    let focusStart;
    
    input.addEventListener('focus', () => {
        focusStart = Date.now();
        posthog.capture('field_focus', {field: input.name});
    });
    
    input.addEventListener('blur', () => {
        const focusDuration = Date.now() - focusStart;
        fieldFocusTimes[input.name] = (fieldFocusTimes[input.name] || 0) + focusDuration;
    });
    
    input.addEventListener('keydown', () => {
        keystrokeTimestamps.push(Date.now());
    });
});
// Submit analytics
document.querySelector('form').addEventListener('submit', () => {
    const sessionData = {
        duration: Date.now() - sessionStart,
        keystrokes: keystrokeTimestamps.length,
        typing_speed: calculateTypingSpeed(),
        field_focus: fieldFocusTimes,
        user_id: typeof USER_ID !== 'undefined' ? USER_ID : null
    };

    posthog.capture('checkout_completed', sessionData);
});

function calculateTypingSpeed() {
    if (keystrokeTimestamps.length < 2) return 0;
    const intervals = [];
    for (let i = 1; i < keystrokeTimestamps.length; i++) {
        intervals.push(keystrokeTimestamps[i] - keystrokeTimestamps[i-1]);
    }
    const avgInterval = intervals.reduce((a, b) => a + b) / intervals.length;
    return Math.round(60000 / avgInterval); // CPM
}

