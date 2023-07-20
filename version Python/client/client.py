# coding: utf-8

import tkinter as tk
from tkinter import filedialog
import socket
import logging
import os
import datetime
import threading

HOST = '192.168.211.1'
PORT = 5000
FILE_PORT = 5001

logging.basicConfig(filename='client.log',level=logging.INFO)

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

def send_files(conn,filenames):
    conn.send(f'send_files:{",".join(filenames)}'.encode())
    logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - Sent files: {filenames}')

def search_file():
    filename = search_entry.get().strip()
    if filename:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.connect((HOST,PORT))
            s.send(f'search_file:{filename}'.encode())
            response = s.recv(1024).decode()
            if response.startswith('File found'):
                logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - {response}')
                result_label.config(text=response)
                locations = response.split(':')[-1].split(',')
                if len(locations) > 0:
                    ip_port = locations[0].split(':')
                    if len(ip_port) > 1:
                        ip,port = ip_port
                        download_file(ip[1:-1],int(port),filename)
                    #else:
                        #logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}-Invalid file location')
                else:
                    logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - File not found:{filename}')
                    result_label.config(text=f'File not found:{filename}')
            else:
                #logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - {response}')
                result_label.config(text=response)

def listen():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind(('localhost',FILE_PORT))
        s.listen()
        while True:
            conn,addr = s.accept()
            data = conn.recv(1024).decode()
            if data.startswith('download'):
                filename = data.split(':')[1]
                with open(filename,'rb') as f:
                    while True:
                        file_data = f.read(1024)
                        if not file_data:
                            break
                    conn.sendall(file_data)
            conn.close()
server_thread = threading.Thread(target=listen)
server_thread.daemon = True
server_thread.start()

def download_file(ip,port,filename):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        try:
            s.connect((ip,FILE_PORT))
        except ConnectionRefusedError:
            logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")}-Connection refused')
            result_label.config(text='Connection refused')
            return
        s.send(f'download:{filename}'.encode())
        with open(filename,'wb') as f:
            while True:
                conn,addr = s.accept()
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
        logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - {filename} downloaded successfully')
        result_label.config(text=f'{filename} downloaded successfully')

def connect():
    ip = ip_entry.get().strip()
    port = port_entry.get().strip()
    if ip and port:
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            #s.bind(('localhost',0))
            s.connect((ip,int(port)))
            filename = select_file()
            if os.path.isfile(filename):
                filenames = [filename.split('/')[-1]]
                send_files(s, filenames)
                filename = filename.split('/')[-1]
                search_file()
            else:
                logging.info(f'{datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")} - Invalid file path')

#GUI
root = tk.Tk()
root.title('Client')
root.geometry('400x400')

ip_label = tk.Label(root,text='Server IP Address:',font=('Arial',12))
ip_label.pack(pady=10)

ip_entry = tk.Entry(root,font=('Arial',12))
ip_entry.pack(pady=10)

port_label = tk.Label(root,text='Server Port:',font=('Arial',12))
port_label.pack(pady=10)

port_entry = tk.Entry(root,font=('Arial',12))
port_entry.pack(pady=10)

connect_button = tk.Button(root,text='Connect',command=connect)
connect_button.pack(pady=10)

search_label = tk.Label(root,text='Enter the filename to search:',font=('Arial',12))
search_label.pack(pady=10)

search_entry = tk.Entry(root,font=('Arial',12))
search_entry.pack(pady=10)

search_button = tk.Button(root,text='Search',command=search_file)
search_button.pack(pady=10)

result_label = tk.Label(root,text='',font=('Arial',12))
result_label.pack(pady=10)

download_label = tk.Label(root,text='Enter file name to download:',font=('Arial',12))
download_label.pack(pady=10)

download_entry = tk.Entry(root,font=('Arial',12))
download_entry.pack(pady=10)

ip_port_label = tk.Label(root,text='Enter the IP address and port of the client who owns the file(separated by comma):',
font=('Arial',12))
ip_port_label.pack(pady=10)

ip_port_entry = tk.Entry(root,font=('Arial',12))
ip_port_entry.pack(pady=10)

download_button = tk.Button(root,text='Download',command=lambda: download_file(*ip_port_entry.get().strip().split(','),
download_entry.get().strip()))
download_button.pack(pady=10)

root.mainloop()

# class ClientGUI:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("File sharing client")
#         self.socket = None
#         #self.file_listbox = {}
#         self.file_list = []
#         self.search_results = []
#         self.create_widgets()
#         self.log_file = open("client.log","a")

#     def create_widgets(self):
#         #server connection frame
#         self.connection_frame = tk.Frame(self.root)
#         self.connection_frame.pack(padx=10,pady=10)
#         tk.Label(self.connection_frame,text="Server IP Address").pack(side=tk.LEFT)
#         self.server_ip_entry = tk.Entry(self.connection_frame,width=20)
#         self.server_ip_entry.pack(side=tk.LEFT)
#         tk.Label(self.connection_frame,text="Server Port").pack(side=tk.LEFT)
#         self.server_port_entry = tk.Entry(self.connection_frame,width=10)
#         self.server_port_entry.pack(side=tk.LEFT)
#         connect_button = tk.Button(self.connection_frame,text="Connect",command=self.connect_to_server)
#         connect_button.pack(side=tk.LEFT)

#         #Share file/directory frame
#         # self.file_listbox = tk.Listbox(self.root)
#         # self.file_listbox.pack()
#         self.share_frame = tk.Frame(self.root)
#         self.share_frame.pack(padx=10,pady=10)
#         tk.Label(self.share_frame,text="Share File/Directory").pack(side=tk.LEFT)
#         self.share_entry = tk.Entry(self.share_frame,width=50)
#         self.share_entry.pack(side=tk.LEFT)
#         browse_button = tk.Button(self.share_frame,text="Browse",command=self.browse_file_or_directory)
#         browse_button.pack(side=tk.LEFT)
#         share_button = tk.Button(self.share_frame,text="Share",command=self.share_file_or_directory)
#         share_button.pack(side=tk.LEFT)

#         #File list box
#         self.file_list_frame = tk.Frame(self.root)
#         self.file_list_frame.pack(padx=10,pady=10)
#         tk.Label(self.file_list_frame,text="Files Shared").pack()
#         self.file_listbox = tk.Listbox(self.file_list_frame,width=50)
#         self.file_listbox.pack(side=tk.LEFT,fill=tk.BOTH)
#         scrollbar = tk.Scrollbar(self.file_list_frame)
#         scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
#         self.file_listbox.config(yscrollcommand=scrollbar.set)
#         scrollbar.config(command=self.file_listbox.yview)
#         self.update_file_listbox()

#         #Search file frame
#         self.search_frame = tk.Frame(self.root)
#         self.search_frame.pack(padx=10,pady=10)
#         tk.Label(self.search_frame,text="Search File").pack(side=tk.LEFT)
#         self.search_entry = tk.Entry(self.search_frame,width=50)
#         self.search_entry.pack(side=tk.LEFT)
#         search_button = tk.Button(self.search_frame,text="Search",command=self.search_for_file)
#         search_button.pack(side=tk.LEFT)

#         #Search results frame
#         self.search_results_frame = tk.Frame(self.root)
#         self.search_results_frame.pack(padx=10,pady=10)
#         tk.Label(self.search_results_frame,text="Search Results").pack()
#         self.search_results_listbox = tk.Listbox(self.search_results_frame,width=50)
#         self.search_results_listbox.pack(side=tk.LEFT,fill=tk.BOTH)
#         scrollbar = tk.Scrollbar(self.search_results_frame)
#         scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
#         self.search_results_listbox.config(yscrollcommand=scrollbar.set)
#         scrollbar.config(command=self.search_results_listbox.yview)
#         self.search_results_listbox.bind("<Double-Button-1>", self.download_file)
#         self.update_search_results_listbox()

#         #Logs frame
#         self.logs_frame = tk.Frame(self.root)
#         self.logs_frame.pack(padx=10,pady=10)
#         logs_button = tk.Button(self.logs_frame,text="View Logs",command=self.view_logs)
#         logs_button.pack()

#     def connect_to_server(self):
#         server_ip = self.server_ip_entry.get()
#         server_port = int(self.server_port_entry.get())
#         self.socket = socket.socket()
#         try:
#             self.socket.connect((server_ip,server_port))
#             messagebox.showinfo("Connection Successful","Connected to server")
#             #self.view_logs("connected to server")
#         except:
#             messagebox.showerror("Connection Error","Could not connect to server")

#     def browse_file_or_directory(self):
#         file_or_directory = filedialog.askopenfilename()
#         self.share_entry.delete(0,tk.END)
#         self.share_entry.insert(0, file_or_directory)

#     def share_file_or_directory(self):
#         file_or_directory = self.share_entry.get()
#         if os.path.isfile(file_or_directory):
#             self.share_file(file_or_directory)
#         elif os.path.isdir(file_or_directory):
#             self.share_directory(file_or_directory)

#     def share_file(self,filename):
#         #filename = os.path.basename(file_path)
#         self.socket.send(("SHARE:" + os.path.basename(filename)).encode())
#         # with open(file_path,"rb") as f:
#         #     data = f.read(1024)
#         #     while data:
#         #         self.socket.send(data)
#         #         data = f.read(1024)

#         self.file_list.append(filename)
#         self.update_file_listbox()

#     def share_directory(self, dir_path):
#         for root, dirs, files in os.walk(dir_path):
#             for filename in files:
#                 self.share_file(os.path.join(root,filename))

#     def search_for_file(self):
#         query = self.search_entry.get()
#         if not query:
#             return 
#         self.socket.send(("SEARCH:" + query).encode())
#         data = self.socket.recv(1024).decode()
#         if data.startswith("SEARCHRESULT"):
#             results = data.split(":")[1].split(",")
#             if results[0] == "No results found":
#                 self.search_results_listbox.delete(0,tk.END)
#                 messagebox.showinfo("Search Results","No results found")
#             else:
#                 self.search_results = results.self.update_search_results_listbox()

#     def update_search_results_listbox(self):
#         self.search_results_listbox.delete(0,tk.END)
#         for result in self.search_results:
#             filename, ip_address = result.split(":")
#             self.search_results_listbox.insert(tk.END,filename + "(shared by " + ip_address +")")

#     def download_file(self,event):
#         selection = self.search_results_listbox.curselection()
#         if not selection:
#             return
#         index = selection[0]
#         result = self.search_results[index]
#         filename, ip_address = result.split(":")
#         response = messagebox.askyesno("Download File", "Do you want to download " + filename + "?")
#         if response == tk.NO:
#             return 
#         with socket.socket() as s:
#             s.connect((ip_address,8000))
#             s.send(("DOWNLOAD:" + filename + ":" + self.socket.getsockname()[0] + ":8000").encode())
#             data = s.recv(1024)
#             with open(filename,"wb") as f:
#                 while data:
#                     f.write(data)
#                     data = s.recv(1024)
#                 if os.path.isfile(filename):
#                     messagebox.showinfo("Download Complete","File downloaded successfully")
#                 else:
#                     messagebox.showerror("Download Failure","An error occured while downloading the file")

#     def update_file_listbox(self):
#         self.file_listbox.delete(0,tk.END)
#         for filename in self.file_list:
#             self.file_listbox.insert(tk.END,filename)

#     def view_logs(self):
#         with open("client.log","r") as f:
#             log_contents = f.read()
#         messagebox.showinfo("Client Logs", log_contents)

#     def start(self):
#         self.root.mainloop()

# if __name__ == "__main__":
#     client_gui = ClientGUI()
#     client_gui.start()
            
