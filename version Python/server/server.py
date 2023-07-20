# coding: utf-8

import socket
import threading
import logging
import datetime
#import os
import tkinter as tk
#from tkinter import messagebox

HOST = '192.168.211.1'
PORT = 5000

clients = []
file_list = {}
logging.basicConfig(filename=f'server.log',level=logging.INFO)

def handle_connection(conn,addr):
    while True:
        try:
            data = conn.recv(1024).decode()
        except:
            clients.remove((conn,addr))
            logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - Connection closed with{addr}')
            break
        if not data:
            continue
        if data.startswith('send_files'):
            filenames = data.split(':')[1].split(',')
            with open('file_list.txt','a') as f:
                for file in filenames:
                    if file in file_list:
                        file_list[file].append(addr)
                    else:
                        file_list[file] = [addr]
                    f.write(f'{file}-{addr[0]}:{addr[1]}--->{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}\n')
            logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - File list updated with:{filenames} from {addr}')
        elif data.startswith('search_file'):
            filename = data.split(':')[1]
            if filename in file_list:
                locations = file_list[filename]
                if len(locations) > 0:
                    conn.send(f'File found: {filename}, Locations:{file_list[filename]}'.encode())
                    logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - File found:{filename},Locations:{locations}')
                else:
                    conn.send(f'File not found:{filename}'.encode())
                    logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - File not found:{filename}')
        elif data.startswith('download'):
            filename = data.split(':')[1]
            with open(filename,'rb') as f:
                file_data = f.read()
            conn.sendall(file_data)
    conn.close()

def accept_clients():
    while True:
        conn,addr = s.accept()
        clients.append((conn,addr))
        logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}- Connection established with {addr}')
        threading.Thread(target=handle_connection,args=(conn,addr)).start()

def start_server():
    threading.Thread(target=accept_clients).start()
    status_label.config(text='Server started')

def stop_server():
    s.close()
    status_label.config(text='Server stopped')

def update_files_list():
    with open('file_list.txt','r') as f:
        files_list_label.config(text=f.read())

def main():
    global s
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen()
    logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - Server started at {HOST}:{PORT}')

    #GUI
    global status_label,files_list_label
    root = tk.Tk()
    root.title('Server')
    root.geometry('400x400')

    status_label = tk.Label(root, text='Server not started',font=('Arial',12))
    status_label.pack(pady=10)

    start_button = tk.Button(root,text='Start server',command=start_server)
    start_button.pack(pady=10)

    stop_button = tk.Button(root,text='Stop server',command=stop_server)
    stop_button.pack(pady=10)

    files_list_label = tk.Label(root,text='',font=('Arial',12))
    files_list_label.pack(pady=10)

    update_button = tk.Button(root,text='Update Files List',command=update_files_list)
    update_button.pack(pady=10)

    root.mainloop()

if __name__ == '__main__':
    main()

# class Server:
#     def __init__(self):
#         self.socket = socket.socket()
#         self.socket.bind(('192.168.211.1', 8000))
#         self.socket.listen()
#         self.file_list_file = "file_list.txt"
#         self.load_file_list()
#         self.log_file = open("server.log","a")
#         self.running = False

#     def handle_client(self, client_socket):
#         client_address = client_socket.getpeername()[0]
#         if client_address not in self.file_list:
#             self.file_list[client_address] = []

#         while True:
#             data = client_socket.recv(1024).decode()
#             if not data:
#                 break
#             if data.startswith("SHARE"):
#                 filename = data.split(":")[1]
#                 self.file_list[client_address].append(filename)
#                 self.save_file_list()
#                 self.log("File " + filename + "shared by " + client_address)
#             elif data.startswith("SEARCH"):
#                 query = data.split(":")[1]
#                 results = [filename + ":" + client_address for client_address, file_list in self.file_list.items()
#                 for filename in file_list if query in filename]
#                 if results:
#                     result_string = ",".join(results)
#                     client_socket.send(("SEARCHRESULT:"+result_string).encode())
#                 else:
#                     client_socket.send("SEARCHRESULT:No results found".encode())
#             elif data.startswith("DOWNLOAD"):
#                 filename = data.split(":")[1]
#                 ip_address = data.split(":")[2]
#                 port = int(data.split(":")[3])
#                 send_thread = threading.Thread(target=self.send_file,args=(client_socket,ip_address,port,filename))
#                 send_thread.start()
#         client_socket.close()

#     def send_file(self,client_socket,ip_address,port,filename):
#         with socket.socket() as s:
#             s.connect((ip_address,port))
#             s.send(("DOWNLOAD:"+filename).encode())
#             while data:
#                 client_socket.send(data)
#                 data = s.recv(1024)

#     def listen(self):
#         while self.running:
#             client_socket,address = self.socket.accept()
#             client_thread = threading.Thread(target=self.handle_client,args=(client_socket,))
#             client_thread.start()
#             self.log("Server is listening for connections")

#     def start(self):
#         self.running = True
#         listen_thread = threading.Thread(target=self.listen)
#         listen_thread.start()
#         self.log("Server has started")

#     def stop(self):
#         self.running = False
#         self.socket.close()
#         self.log("Server is stopped")

#     def save_file_list(self):
#         with open(self.file_list_file,"w") as f:
#             for client_address,file_list in self.file_list.items():
#                 for filename in file_list:
#                     f.write(client_address+":"+filename+"\n")

#     def load_file_list(self):
#         self.file_list = {}
#         if os.path.isfile(self.file_list_file):
#             with open(self.file_list_file,"r") as f:
#                 lines = f.readlines()
#                 for line in lines:
#                     client_address, filename = line.strip().split(":")
#                     if client_address not in self.file_list:
#                         self.file_list[client_address] = []
#                     self.file_list[client_address].append(filename)

#     def __del__(self):
#         self.log_file.close()

#     def log(self,message):
#         timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
#         log_entry = "["+timestamp + "]" + message + "\n"
#         self.log_file.write(log_entry)
#         self.log_file.flush()


# class ServerGUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Server")
#         self.server = Server()
#         self.create_widgets()

#     def create_widgets(self):
#         #start/stop buttons
#         self.start_button = tk.Button(self.root, text="Start server",command=self.start_server)
#         self.start_button.pack(padx=10,pady=10)
#         self.stop_button = tk.Button(self.root, text="Stop server",command=self.stop_server,state=tk.DISABLED)
#         self.stop_button.pack(padx=10,pady=10)

#         #file list box
#         self.file_list_frame = tk.Frame(self.root)
#         self.file_list_frame.pack(padx=10,pady=10)
#         tk.Label(self.file_list_frame,text="Files Shared by clients").pack()
#         self.file_listbox = tk.Listbox(self.file_list_frame, width=50)
#         self.file_listbox.pack(side=tk.LEFT,fill=tk.BOTH)
#         scrollbar = tk.Scrollbar(self.file_list_frame)
#         scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
#         self.file_listbox.config(yscrollcommand=scrollbar.set)
#         scrollbar.config(command=self.file_listbox.yview)
#         self.update_file_listbox()

#         #open file button
#         self.open_file_button = tk.Button(self.root,text="Open File",state=tk.DISABLED)
#         self.open_file_button.pack(padx=10,pady=10)

#         #logs button
#         self.logs_button = tk.Button(self.root,text="View Logs", command=self.view_logs)
#         self.logs_button.pack(padx=10,pady=10)

#     def update_file_listbox(self):
#         self.file_listbox.delete(0,tk.END)
#         for client_address,file_list in self.server.file_list.items():
#             for filename in file_list:
#                 self.file_listbox.insert(tk.END,filename + " (shared by " + client_address + ")")

#     def start_server(self):
#         self.server.start()
#         self.start_button.config(state=tk.DISABLED)
#         self.stop_button.config(state=tk.NORMAL)
#         self.open_file_button.config(state=tk.NORMAL)

#     def stop_server(self):
#         self.server.stop()
#         self.start_button.config(state=tk.NORMAL)
#         self.stop_button.config(state=tk.DISABLED)
#         self.open_file_button.config(state=tk.DISABLED)
#         self.update_file_listbox()

#     def open_file(self):
#         selection = self.file_listbox.curselection()
#         if not selection:
#             return
#         index = selection[0]
#         client_address,filename = self.server.file_list[index]
#         with open(filename,"r") as f:
#             file_contents = f.read()
#         messagebox.showinfo("File contents", file_contents)

#     def view_logs(self):
#         with open("server.log","r") as f:
#             log_contents = f.read()
#         messagebox.showinfo("Server Logs",log_contents)

#     def start(self):
#         self.root.mainloop()

# if __name__ == "__main__":
#     server_gui = ServerGUI()
#     server_gui.start()
