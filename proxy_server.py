#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

PORT = 4173

INJECT_SCRIPT = """
<script>
(function () {
  function toProxy(url) {
    return '/proxy?url=' + encodeURIComponent(url);
  }

  function absoluteUrl(value) {
    try { return new URL(value, window.location.href).toString(); }
    catch (_) { return ''; }
  }

  document.addEventListener('click', function (event) {
    const a = event.target.closest('a[href]');
    if (!a) return;
    const href = a.getAttribute('href');
    if (!href || href.startsWith('#') || href.startsWith('javascript:')) return;

    event.preventDefault();
    const abs = absoluteUrl(href);
    if (abs) window.location.href = toProxy(abs);
  }, true);

  document.addEventListener('submit', function (event) {
    const form = event.target;
    if (!(form instanceof HTMLFormElement)) return;
    const action = form.getAttribute('action') || window.location.href;
    const method = (form.getAttribute('method') || 'GET').toUpperCase();
    if (method !== 'GET') return;

    event.preventDefault();
    const abs = absoluteUrl(action);
    const params = new URLSearchParams(new FormData(form));
    const full = params.toString() ? abs + (abs.includes('?') ? '&' : '?') + params.toString() : abs;
    window.location.href = toProxy(full);
  }, true);
})();
</script>
"""


class ProxyHandler(SimpleHTTPRequestHandler):
    def _proxy(self, target_url: str):
        parsed = urlparse(target_url)
        if parsed.scheme not in ("http", "https"):
            self.send_error(400, "Only http/https URLs are supported")
            return

        req = Request(
            target_url,
            headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                              " (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            },
        )

        try:
            with urlopen(req, timeout=20) as resp:
                status = resp.status
                content_type = resp.headers.get("Content-Type", "application/octet-stream")
                content = resp.read()
        except HTTPError as err:
            status = err.code
            content_type = err.headers.get("Content-Type", "text/plain; charset=utf-8")
            content = err.read() or f"HTTP error: {err.code}".encode("utf-8")
        except URLError as err:
            self.send_error(502, f"Proxy error: {err.reason}")
            return

        if "text/html" in content_type:
            charset = "utf-8"
            if "charset=" in content_type:
                charset = content_type.split("charset=")[-1].split(";")[0].strip()

            html = content.decode(charset, errors="replace")

            base_tag = f'<base href="{target_url}">'
            marker = "<head>"
            if marker in html:
                html = html.replace(marker, f"{marker}\n{base_tag}", 1)
            else:
                html = f"<head>{base_tag}</head>{html}"

            html = html.replace("<meta http-equiv=\"Content-Security-Policy\"", "<meta data-removed-csp=\"")
            html = html.replace("<meta http-equiv='Content-Security-Policy'", "<meta data-removed-csp='")

            if "</body>" in html:
                html = html.replace("</body>", f"{INJECT_SCRIPT}</body>", 1)
            else:
                html += INJECT_SCRIPT

            content = html.encode("utf-8")
            content_type = "text/html; charset=utf-8"

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.path.startswith("/proxy"):
            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)
            target = query.get("url", [""])[0].strip()
            target = unquote(target)
            if not target:
                self.send_error(400, "Missing ?url=")
                return
            self._proxy(target)
            return
        return super().do_GET()


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), ProxyHandler)
    print(f"Proxy server running on http://0.0.0.0:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    main()
