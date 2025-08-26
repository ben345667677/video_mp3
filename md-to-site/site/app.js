const http = require('http')
const path = require('path')
const fs = require('fs')

const PORT = 3000
const HOST = '0.0.0.0'
const publicDir = __dirname

// Enhanced Markdown to HTML converter with beautiful styling
function markdownToHtml(markdown) {
	let html = markdown
		// Headers with enhanced styling
		.replace(/^### (.*$)/gim, '<h3 class="content-title">$1</h3>')
		.replace(/^## (.*$)/gim, '<h2 class="subtitle">$1</h2>')
		.replace(/^# (.*$)/gim, '<h1 class="main-title">$1</h1>')
		// Bold with enhanced styling
		.replace(/\*\*(.*)\*\*/gim, '<strong class="highlight">$1</strong>')
		// Italic
		.replace(/\*(.*)\*/gim, '<em>$1</em>')
		// Code blocks
		.replace(/```(.*?)```/gims, '<pre class="code-block"><code>$1</code></pre>')
		// Inline code
		.replace(/`(.*?)`/gim, '<code class="inline-code">$1</code>')
		// Lists
		.replace(/^\* (.*$)/gim, '<li>$1</li>')
		.replace(/^- (.*$)/gim, '<li>$1</li>')
		// Line breaks
		.replace(/\n\n/gim, '</p><p>')
		.replace(/\n/gim, '<br>')
	
	// Wrap in paragraphs
	html = '<p>' + html + '</p>'
	
	return html
}

const server = http.createServer((req, res) => {
	const serveFile = (response, filePath, contentType) => {
		fs.readFile(filePath, (err, content) => {
			if (err) {
				if (err.code === 'ENOENT') {
					response.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' })
					response.end('Not Found')
				} else {
					response.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' })
					response.end(`Server Error: ${err.code}`)
				}
			} else {
				response.writeHead(200, { 'Content-Type': contentType })
				response.end(content)
			}
		})
	}

	if (req.url === '/') {
		return serveFile(res, path.join(publicDir, 'index.html'), 'text/html; charset=utf-8')
	}
	if (req.url === '/styles.css') {
		return serveFile(res, path.join(publicDir, 'styles.css'), 'text/css; charset=utf-8')
	}
	if (req.url.startsWith('/pages/')) {
		const pageFile = req.url.replace('/pages/', '')
		const filePath = path.join(publicDir, 'pages', pageFile)
		
		// Check if it's a Markdown file
		if (pageFile.endsWith('.md')) {
			fs.readFile(filePath, 'utf8', (err, markdownContent) => {
				if (err) {
					if (err.code === 'ENOENT') {
						res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' })
						res.end('Not Found')
					} else {
						res.writeHead(500, { 'Content-Type': 'text/plain; charset=utf-8' })
						res.end(`Server Error: ${err.code}`)
					}
				} else {
					const htmlContent = markdownToHtml(markdownContent)
					const pageName = pageFile.replace('.md', '')
					const fullHtml = `<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>${pageName} - יואב 2 -- DevOps</title>
	<link rel="stylesheet" href="/styles.css">
	<style>
		body {
			background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
			min-height: 100vh;
			margin: 0;
			font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
		}
		
		.site-header {
			background: linear-gradient(90deg, #000000 0%, #1a1a1a 100%);
			color: #fff;
			padding: 15px 0;
			margin: 0;
			border-radius: 0 0 20px 20px;
			box-shadow: 0 4px 20px rgba(0,0,0,0.3);
			position: relative;
			overflow: hidden;
		}
		
		.site-header::before {
			content: '';
			position: absolute;
			top: 0;
			left: 0;
			right: 0;
			bottom: 0;
			background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
			animation: shine 3s infinite;
		}
		
		@keyframes shine {
			0% { transform: translateX(-100%); }
			100% { transform: translateX(100%); }
		}
		
		.site-title {
			margin: 0;
			font-size: 1.8rem;
			text-align: center;
			color: #fff;
			font-weight: 700;
			text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
			position: relative;
			z-index: 1;
		}
		
		.container {
			max-width: 1200px;
			margin: 30px auto;
			padding: 30px;
			background: rgba(255,255,255,0.95);
			border-radius: 20px;
			box-shadow: 0 10px 40px rgba(0,0,0,0.2);
			backdrop-filter: blur(10px);
		}
		
		.content {
			line-height: 1.8;
			color: #333;
		}
		
		.main-title {
			font-size: 3rem;
			color: #2c3e50;
			text-align: center;
			margin-bottom: 20px;
			background: linear-gradient(45deg, #667eea, #764ba2);
			-webkit-background-clip: text;
			-webkit-text-fill-color: transparent;
			background-clip: text;
			text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
		}
		
		.subtitle {
			font-size: 1.5rem;
			color: #34495e;
			text-align: center;
			margin-bottom: 30px;
			padding: 10px;
			border-bottom: 3px solid #667eea;
			display: inline-block;
			width: 100%;
		}
		
		.content-title {
			font-size: 2rem;
			color: #2c3e50;
			margin: 30px 0 20px 0;
			padding: 15px;
			background: linear-gradient(90deg, #f8f9fa, #e9ecef);
			border-left: 5px solid #667eea;
			border-radius: 0 10px 10px 0;
		}
		
		.highlight {
			background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
			padding: 2px 8px;
			border-radius: 4px;
			font-weight: 600;
		}
		
		.code-block {
			background: #2d3748;
			color: #e2e8f0;
			padding: 20px;
			border-radius: 10px;
			overflow-x: auto;
			margin: 20px 0;
			border-left: 5px solid #667eea;
		}
		
		.inline-code {
			background: #f7fafc;
			color: #2d3748;
			padding: 2px 6px;
			border-radius: 4px;
			font-family: 'Courier New', monospace;
			border: 1px solid #e2e8f0;
		}
		
		li {
			margin: 10px 0;
			padding: 5px 0;
		}
		
		p {
			margin: 15px 0;
			font-size: 1.1rem;
		}
		
		.back-btn {
			display: inline-block;
			margin-bottom: 30px;
			padding: 12px 25px;
			background: linear-gradient(45deg, #667eea, #764ba2);
			color: white;
			text-decoration: none;
			border-radius: 25px;
			font-weight: 600;
			transition: all 0.3s ease;
			box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
		}
		
		.back-btn:hover {
			transform: translateY(-2px);
			box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
		}
	</style>
</head>
<body>
	<header class="site-header">
		<h1 class="site-title">יואב 2 -- DevOps</h1>
	</header>
	<main class="container">
		<div class="content">
			<a href="/" class="back-btn">← חזרה לדף הבית</a>
			${htmlContent}
		</div>
	</main>
</body>
</html>`
					res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' })
					res.end(fullHtml)
				}
			})
			return
		}
		
		// Regular HTML files
		return serveFile(res, filePath, 'text/html; charset=utf-8')
	}
	res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' })
	res.end('Not Found')
})

server.listen(PORT, HOST, () => {
	console.log(`Server running at http://${HOST}:${PORT}/`)
})
