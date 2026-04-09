import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './src/setupTests.js',
    coverage: {
      provider: 'istanbul',
      reportOnFailure: true,
      exclude: ['src/assets', 'src/App.{css,jsx}', 'src/Test/', 'src/Errors/', '**.css'],
      reporter: ['cobertura', 'html']
    }
  },
  server: {
    watch: {
      usePolling: true
    },
    host: true,
    port: 5173,
    strictPort: true
  },
})