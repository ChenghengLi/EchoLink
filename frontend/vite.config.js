import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'

export default ({ mode }) => {
  // Load environment variables with VITE_ prefix
  process.env = {...process.env, ...loadEnv(mode, './config')};

  // https://vitejs.dev/config/
  return defineConfig({
    plugins: [vue()],
    test: {
      globals: true,
      environment: 'jsdom',
    },
    VITE_API_URL: process.env.VITE_API_URL,
  })
}

