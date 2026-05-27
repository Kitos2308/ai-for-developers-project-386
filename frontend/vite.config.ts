import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';
const LOG_REQUESTS = process.env.VITE_LOG_API_REQUESTS === 'true';

function logRequest(req: any) {
	if (!LOG_REQUESTS) return;
	console.log(`\n[API ${req.method}] ${API_URL}${req.url}`);
	console.log('[API Headers]', JSON.stringify({
		'content-type': req.headers['content-type'],
		'accept': req.headers['accept'],
	}, null, 2));
}

function logResponse(req: any, res: any) {
	if (!LOG_REQUESTS) return;
	console.log(`[API Response ${req.method}] ${req.url} - ${res.statusCode}`);
}

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			'/public': {
				target: API_URL,
				changeOrigin: true,
				configure: (proxy) => {
					proxy.on('proxyReq', (_, req) => logRequest(req));
					proxy.on('proxyRes', (res, req) => logResponse(req, res));
				},
			},
			'/admin': {
				target: API_URL,
				changeOrigin: true,
				configure: (proxy) => {
					proxy.on('proxyReq', (_, req) => logRequest(req));
					proxy.on('proxyRes', (res, req) => logResponse(req, res));
				},
			},
		}
	}
});
