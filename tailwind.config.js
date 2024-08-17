/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/**/**/*.{html,js}',
    './**/**/**/**/*.{html,js}'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          "50": "#ECEFED",
          "100": "#E4EBE6",
          "200": "#D4E5DA",
          "300": "#C4DECE",
          "400": "#B1D5BF",
          "500": "#9AC9AD",
          "600": "#7BB995",
          "700": "#4BA374",
          "800": "#038C57",
          "900": "#007D4C",
          "950": "#006D3D",
          "990": "#1D3B2A"
        },
        secondary: "#8D8D98",
        third:"#F1F1F1"
      }
    },
    fontFamily:{
      'body': [
        'Montserrat'
      ],
      'sans': [
        'Montserrat'
      ]
    }
  },
  daisyui: {
    themes: ["light",],
  },
  plugins: [
    require('daisyui'),
  ],
}
