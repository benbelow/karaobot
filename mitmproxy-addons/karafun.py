"""
Run as follows: mitmproxy -s karafun.py
"""
from mitmproxy import ctx

class Karafun:
    # Intercept all responses
    # API docs: https://docs.mitmproxy.org/stable/api/mitmproxy/http.html#HTTPFlow
    def response(self, flow):
        request_path = flow.request.path

        # Only modify the lyrics
        if request_path.find("request.php"):
            flow.response.text = flow.response.text.replace("creep", "crêpe")
            # TODO: interpret response XML, replace words and reconstruct

addons = [Karafun()]