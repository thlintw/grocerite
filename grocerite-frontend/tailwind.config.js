/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin');

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
      },
      boxShadow: {
        'grocerite-sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      }
    },
  },
  plugins: [
    plugin(function({ addUtilities, theme }) {
      const newUtilities = {};
      const colors = theme('colors');

      Object.keys(colors).forEach((colorName) => {
        const isColorObject = typeof colors[colorName] === 'object';

        const shadowSizes = {
          sm: '2px',
          md: '4px',
          lg: '6px',
          xl: '8px',
          '2xl': '10px',
        };

        Object.keys(shadowSizes).forEach((size) => {
          const sizeValue = shadowSizes[size];

          if (isColorObject) {
            Object.keys(colors[colorName]).forEach((shade) => {
              const colorValue = colors[colorName][shade];
              const key = `.shadow-grocerite-${colorName}-${shade}-${size}`;
              newUtilities[key] = {
                boxShadow: `0 ${sizeValue} 0 0 ${colorValue}`,
              };
            });
          } else {
            const colorValue = colors[colorName];
            const key = `.shadow-grocerite-${colorName}-${size}`;
            newUtilities[key] = {
              boxShadow: `0 ${sizeValue} 0 0 ${colorValue}`,
            };
          }
        });
      });

      addUtilities(newUtilities, ['responsive', 'hover']);
    }),
  ],
}

