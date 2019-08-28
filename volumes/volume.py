from flask import Flask
from flask_api import status
import socket
import os
import sys
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def list_dir():
    my_hostname = socket.gethostname()
    my_address = socket.gethostbyname(my_hostname)
    my_task_id = os.environ.get('TASK_ID')
    my_node_hostname = os.environ.get('NODE_HOSTNAME')

    message = '<h1>Experiment with Persistent Volumes in Docker Swarm</h1>\n'
    message += '<h2>My IP address is '+my_address+'</h2>\n'
    message += '<h2>My Task ID is '+my_task_id+'</h2>\n'
    message += '<h2>I run on Node '+my_node_hostname+'</h2>\n'
    message += '<h3>Listing of /data directory:</h3>'
    message += '<table>\n'
    message += '<tr> <th>Name</th> <th>Type</th> </tr>\n'
    with os.scandir('/data') as dir:
      for entry in dir:
        if entry.is_file():
            message += '<tr> <td>'+entry.name+'</td> <td>file</td> </tr>\n'
        elif entry.is_dir():
            message += '<tr> <td>'+entry.name+'</td> <td>directory</td> </tr>\n'
        else:
            message += '<tr> <td>'+entry.name+'</td> <td>other</td> </tr>\n'
      dir.close()
    message += '</table>\n'
    return message

@app.route('/create')
def new_file():
    name = '/data/'+datetime.now().strftime('%H-%M-%S')
    file = open(name, 'w+')
    if file:
      return '<h2>File '+name+' created</h2>'
    else:
      return '<h2>Failed to create the file</h2>'

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
