"""
Network utilities: internet check for Auto mode.
"""

import socket
import urllib.request
import urllib.error


def is_internet_available(timeout: float = 5.0) -> bool:
    """
    Check if internet is reachable (for Auto mode: prefer online when possible).
    """
    test_hosts = [
        ("https://api.openai.com", "https"),
        ("https://www.google.com", "https"),
        ("8.8.8.8", "socket"),
    ]
    for target, method in test_hosts:
        try:
            if method == "https":
                req = urllib.request.Request(target, method="HEAD")
                with urllib.request.urlopen(req, timeout=timeout) as _:
                    return True
            elif method == "socket":
                sock = socket.create_connection((target, 443), timeout=timeout)
                sock.close()
                return True
        except (urllib.error.URLError, OSError, socket.timeout):
            continue
    return False
