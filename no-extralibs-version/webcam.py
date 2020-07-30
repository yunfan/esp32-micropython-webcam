import socket
import uos
import network
import machine
import time
import camera
import _thread

led = machine.Pin(4, machine.Pin.OUT)
camLock = _thread.allocate_lock()

def setup_conn(port, accept_handler):
    global listen_s
    listen_s = socket.socket()
    listen_s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ai = socket.getaddrinfo("0.0.0.0", port)
    addr = ai[0][4]

    listen_s.bind(addr)
    listen_s.listen(1)
    if accept_handler:
        listen_s.setsockopt(socket.SOL_SOCKET, 20, accept_handler)
    for i in (network.AP_IF, network.STA_IF):
        iface = network.WLAN(i)
        if iface.active():
            print("WebCam daemon started on http://%s:%d" % (iface.ifconfig()[0], port))
    return listen_s


def accept_conn(listen_sock):
    try:
        cl, remote_addr = listen_sock.accept()
        print("\nWebCam connection from:", remote_addr)

        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break

        print("\nWebCam request parsing Done:")

        led.on()
        with camLock:
            buf = camera.capture()
        led.off()
        print(type(buf), len(buf))

        cl.send('HTTP/1.0 200 OK\r\nContent-Type: image/jpeg\r\nContent-Length: {}\r\n\r\n'.format(len(buf)))
        cl.send(buf)
    finally:
        if cl:
            cl.close()
        led.off()
        print("finally request done")


def start(port=8267):
    camera.init()
    setup_conn(port, accept_conn)
