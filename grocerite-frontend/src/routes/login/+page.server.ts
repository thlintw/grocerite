import { redirect } from "@sveltejs/kit";
import type { Actions } from "./$types";
import { getFirebaseServer } from "$lib/server/firebaseServer";

export const actions = {
    default: async ({ request, cookies }) => {
        const form = await request.formData();
        const token = form.get("token");
        if (!token || typeof token !== "string") {
            throw redirect(303, "/login");
        }
        const admin = getFirebaseServer();
        if (admin.error) {
            throw redirect(303, "/login");
        }

        // Expires in 5 days
        const expiresIn = 60 * 60 * 24 * 5;
        let sessionCookie: string;
        try {
            sessionCookie = await admin.data
                .auth()
                .createSessionCookie(token, { expiresIn: expiresIn * 1000 });
        } catch (error) {
            console.error(error);
            throw redirect(303, "/login");
        }

        cookies.set("session", sessionCookie, {
            maxAge: expiresIn,
            path: "/",
            httpOnly: true,
            secure: true,
            sameSite: "lax",
        });

        throw redirect(303, "/");
    },
} satisfies Actions;