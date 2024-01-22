import threading
from queue import Queue

from flask import Flask

from neoscore.core import neoscore
from neoscore.core.point import ORIGIN
from neoscore.core.text import Text

"""
This example demonstrates a simple way to send messages to a Neoscore application from
external programs using a local HTTP server. This is a common way to perform
inter-process communication (IPC). This pattern allows any external program which can
send HTTP requests to communicate with a Neoscore application.

To run this example, you must first install the HTTP Server framework Flask using `pip
install flask`. Then run this script to start the server, and in another terminal you
can test it with `curl localhost:5000/set_text/anything`, or by simply loading that URL
in your browser. (The port number 5000 may vary - check the Flask startup logs)
"""


# The queue that carries messages between the Flask thread and Neoscore thread
message_queue = Queue()


# Flask code ############

app = Flask(__name__)


@app.route("/set_text/<text>")
def set_text(text: str):
    # Send messages between the Flask thread and the Neoscore refresh func thread
    # using a simple message queue.
    message_queue.put(text)
    return f'text set to "{text}"'


def run_flask():
    app.run()


# Start a new thread that will run the Flask application
t = threading.Thread(target=run_flask)
t.start()

# Set up Neoscore in the main thread
neoscore.setup()

main_text = Text(ORIGIN, None, "Change this text with an HTTP request")


def refresh_func(time: float) -> neoscore.RefreshFuncResult:
    request_render = False
    # Process all available messages from the Flask thread
    while not message_queue.empty():
        request_render = True
        msg = message_queue.get()
        main_text.text = msg
    # If our main loop doesn't make changes unless messages
    # trigger them, we can optimize our application by telling
    # Neoscore when we do or don't need a re-render.
    return neoscore.RefreshFuncResult(request_render)


neoscore.show(refresh_func)
