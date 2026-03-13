import json
import mitmproxy
import os
import shutil
import stat
import yaml

with open('config.yml', 'r') as f:
    dictConfig = yaml.load(f, Loader = yaml.FullLoader)

class RequestExtractor:
    def request(self, flow: mitmproxy.http.HTTPFlow):
        match flow.request.method:
            case 'PUT' | 'PATCH':
                global nRequest
                logPath = os.path.join(logDirPath, f'request{nRequest}.sh')
                with open(logPath, 'w') as f:
                    jsonBody = json.dumps(json.loads(flow.request.content.decode('utf-8')), indent = 4)
                    f.write(f'az rest --method {flow.request.method} \\\n')
                    f.write(f'--url {flow.request.url} \\\n')
                    f.write(f'--headers "Content-Type=application/json" \\\n')
                    f.write(f'--body \'\n')
                    f.write(f'{jsonBody}\'')
                
                os.chmod(logPath, os.stat(logPath).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                nRequest += 1
        
        return

logDirPath = os.path.join(dictConfig['path']['main'], dictConfig['path']['log'])
shutil.rmtree(logDirPath)
os.makedirs(logDirPath, exist_ok = True)
nRequest = 0

addons = [RequestExtractor()]