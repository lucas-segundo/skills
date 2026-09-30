# Backend lint

Enforce the hexagonal dependency direction with `eslint-plugin-boundaries`, and framework/ORM bans with `no-restricted-imports`. Add the plugin as a devDependency. Merge into the project's existing ESLint config.

## Flat config (`eslint.config.js`)

```js
import boundaries from 'eslint-plugin-boundaries';

export default [
  // ...existing config
  {
    plugins: { boundaries },
    settings: {
      'boundaries/elements': [
        { type: 'domain', pattern: 'src/domain/**' },
        { type: 'app', pattern: 'src/app/**' },
        { type: 'infra', pattern: 'src/infra/**' },
        { type: 'main', pattern: 'src/main/**' },
      ],
    },
    rules: {
      'boundaries/element-types': ['error', {
        default: 'disallow',
        rules: [
          { from: 'domain', allow: ['domain'] },
          { from: 'app', allow: ['app', 'domain'] },
          { from: 'infra', allow: ['infra', 'app', 'domain'] },
          { from: 'main', allow: ['main', 'app', 'infra', 'domain'] },
        ],
      }],
    },
  },
  // domain and app must stay free of framework, ORM and validator packages
  {
    files: ['src/domain/**', 'src/app/**'],
    rules: {
      'no-restricted-imports': ['error', {
        patterns: [
          { group: ['@nestjs/*', 'express', 'fastify', 'koa', 'hono'], message: 'Web frameworks belong in main.' },
          { group: ['@prisma/*', 'typeorm', 'drizzle-orm', 'mongoose', 'sequelize', 'knex', 'pg'], message: 'ORMs and drivers belong in infra.' },
          { group: ['zod', 'class-validator', 'joi', 'yup'], message: 'Validation belongs in main/routes/*/dto.' },
        ],
      }],
    },
  },
  // infra never reaches into the delivery layer
  {
    files: ['src/infra/**'],
    rules: {
      'no-restricted-imports': ['error', {
        patterns: [{ group: ['**/main/**', 'src/main/**'], message: 'infra must not import main.' }],
      }],
    },
  },
];
```

Notes:
- Trim the banned package lists to what the project actually uses and add the ones it uses that are missing.
- No barrel files: add the project's barrel rule (`eslint-plugin-barrel-files` `avoid-barrel-files`, or Biome `noBarrelFile`).
