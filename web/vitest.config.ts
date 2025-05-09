import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react'; // Para suportar React/JSX

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true, // Para não precisar importar describe, it, expect, etc.
    environment: 'jsdom', // Simula o ambiente do navegador
    setupFiles: './src/tests/setupTests.ts', // Arquivo para setup global de testes (ex: estender expect com jest-dom)
    css: false, // Se você não estiver testando CSS ou usando importações de CSS que quebram os testes
    // Opcional: configurar caminhos de alias se usados no projeto (ex: @/*)
    // resolve: {
    //   alias: {
    //     '@': path.resolve(__dirname, './src'),
    //   },
    // },
  },
}); 