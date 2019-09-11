import asyncio

S_PORT = 21207
HOST   = '192.168.200.52'
PORT = 19003


GET_HAMMER = ['look', 'look mirror', 'get hairpin', 'look chest', 'unlock chest with hairpin', 'open chest', 'look in chest', 'get hammer from chest', 'unlock door with hairpin', 'open door']

def work_input(client, data):
    if client.state == "init":
        if "SUBMIT autograde command" not in data:
            pass
         
        else:
            client.state = "command" # update state
            client.write("SUBMIT,Debolina De,dde3@jhu.edu,1,{}".format(S_PORT))
    elif client.state == "command":
        if "SUBMIT: OK" in data:
            client.state = "client_test"
            for step in GET_HAMMER:
                client.write(step)
        elif "SUBMIT: FAIL" in data:
            pass
           
        else:
            
            pass
    elif client.state == "client_test":
        if "ClIENT TEST: OK" in data:
            client.state = "server_test"
            print("PASSED BY CLIENT!!") 
        else:
            pass
    elif client.state == "server_test":
        if "SERVER TEST: OK" in data:
            client.state = "done"
            print("SERVER PASSED!!") 
        else:
            pass
    
class NewClient3(asyncio.Protocol):
    # States
    STATES = ["init", "command", "client_test", "server_test"]

    def __init__(self):
        #self.proceed = False
        self.state = "init"
        pass

    def connection_made(self, transport):
        self.transport = transport
        print("Connected")

    def data_received(self, data):
        lines = data.decode().split("<EOL>\n")
        for line in lines:
            if not line: continue
            print(line)
            work_input(self, line)
                
    def write(self, msg):
        msg += "<EOL>\n"
        print("Data to send: {}".format(msg.encode()))
        self.transport.write(msg.encode())

    def connection_lost(self):
        print("Disconnected")    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(NewClient3, HOST, PORT)
    client = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
        
    client.close()
    loop.run_until_complete(client.close())
    loop.close()

