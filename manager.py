#!/usr/bin/env python3

import sys, asyncio, utils


#This function reads a file with a list of agent addresses.
#These addresses are stored in an array and the function returns the array
def load_agents():
	agents = []
	f = open("agents.conf", 'r')
	for line in f:
		agents.append(line)
	return agents

#This is the main function of the ipv6 client manager. It receives a command key from the user which references
#a command key in a commands folder. If a valid key is found, it is sent to every agent address from
#an agents folder. The listening agents execute the command on their end and send the output to the manager.
#The manager then prints out the outputs grouped by agent addresses
async def manage():
	try:
	#Input loop for getting a command key from the user. If the command does not exist in the 
	#commands file, it reprompts the user for a valid command key.
		while(True):
			command = input("Enter a command: ")
			if (utils.get_command(command) == None): #checking if command key exists in the commands file
				print("Command not found in commands.conf. Please Enter a valid command")
			else:
				break
	
		agents = load_agents() #retrieve agents array
	
	#iterate through every agent
		for a in agents:
			try:
				print("AGENT: " + a.strip()) #current agent
	    			#connecting to the current agent
				reader, writer = await asyncio.open_connection(a.strip(), "12345")
	    			#sending command key
				writer.write(command.encode('utf-8') + b'\n')
				await writer.drain()
	    			#receiving the output of the command executed by the agent
				data = await reader.read()
				print(data.decode('utf-8'))	#printing output
				writer.close()
				await writer.wait_closed()
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)

asyncio.run(manage())
