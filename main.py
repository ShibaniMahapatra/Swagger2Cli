import requests
import json
from prettytable import PrettyTable

url = input("Input Swagger URL: ")
x = requests.get(url)
content = x.content.decode("utf-8")


swagger = json.loads(content)
host = swagger["host"] + swagger["basePath"]
schemes = swagger["schemes"][0] + "://"


class API(object):
    def get(self, url):
        return requests.get(url=url)

    def post(self, url, headers, data, files):
        return requests.post(url=url, data=data, headers=headers, files=files)

    def delete(self, url, headers, data):
        return requests.delete(url=url, data=data, headers=headers)


api_handler = API()

for endpoint, endpoint_value in swagger["paths"].items():
    url = host
    for action, action_value in endpoint_value.items():
        raw_endpoint = endpoint
        print("ENDPOINT: ", endpoint)
        print("REQUEST: ", action.upper())
        data = {}
        headers = {}
        files = {}
        for parameter in action_value["parameters"]:
            parameter_value = input("Input Parameter Value: " + parameter["name"] + " = ")
            if parameter["in"] == 'path':
                var = "{" + parameter["name"] + "}"
                raw_endpoint = raw_endpoint.replace(var, parameter_value)
            elif parameter["in"] == 'header':
                headers[parameter["name"]] = parameter_value
            elif parameter['type'] == 'file':
                    files = { parameter['name']: open(parameter_value, 'rb') }
            else:
                data[parameter["name"]] = parameter_value
        url = schemes + host + raw_endpoint
        files_count = len(files.keys())
        table = PrettyTable(["URL", "HEADERS", "DATA", "FILES"])
        table.add_row([url, headers, data, len(files.keys()) if files else None])
        print(table)
        if action == 'get':
            response = api_handler.get(url)
            print(response)
            print(response.content)
        if action == 'post':
            response = api_handler.post(url, headers, data, files)
            print(response)
            print(response.content)
        if action == 'delete':
            response = api_handler.delete(url, headers, data)
            print(response)
            print(response.content)
        print("---------------------------------")