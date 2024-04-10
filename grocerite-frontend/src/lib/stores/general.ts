// light/dark mode switch store

import { writable, derived } from 'svelte/store';
import { locale } from 'svelte-i18n';

export const darkMode = writable(false);

export const lc = derived(locale, $locale => {
    const isJPorTW = $locale === 'ja-JP' || $locale === 'zh-TW';
    return {
        title: isJPorTW ? 'font-sans text-2xl font-bold -top-5' : 'font-berkshire text-3xl -top-6',
        text: isJPorTW ? 'font-sans' : 'font-serif'
    };
});