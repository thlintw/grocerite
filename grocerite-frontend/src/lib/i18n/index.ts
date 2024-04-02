import { getLocaleFromNavigator, init, register } from 'svelte-i18n';
import { browser } from '$app/environment';


register('en-US', () => import('./en_US.json'));
register('sv-SE', () => import('./sv_SE.json'));
register('ja-JP', () => import('./ja_JP.json'));
register('zh-TW', () => import('./zh_TW.json'));

const defaultLocale = 'en-US';

init({
    fallbackLocale: defaultLocale,
    initialLocale: 'en-US',
});