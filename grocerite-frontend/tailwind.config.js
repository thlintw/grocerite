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
        'llg': '0.75rem',
      },
      screens: {
        '3xl': '1600px',
      },
      fontFamily: {
        berkshire: ['Berkshire Swash', 'cursive'],
      }
    },
  },
  safelist: [
    // orange outline button
    'border-orange-500',
    'text-orange-500',
    'hover:bg-orange-500',
    'hover:text-white',
    'focus:ring-orange-300',
    'dark:border-orange-300',
    'dark:text-orange-300',
    'dark:hover:bg-orange-300',
    'dark:hover:text-white',
    'dark:focus:ring-orange-800',
    // orange button
    'bg-orange-500',
    'hover:bg-orange-600',
    'focus:ring-orange-300',
    'dark:bg-orange-600',
    'dark:hover:bg-orange-700',
    'dark:focus:ring-orange-800',
    // emerald outline button
    'border-emerald-500',
    'text-emerald-500',
    'hover:bg-emerald-500',
    'hover:text-white',
    'focus:ring-emerald-300',
    'dark:border-emerald-300',
    'dark:text-emerald-300',
    'dark:hover:bg-emerald-300',
    'dark:hover:text-white',
    'dark:focus:ring-emerald-800',
    // emerald button
    'bg-emerald-500',
    'hover:bg-emerald-600',
    'focus:ring-emerald-300',
    'dark:bg-emerald-600',
    'dark:hover:bg-emerald-700',
    'dark:focus:ring-emerald-800'
  ],
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
    plugin(function({ addUtilities, theme }) {
      const newUtilities = {};
      const colors = theme('colors');

      const shadowSizes = {
        sm: '1px',
        md: '2px',
        lg: '3px',
        xl: '4px',
        '2xl': '5px',
      };

      Object.keys(shadowSizes).forEach((size) => {
        const sizeValue = shadowSizes[size];

        Object.keys(colors).forEach((colorName) => {
          const isColorObject = typeof colors[colorName] === 'object';

          if (isColorObject) {
            Object.keys(colors[colorName]).forEach((shade) => {
              const colorValue = colors[colorName][shade];
              const key = `.drop-shadow-grocerite-${colorName}-${shade}-${size}`;
              newUtilities[key] = {
                // dropShadow: `0 ${sizeValue} 0 0 ${colorValue}`,
                filter: `drop-shadow(0 ${sizeValue} 0 ${colorValue})`,
              };
            });
          } else {
            const colorValue = colors[colorName];
            const key = `.shadow-grocerite-${colorName}-${size}`;
            newUtilities[key] = {
              // dropShadow: `0 ${sizeValue} 0 0 ${colorValue}`,
              filter: `drop-shadow(0 ${sizeValue} 0 ${colorValue})`,
            };
          }
        });
      });
      
      addUtilities(newUtilities, ['responsive', 'hover']);

    }),
  ],
}

