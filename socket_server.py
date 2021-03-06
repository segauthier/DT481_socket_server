import time
import socket
import os
from os import path
import json
import csv
import threading
import pytz
import datetime

from wipy.lib.box_data_template import *

host_port = 8002

app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(os.path.join(app_dir, r"DT481_bokeh_serveur"), "data")

MoxBox = "MoxBox"
client_ls = []
init = True


def formatData2csv(timestamp, data, header=False):
    list2write = []
    if header:
        for k in list(data.keys()):
            list2write = list2write + [k+"_"+l for l in list(data[k].keys())]
        list2write = ["timestamp"] + list2write
    else:
        for k in list(data.keys()):
            list2write = list2write + list(data[k].values())
        list2write = [timestamp] + list2write

    return list2write


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.clientsocket.setblocking(0)
        print("Starting new client thread at %s, port: %s" % (self.ip, self.port, ))

    def run(self):
        time.sleep(10)
        bool_run = True
        i_error = 0
        while bool_run:
            try:
                self.clientsocket.settimeout(10)
                response = self.clientsocket.recv(4096)
                self.clientsocket.settimeout(None)
            except socket.timeout:
                response = ""
                self.terminate()

            if response != "":
                print("Client id :", self.ident)
                try:
                    self.write_csv(json.loads(response))
                    print(response)
                    i_error = 0
                except (json.JSONDecodeError, PermissionError) as e:
                    print("json decoding error.")
                    print(e)
                    i_error += 1
                    if i_error > 20:
                        self.terminate()
                        bool_run = False
            else:
                bool_run = False

    def terminate(self):
        print("Client ", self.ident, "was closed.")
        self.clientsocket.close()

    @staticmethod
    def write_csv(data):
        box_id = data[BOX_params][BOX_ID]
        box_dir = path.join(data_path, MoxBox + str(box_id))

        write_header = False

        # Manage MoxBox folders
        if not path.isdir(box_dir):
            os.makedirs(box_dir)
        
        current_date = datetime.datetime.now(pytz.timezone('Europe/Paris'))
        date_tag = current_date.strftime('%Y%m%d')
        timestamp = current_date.strftime('%Y%m%d %H:%M:%S')
        curr_file_name = MoxBox + str(box_id) + '_' + str(date_tag) + '.csv'
        curr_path = path.join(path.join(data_path, MoxBox + str(box_id)), curr_file_name)

        if not os.path.exists(curr_path):
            write_header = True

        with open(curr_path, 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t', lineterminator="\n")
            if write_header:
                csv_writer.writerow(formatData2csv(timestamp, data, True))

            csv_writer.writerow(formatData2csv(timestamp, data))


def start():
    global init
    while True:
        if init:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostname()
            s.bind((host, host_port))
            s.listen(5)
            print("Starting server and listening ...")
            print("Host name :", host)
            init = False

        try:
            client, address = s.accept()
            new_client = ClientThread(address, host_port, client)
            client_ls.append(new_client)
            new_client.start()

        except OSError:
            print("Connection error:")
            for c in client_ls:
                c.terminate()
            s.close()
            init = True


if __name__ == '__main__':
    start()
