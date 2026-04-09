import http.server
import socketserver

PORT = 8080

class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

print(f"✅ Server Running at http://localhost:{PORT}")
with socketserver.TCPServer(("", PORT), NoCacheHandler) as httpd:
    httpd.serve_forever()