/// <reference types="vite/client" />

interface Window {
  pywebview?: {
    api?: {
      open_widget?: () => Promise<void>;
      hide_widget?: () => Promise<void>;
      show_main?: () => Promise<void>;
    };
  };
}
