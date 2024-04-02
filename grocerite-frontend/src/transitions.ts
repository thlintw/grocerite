import { cubicOut } from 'svelte/easing';

export function scaleFade(node: HTMLElement, { duration = 300, delay = 0, easing = cubicOut } = {}) {
    return {
        duration,
        delay,
        easing,
        css: (t: number) => `
            opacity: ${t};
            transform: scale(${0.9 + t * 0.1});
        `
    };
}