/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./src/**/*.svelte', './src/**/*.html'],
  content: [],
  darkMode: 'class',
  important: true,
  theme: {
    extend: {
      width: {
        inherit: 'inherit',
      },
      borderRadius: {
        '2xl': '2rem',
        'xl': '1rem',
      },
      screens: {
        '3xl': '1600px',
      },
      fontFamily: {
        berkshire: ['Berkshire Swash', 'cursive'],
      }
    },
  },
  plugins: [require('tw-neumorphism')],
}

