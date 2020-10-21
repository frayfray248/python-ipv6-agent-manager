#!/usr/bin/python3

import sys, asyncio, utils, subprocess, struct

HOST = "an ipv6 address"
PORT = "12345"

#This is the main function of the ipv6 agent server. It listens for a connection and a command key string.
#The command key is matched with a shell command from a commands file. The shell command is executed and the
#output is sent to the manager. 
async def serve(reader, writer):
    try:
        key = await reader.readline() #receiving command key
	#retrieving shell command array from a commands file or None if no command found
        command = utils.get_command(key.decode('utf-8').strip())
        if command == None: #shell command validation
            writer.write("No command found".encode('utf-8'))
        else:
	    #executing shell command and saving the output
            output = subprocess.check_output(command, encoding='utf-8')
	    #encoding and sending the output to the manager
            encoded_output = output.encode('utf-8')
            writer.write(encoded_output)
        await writer.drain()
        writer.close()
       
    except Exception as e:
        print(e)

#ipv6 server creation
async def main():
    server = await asyncio.start_server(serve, HOST, PORT)
    print("SERVER: started server (" + str(HOST) + ", " + str(PORT) + ")")
    await server.serve_forever()
asyncio.run(main())


