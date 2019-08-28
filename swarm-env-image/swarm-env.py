from flask import Flask
from flask_api import status
import socket
import os
import sys
import dns.resolver
import netifaces


app = Flask(__name__)

disabled = False

@app.route('/')
def swarm_env():
    my_hostname =        socket.gethostname()
    my_address =         socket.gethostbyname(my_hostname)

    if disabled:
        return 'Service disabled @'+my_hostname+'@'+my_address, status.HTTP_503_SERVICE_UNAVAILABLE

    env_service_name =   os.environ.get('SERVICE_NAME')
    if env_service_name:
      service_address =  str(socket.gethostbyname_ex(env_service_name)[2])
    dns_resolver = dns.resolver.Resolver()

    message = '<h1>Swarm Environment Information v1</h1>\n'
    message += '<h2>My hostname is '+my_hostname+'</h2>\n'
    message += '<h2>IP Address of my hostname is '+my_address+'</h2>\n'
    message += '<h3>Environment Variables:</h3>'
    message += '<table>\n'
    message += '<tr> <th>Environment Variable</th> <th>Value</th> </tr>\n'
    for variable in os.environ.keys():
        bold = ''
        unbold = ''
        if variable in ['NODE_HOSTNAME','SERVICE_NAME','TASK_SLOT']:
            bold = '<b>'
            unbold = '</b>'
        message += '<tr> <td>'+variable+'</td> <td>'+bold+os.environ.get(variable)+unbold+'</td> </tr>\n'
    message += '</table>\n'
    message += '<h3>Address of Service "'+env_service_name+'" Endpoint: '+service_address+'</h3>\n'
    message += '<h3>Addresses of Service "'+env_service_name+'" Tasks:</h3>\n<ul>\n'
    for addr in sorted(dns_resolver.query("tasks."+env_service_name, "A")):
        message += '<li>'+str(addr)+', DNS Name: '+str(socket.gethostbyaddr(str(addr))[0])+'</li>\n'
    message += '</ul>\n'
    message += '<h3>My Network Interfaces</h3>\n<table>\n'
    message += '<tr> <th>Interface</th> <th>IPv4 Address</th> </tr>\n'
    for interface in netifaces.interfaces():
        if_addr = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in if_addr:
            message += '<tr> <td>'+interface+'</td> <td>'+str(if_addr[netifaces.AF_INET][0]['addr'])+'</td> </tr>\n'
        else:
            message += '<tr> <td>'+interface+'</td> <td>No IPv4 Address</td> </tr>\n'
    message += '</table>\n'

    return message

@app.route('/disable')
def disable():
    global disabled
    disabled = True
    my_hostname =        socket.gethostname()
    my_address =         socket.gethostbyname(my_hostname)
    return '<h2>Disabling '+my_hostname+'@'+my_address+'</h2>'

@app.route('/healthcheck')
def healtcheck():
    global disabled
    if disabled:
        return 'Service disabled', status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        return 'OK', status.HTTP_200_OK

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
