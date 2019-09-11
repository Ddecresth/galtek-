import asyncio, sys
import escape_room_main as er

S_PORT = 21207
HOST       = '192.168.200.52'
PORT     = 19003

class Server3(asyncio.Protocol):

    def __init__(self):
        print("I'm running")    

    def connection_made(self, transport):
        self.transport = transport
        self.game = er.EscapeRoomGame(output=self.write)
        self.game.create_game()
        self.game.start()

    def data_received(self, data):
        lines = data.decode().split("<EOL>\n")
        for line in lines:
            if not line: continue
            print("Received: {}".format(line))
            output = self.game.command(line)

    def write(self, msg):
        msg += "<EOL>\n"
        self.transport.write(msg.encode())

    def connection_lost(self):
        print("Connection close")


def main(args):
	loop = asyncio.get_event_loop()
	coro = loop.create_server(Server3,'', S_PORT) 
	server = loop.run_until_complete(coro)

	try:
		loop.run_forever()
	except KeyboardInterrupt:
		pass

	server.close()
	loop.run_until_complete(server.wait_close())
	loop.close()

if __name__ == "__main__":
    main(sys.argv[1:])

