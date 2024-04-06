/** @type {import('./$types').PageLoad} */

export async function load({ params, fetch }) {
    // Fetch data from an https://httpbin.org/get
    const response = await fetch('https://httpbin.org/get');
    const data = await response.json();
    console.log(data);
	return {
		post: {
			title: `title`,
			content: `Content ccccc`,
            url: data.url,
		}
	};
}