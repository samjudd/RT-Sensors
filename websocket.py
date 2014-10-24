import socket
import hashlib
import base64
import threading
import time

class ClientConnection:
    MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    HSHAKE_RESP = 'HTTP/1.1 101 Switching Protocols\r\n' + \
                  'Upgrade: websocket\r\n' + \
                  'Connection: Upgrade\r\n' + \
                  'Sec-WebSocket-Accept: %s\r\n' + \
                  '\r\n'
    
    def __init__(self, client):
        print('Handshaking...')
        self.handshake(client)
        print('Handshake successful...')

        try:
            threading.Thread(target=self.loop).start()
        except Exception as e:
            print("Exception %s" % (str(e)))

        print('Client closed: ' + str(address))
        
    def loop(self):
        while 1:
                data = self.receive_data(client)
                print("received [%s]" % (data,))
                self.send(data)
    
    def handshake(self, client):
        data = client.recv(2048)

        headers = {}
        lines = data.splitlines()
        for l in lines:
            parts = l.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]
        headers['code'] = lines[len(lines) - 1]

        key = headers['Sec-WebSocket-Key']
        resp_data = self.HSHAKE_RESP % (base64.b64encode(hashlib.sha1(key + self.MAGIC).digest()),)

        return client.send(resp_data)

class PyWSock:
    MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    HSHAKE_RESP = 'HTTP/1.1 101 Switching Protocols\r\n' + \
                  'Upgrade: websocket\r\n' + \
                  'Connection: Upgrade\r\n' + \
                  'Sec-WebSocket-Accept: %s\r\n' + \
                  '\r\n'
    LOCK = threading.Lock()

    clients = []

    def __init__(self, port):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', port))
        s.listen(5)
        while 1:
            print ('Waiting for connection...')
            connection, address = s.accept()
            print ('Connection from: ' + str(address))
            threading.Thread(target=self.handle_client, args=(connection, address)).start()
            self.LOCK.acquire()
            self.clients.append(connection)
            self.LOCK.release()

    def handle_client(self, client, address):
        print('Handshaking...')
        self.handshake(client)
        print('Handshake successful...')
        self.send('hello')

        try:
            while 1:
                data = self.receive_data(client)
                print("received [%s]" % (data,))
                self.send(data)
        except Exception as e:
            print("Exception %s" % (str(e)))

        print('Client closed: ' + str(address))

        self.LOCK.acquire()
        self.clients.remove(client)
        self.LOCK.release()

        client.close()

    def handshake(self, client):
        data = client.recv(2048)

        headers = {}
        lines = data.splitlines()
        for l in lines:
            parts = l.split(": ", 1)
            if len(parts) == 2:
                headers[parts[0]] = parts[1]
        headers['code'] = lines[len(lines) - 1]

        key = headers['Sec-WebSocket-Key']
        resp_data = self.HSHAKE_RESP % (base64.b64encode(hashlib.sha1(key + self.MAGIC).digest()),)

        return client.send(resp_data)

    def receive_data(self, client):
        # as a simple server, we expect to receive:
        # - all data at one go and one frame
        # - one frame at a time
        #    - text protocol
        #    - no ping pong messages
        data = bytearray(client.recv(512))
        if (len(data) < 6):
            raise Exception("Error reading data")
        # FIN bit must be set to indicate end of frame
        assert (0x1 == (0xFF & data[0]) >> 7)
        # data must be a text frame
        # 0x8 (close connection) is handled with assertion failure
        assert (0x1 == (0xF & data[0]))
        # assert that data is masked
        assert (0x1 == (0xFF & data[1]) >> 7)
        datalen = (0x7F & data[1])

        #print("received data len %d" %(datalen,))

        str_data = ''
        if datalen > 0:
            mask_key = data[2:6]
            masked_data = data[6:(6 + datalen)]
            unmasked_data = [masked_data[i] ^ mask_key[i % 4] for i in range(len(masked_data))]
            str_data = str(bytearray(unmasked_data))
        return str_data

    def send(self, data):
        # 1st byte: fin bit set. text frame bits set.
        # 2nd byte: no mask. length set in 1 byte. 
        resp = bytearray([0b10000001, len(data)])
        # append the data bytes
        for d in bytearray(data):
            resp.append(d)

        self.LOCK.acquire()
        for client in self.clients:
            try:
                client.send(resp)
            except:
                print("error sending to a client")
        self.LOCK.release()

    def close(self):
        self.LOCK.acquire()
        for client in self.clients:
            client.close()
            self.clients.remove(client)
        self.LOCK.release()

    def loop(self):
        while True:
            self.send('hi')
            time.sleep(100)
            
threading.Thread(target=self.handle_client, args=(connection, address)).start()
    ws = PyWSock(2005)
