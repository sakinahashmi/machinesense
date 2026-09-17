/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        slate: {
          50: '#F8FAFC',
          100: '#F4F6F8',
          200: '#D8E0E6',
          300: '#CBD5DE',
          400: '#8E9DAA',
          500: '#667685',
          600: '#667685',
          700: '#465563',
          800: '#2E3D4A',
          900: '#17212B',
          950: '#0E161E',
        },
        brand: {
          DEFAULT: '#356B7A',
          dark: '#285664',
          light: '#E8F0F2',
          border: '#B8D2D9',
        },
        action: {
          DEFAULT: '#C87916',
          hover: '#A96210',
          light: '#FAF4E8',
          border: '#F0DEC0',
        },
        status: {
          success: '#23805A',
          successBg: '#E9F5F0',
          successBorder: '#C6E6D8',
          warning: '#C58A20',
          warningBg: '#FAF4E8',
          warningBorder: '#F0DEC0',
          critical: '#C34B4B',
          criticalBg: '#F9EBEB',
          criticalBorder: '#F2CDCD',
        },
        sidebar: {
          bg: '#202A33',
          active: '#30424F',
          text: '#B9C5CE',
          muted: '#AEBBC5',
          activeText: '#FFFFFF',
          border: '#2B3844',
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Menlo', 'Consolas', 'monospace'],
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      }
    },
  },
  plugins: [],
}


