import asyncio
import fastmcp
import os
import subprocess
import yaml

import structure

with open('config.yml', 'r') as f:
    dictConfig = yaml.load(f, Loader = yaml.FullLoader)

bLogging = False
listHttpsLog = []
server = fastmcp.FastMCP('https-logging')
lock = asyncio.Lock()

@server.tool()
async def startHttpsLogging():
    async with lock:
        listHttpsLog.clear()
        global bLogging
        bLogging = True

    return

@server.tool()
async def logHttps(httpsLog: structure.HttpsLog):
    async with lock:
        if bLogging:
            listHttpsLog.append(httpsLog)

    return

@server.tool()
async def stopHttpsLogging():
    async with lock:
        global bLogging
        bLogging = False
        
        return listHttpsLog

if __name__ == '__main__':
    try:
        process = subprocess.Popen(f"mitmdump -s {os.path.join(dictConfig['path']['main'], dictConfig['path']['code'], 'proxy2McpServer.py')} -p {dictConfig['port']['mcpServerProxy']}", shell=True, stdout = subprocess.DEVNULL)
        server.run(transport = 'streamable-http', port = dictConfig['port']['mcpServer'])
    finally:
        process.terminate()