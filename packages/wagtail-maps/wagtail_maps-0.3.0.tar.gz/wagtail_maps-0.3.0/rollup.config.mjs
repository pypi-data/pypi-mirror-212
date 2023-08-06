import babel from '@rollup/plugin-babel';
import resolve from '@rollup/plugin-node-resolve';
import terser from '@rollup/plugin-terser';

const PRODUCTION = process.env.NODE_ENV === 'production';

function addInput(input) {
  return {
    input,
    output: {
      dir: 'wagtail_maps/static/wagtail_maps/js',
      format: 'iife',
      sourcemap: true,
    },
    plugins: [
      resolve(),
      babel({ babelHelpers: 'bundled' }),
      PRODUCTION && terser(),
    ],
  };
}

export default [
  addInput('client/src/admin-form.js'),
  addInput('client/src/admin-form_controllers.js'),
  addInput('client/src/map-block.js'),
];
