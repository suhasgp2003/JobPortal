module.exports = {
  content: [
    './templates/**/*.html',
    './accounts/Templates/**/*.html',
    './jobs/templates/**/*.html',
    './jobs/forms.py',
  ],
  // Keep utility precedence and breakpoints consistent with the existing design.
  important: true,
  corePlugins: { preflight: false, container: false },
  theme: {
    screens: { sm: '576px', md: '768px', lg: '992px', xl: '1200px', '2xl': '1400px' },
  },
};
