"""
Run as follows: mitmproxy -s karafun.py
"""

from play_song import handle_play_song
from queue_song import handle_queue_song

class Karafun:
    # Intercept all responses
    # API docs: https://docs.mitmproxy.org/stable/api/mitmproxy/http.html#HTTPFlow
    def response(self, flow):
        log = open("../log.txt", "a")
        request_path = flow.request.path

        if "info.php" in request_path:
            handle_queue_song(flow, log)

        if "request.php" in request_path:
            handle_play_song(flow, log)


addons = [Karafun()]
