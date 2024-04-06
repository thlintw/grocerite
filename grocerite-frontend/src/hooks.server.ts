import { redirect, type Handle } from '@sveltejs/kit'
import { locale } from 'svelte-i18n'
import { building } from "$app/environment";
import type { DecodedIdToken } from "firebase-admin/auth";

export const handle: Handle = async ({ event, resolve }) => {
	const lang = event.request.headers.get('accept-language')?.split(',')[0]
	if (lang) {
		locale.set(lang)
	}

	return resolve(event)
}