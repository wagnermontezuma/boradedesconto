/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#FF6B00',
          50: '#FFF2E9',
          100: '#FFE2CB',
          200: '#FFCA9E',
          300: '#FFA866',
          400: '#FF8533',
          500: '#FF6B00',
          600: '#E05F00',
          700: '#B24B00',
          800: '#913C00',
          900: '#703000',
        },
        secondary: {
          DEFAULT: '#2563eb',
          dark: '#1d4ed8',
          light: '#3b82f6',
        },
        discount: {
          low: '#22c55e',
          medium: '#f97316',
          high: '#ef4444',
        }
      },
      gridTemplateColumns: {
        'auto-fit': 'repeat(auto-fit, minmax(220px, 1fr))',
      },
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
      },
      boxShadow: {
        'card': '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      },
    },
  },
  plugins: [],
}; 