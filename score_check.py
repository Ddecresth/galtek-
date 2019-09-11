import asyncio
import sys

AG_IP   = '192.168.200.52'
AG_PORT = 19002

class ScoreClient(asyncio.Protocol):
    def __init__(self, result_id):
        self.result_id = result_id

    def connection_made(self, transport):
        self.transport = transport
        print("Connected")

    def data_received(self, data):
        data = data.decode()
        lines = data.split("<EOL>\n")
        for line in lines:
            if not line: continue
            print(line)
            if "SUBMIT autograde command" in data:
                self.write("RESULT,{}".format(self.result_id))

    def write(self, msg):
        msg += "<EOL>\n"
        print("Data to send: {}".format(msg.encode()))
        self.transport.write(msg.encode())

    def connection_lost(self):
        print("Disconnected")

def main(args):
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: ScoreClient(args[0]), AG_IP, AG_PORT)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
        
    client.close()
    loop.run_until_complete(client.close())
    loop.close()


if __name__ == "__main__":
    main(sys.argv[1:])
