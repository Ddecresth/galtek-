Def new(client):
Import asyncio
Class ClientProtocol(asyncio.Protocol):
	Def __init__(self,loop):
		Self.loop=loop
	Def connection_made(self,transport):
		Self.transport=transport
	Def data_received(self.data):
		Print('Data received: {!r}'.format(data.decode()))
		Command=input()
		Command=command.encode() + b"<EOL>\n"
		Self.transport.write(command)
	Def connection_lost(self,exc):
		Print('connection lost!')
		Self.loop.stop()
		
HOST="0.0.0.0"
PORT="1234"
Loop=asyncio.get_event_loop()
Coro=loop.create_connection(lambda:ClientProtocol(loop),
Loop.run_until_complete(coro)
Loop.run_forever()
Exit()
