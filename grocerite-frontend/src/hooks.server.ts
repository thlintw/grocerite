import { redirect, type Handle } from '@sveltejs/kit'
import { locale } from 'svelte-i18n'
import { building } from "$app/environment";
import { getFirebaseServer } from "$lib/server/firebaseServer";
import type { DecodedIdToken } from "firebase-admin/auth";

export const handle: Handle = async ({ event, resolve }) => {
	const lang = event.request.headers.get('accept-language')?.split(',')[0]
	if (lang) {
		locale.set(lang)
	}

	event.locals.id = "";
    event.locals.email = "";

    const isAuth: boolean = event.url.pathname === "/login";
    if (isAuth || building) {
        event.cookies.set("session", "", {
			path: "/",
		});
        return await resolve(event);
    }

    const session = event.cookies.get("session") ?? "";
    const admin = getFirebaseServer();
    if (admin.error) {
        throw redirect(303, "/login");
    }
    let decodedClaims: DecodedIdToken;
    try {
        decodedClaims = await admin.data.auth().verifySessionCookie(session, false);
    } catch (error) {
        console.error(error);
        throw redirect(303, "/login");
    }
    const { uid, email } = decodedClaims;
    event.locals.id = uid;
    event.locals.email = email ?? "";

    if (!event.locals.id) {
        throw redirect(303, "/login");
    }

	return resolve(event)
}