import urllib.request, json, requests


def mock_call(types, path, parameters):
    data = {}
    for params in parameters:
        if params['in'] == 'path':
            path = path.replace("{" + params['name'] + "}", params['value'])
        print(types, path, parameters)
        data[params['name']] = params['value']
    if types == 'get':
        r = requests.get(url = path, params = data)
    elif types == 'post':
        r = requests.post(url = path, data = params)
    print(r)

def get_parameter_values(types, path, parameters):
    for params in parameters:
        print("Endpoint: " + path)
        print("Request Type: " + types)
        print("Name of the Parameter: " + params['name'])
        params['value'] = input('Enter ' + params['name'] + ' value:')
    return types, path, parameters



input_type = input("For Doc enter 1 else any other character for URL")
if (int(input_type) == 1):
    with urllib.request.urlopen("https://petstore.swagger.io/v2/swagger.json") as url:
        data = json.loads(url.read().decode())
        for paths in data['paths']:
            for types in data['paths'][paths]:
                params = []
                for parameters in data['paths'][paths][types]['parameters']:
                    param = {}
                    param['type'] = parameters['type'] if 'type' in parameters else None 
                    param['in'] = parameters['in']
                    param['name'] = parameters['name']
                    params.append(param)
                types, path, params = get_parameter_values(types, paths, params)
                mock_call(types, paths, params)

        

