module.exports = {
    env: {browser: true, es2020: true, node: true},
    extends: [
        'eslint:recommended', 'plugin:react/recommended',
        'plugin:react/jsx-runtime', 'plugin:react-hooks/recommended',
        'plugin:@tanstack/eslint-plugin-query/recommended',
    ],
    parserOptions: {ecmaVersion: 'latest', sourceType: 'module'},
    settings: {react: {version: '18.2'}},
    plugins: ['react-refresh', 'react', '@tanstack/query'],
    rules: {
        'react-refresh/only-export-components': 'warn',
        "react/jsx-uses-vars": "error",
        "react/jsx-uses-react": "error",
    },
}
