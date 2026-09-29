# Frontend lint

Enforce the layout with `eslint-plugin-boundaries` (dependency direction) and core `no-restricted-imports` (barrels, deep relatives). Add the plugin as a devDependency. Merge into the project's existing ESLint config.

## Flat config (`eslint.config.js`)

```js
import boundaries from 'eslint-plugin-boundaries';

export default [
  // ...existing config
  {
    plugins: { boundaries },
    settings: {
      'boundaries/elements': [
        { type: 'app', pattern: 'src/app/**' },
        { type: 'feature', pattern: 'src/features/*', capture: ['feature'] },
        { type: 'shared', pattern: 'src/shared/**' },
        { type: 'theme', pattern: 'src/theme/**' },
      ],
    },
    rules: {
      'boundaries/element-types': ['error', {
        default: 'disallow',
        rules: [
          { from: 'app', allow: ['feature', 'shared', 'theme'] },
          // a feature may import itself, shared and theme, never another feature
          { from: 'feature', allow: [['feature', { feature: '${from.feature}' }], 'shared', 'theme'] },
          { from: 'shared', allow: ['shared', 'theme'] },
          { from: 'theme', allow: ['theme'] },
        ],
      }],
      'no-restricted-imports': ['error', {
        patterns: [
          { group: ['../../*'], message: 'Use the project alias instead of deep relative imports.' },
          { group: ['**/features/*', '**/shared/components', '**/shared/hooks', '**/shared/api'], message: 'No barrel imports. Import the specific file.' },
        ],
      }],
    },
  },
];
```

Notes:
- Adjust the element patterns and the alias to the real folders. With `eslint-import-resolver-typescript` configured, `boundaries` resolves aliases; add it if boundary rules do not fire on aliased imports.
- Barrels: also forbid creating them with a rule such as `import/no-barrel-file` (or `eslint-plugin-barrel-files` `avoid-barrel-files`) if the project has that plugin.
- Biome projects: use `noBarrelFile` and `noRestrictedImports`; Biome has no boundaries rule, so keep ESLint for that one check.
