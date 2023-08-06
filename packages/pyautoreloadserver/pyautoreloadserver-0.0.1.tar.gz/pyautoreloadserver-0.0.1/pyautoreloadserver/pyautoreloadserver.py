import logging
import time
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from socketserver import TCPServer


logging.basicConfig(level=logging.INFO)


class Server(HTTPServer):
    pass


class RequestHandler(SimpleHTTPRequestHandler):
    pass


class AutoReloadHTTPServer:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 8000,
        root: str = ".",
        delay: float = 0.001,
        ServerClass: TCPServer = Server,
        RequestHandlerClass: BaseHTTPRequestHandler = RequestHandler,
    ) -> None:
        self._delay = delay
        RequestHandlerClass.directory = root
        self._httpd = ServerClass((host, port), RequestHandlerClass)
        self._stop_flag = False

    def serve(self) -> None:
        """
        Starts the server
        """
        try:
            host, port = self._httpd.server_address
            log_msg = f"Starting server. Visit http://{host}:{port}"
            logging.info(log_msg    )
            while not self._stop_flag:
                self._httpd.handle_request()
                time.sleep(self._delay)
        except KeyboardInterrupt as e:
            logging.info("Quitting server...")
            logging.error(e)

    def stop(self) -> None:
        """
        Stops serving
        """
        self._stop_flag = True
