import asyncio
import fastmcp
from mitmproxy import http
import yaml

import structure

with open('config.yml', 'r') as f:
    dictConfig = yaml.load(f, Loader = yaml.FullLoader)

class HttpsExtractor:
    def __init__(self):
        self.listHttpsLog = []
        self.lock = asyncio.Lock()

        return
    
    async def request(self, flow: http.HTTPFlow):
        match flow.request.method:
            case 'PUT' | 'PATCH':
                async with self.lock:
                    self.listHttpsLog.append(structure.HttpsLog(
                        method = flow.request.method,
                        url = flow.request.url,
                        requestBody = flow.request.content.decode('utf-8')
                    ))
        
        return
    
    async def response(self, flow: http.HTTPFlow):
        async with self.lock:
            for i in range(len(self.listHttpsLog)):
                if self.listHttpsLog[i].url == flow.request.url and self.listHttpsLog[i].responseBody == '':
                    self.listHttpsLog[i].responseBody = flow.response.content.decode('utf-8')
                    
                    async with fastmcp.Client(f'http://127.0.0.1:{dictConfig["port"]["mcpServer"]}/mcp') as client:
                        await client.call_tool('logHttps', {
                            "httpsLog": self.listHttpsLog[i]
                        })
                    
                    del self.listHttpsLog[i]

                    break

        return

addons = [HttpsExtractor()]