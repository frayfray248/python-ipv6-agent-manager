#!/usr/bin/python3

def get_command(key):
    f = open("commands.conf", 'r')
    command = None
    for line in f:
        command_line = line.split()
        if (key == command_line[0]):
            command_line.remove(key)
            command = command_line
            break
    f.close()
    return command
        
