import { getLocaleFromNavigator, init, register } from 'svelte-i18n';
import { browser } from '$app/environment';


register('en-US', () => import('./en_US.json'));
register('fr-FR', () => import('./fr_FR.json'));
register('sv-SE', () => import('./sv_SE.json'));
register('ja-JP', () => import('./ja_JP.json'));
register('zh-TW', () => import('./zh_TW.json'));

const defaultLocale = 'en-US';

console.log('browser', browser);
if (browser) console.log('window.navigator.language', window.navigator.language);

const getLocaleWithRegion = (language) => {
    const languageMap = {
        'sv': 'sv-SE',
        'fr': 'fr-FR',
        'ja': 'ja-JP',
        'zh': 'zh-TW',
        'en': 'en-US'
    };
    return languageMap[language] || language;
};


init({
    fallbackLocale: defaultLocale,
    initialLocale: browser ? getLocaleWithRegion(window.navigator.language.split('-')[0]) : defaultLocale
});