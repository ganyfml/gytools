import asyncio
import websockets
import socket
import json
import win32serviceutil
import win32service
import win32event
import servicemanager, sys
import time

log_file_path = 'C:/NetorusFiles/PrinterService.log'

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "B2BPrinterService"
    _svc_display_name_ = "B2B Printer Service"

    def print_log(self, log_content):
        with open(log_file_path, 'a+') as log_file:
            log_file.write(log_content)

    async def incoming_print(self, websocket, path):
        print_content_raw = await websocket.recv()
        print_content = json.loads(print_content_raw)
        connection = print_content['connection']
        content = print_content['content']
        self.print_log('接收到打印请求 {}\n'.format(content))
        self.print_log('正在连接打印机： IP：{}，端口：{}\n'.format(connection['ip'], connection['port']))
        res = '打印成功\n'
        try:
            printer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            printer_socket.connect((connection['ip'], connection['port']))
            print('打印机连接成功，发送数据')   
            printer_socket.send(print_content_encode)
            print('发送完成')
            printer_socket.close()
        except:
            print('发送失败')
            res = '打印失败'
        await websocket.send(res)
        self.print_log(res)

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.print_log('Printer Server Init\n')

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.print_log('Printer Server shutdown successfully\n')

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.main()

    def main(self):
        self.print_log('Printer Server start\n')
        start_server = websockets.serve(self.incoming_print, 'localhost', 8765)
        self.server = self.loop.run_until_complete(start_server)
        self.loop.run_forever()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AppServerSvc)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AppServerSvc)
