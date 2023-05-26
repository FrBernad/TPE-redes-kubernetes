// @ts-check

/** @type {import('prettier').Config} */
module.exports = {
    endOfLine: "lf",
    singleQuote: false,
    semi: true,
    tabWidth: 4,
    trailingComma: "none",
    importOrder: ["^(react/(.*)$)|^(react$)", "^(next/(.*)$)|^(next$)", "<THIRD_PARTY_MODULES>", "^@/types/(.*)$", "^@/interfaces/(.*)$", "^@/utils/(.*)$", "^@/components/(.*)$", "^@/styles/(.*)$", "^[./]"],
    importOrderSeparation: false,
    importOrderSortSpecifiers: true,
    importOrderBuiltinModulesToTop: true,
    importOrderParserPlugins: ["typescript", "jsx", "decorators-legacy"],
    importOrderMergeDuplicateImports: true,
    importOrderCombineTypeAndValueImports: true,
    plugins: ["@ianvs/prettier-plugin-sort-imports"],
    bracketSpacing: false,
    printWidth: 120
};
