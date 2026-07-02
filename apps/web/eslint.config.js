import js from "@eslint/js";
import reactPlugin from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";

export default [
  js.configs.recommended,
  {
    files: ["src/**/*.{js,jsx}"],
    plugins: {
      react: reactPlugin,
      "react-hooks": reactHooks,
    },
    languageOptions: {
      parserOptions: {
        ecmaFeatures: { jsx: true },
      },
      globals: {
        // Browser globals
        window: "readonly",
        document: "readonly",
        console: "readonly",
        fetch: "readonly",
        crypto: "readonly",
        URL: "readonly",
        URLSearchParams: "readonly",
        setTimeout: "readonly",
        clearTimeout: "readonly",
        Promise: "readonly",
        JSON: "readonly",
        parseInt: "readonly",
        parseFloat: "readonly",
        Number: "readonly",
        Boolean: "readonly",
        Array: "readonly",
        Object: "readonly",
        String: "readonly",
        Math: "readonly",
        Date: "readonly",
        Error: "readonly",
        Map: "readonly",
        Set: "readonly",
        Symbol: "readonly",
        undefined: "readonly",
        null: "readonly",
        Infinity: "readonly",
        NaN: "readonly",
      },
    },
    settings: {
      react: { version: "18" },
    },
    rules: {
      ...reactPlugin.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,

      // react/react-in-jsx-scope not needed with React 17+ JSX transform
      "react/react-in-jsx-scope": "off",

      // Debt: add PropTypes or migrate to TypeScript in a future pass
      "react/prop-types": "off",

      // Allow ignoring caught errors (common pattern: catch (error) { use statusText instead })
      // and allow destructure-to-exclude pattern (const { excluded, ...rest } = obj)
      "no-unused-vars": ["error", { "caughtErrors": "none", "ignoreRestSiblings": true }],

      // Debt: react-hooks/set-state-in-effect is a new strict v7 rule flagging form-reset
      // useEffect patterns throughout the legacy pages. Downgraded to warn for baseline;
      // each instance should be reviewed and converted to derived state or useMemo.
      "react-hooks/set-state-in-effect": "warn",

      // Debt: unescaped apostrophes in DashboardPage.jsx:223,304 JSX text.
      // Harmless in practice; fix by escaping as &apos; when touching those components.
      "react/no-unescaped-entities": "off",
    },
  },
];
