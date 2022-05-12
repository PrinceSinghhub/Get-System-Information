import psutil
import platform
import GPUtil
from datetime import datetime
from tkinter import *
import webbrowser

root = Tk()
root.title('System and Hardware Information')
root.geometry("1366x770")
# root.resizable(False, False)
root.config(bg='#00154f')

Label(root, text='System and Hardware Information', font='Verdana 20 bold', fg='#f2bc94', bg="#00154f").pack()
Label(root, text='CODEX CODER', font='Verdana 13 bold', fg='#f4af1b', bg="#00154f").pack()
TextBox = Text(root, height=25, width=110, font='Verdana 10 bold')
TextBox.place(x = 180, y= 200)


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def SystemInfo():
    TextBox.delete('1.0', END)
    r="_____System Information By Codex Coder_____"
    TextBox.insert(END,r.center(200))
    TextBox.insert(END,"\n\n\n")
    uname = platform.uname()
    x1=f"System: {uname.system}"
    x2=f"Node Name: {uname.node}"
    x3= f"Release: {uname.release}"
    x4= f"Version: {uname.version}"
    x5=f"Machine: {uname.machine}"
    x6= f"Processor: {uname.processor}"
    TextBox.insert(END, f"{x2.center(220)}\n")
    TextBox.insert(END,f"{x1.center(225)}\n")
    TextBox.insert(END,f"{x3.center(230)}\n")
    TextBox.insert(END,f"{x4.center(225)}\n")
    TextBox.insert(END,f"{x5.center(225)}\n")
    TextBox.insert(END,"\n")
    TextBox.insert(END,f"{x6.center(200)}\n")

# Boot Time
def boottime():
    TextBox.delete('1.0', END)
    r = "_____Boot Time Information By Codex Coder_____"
    TextBox.insert(END, r.center(200))
    TextBox.insert(END, "\n\n\n")
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    TextBox.insert(END, f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

# let's print CPU information
def CPUInfo():
    TextBox.delete('1.0', END)
    r="_____CPU Information By Codex Coder_____"
    TextBox.insert(END,r.center(200))
    TextBox.insert(END,"\n\n\n")
    # number of cores
    TextBox.insert(END, f"Physical cores: {psutil.cpu_count(logical=False)}\n")
    TextBox.insert(END, f"Total cores: {psutil.cpu_count(logical=True)}\n")
    # CPU frequencies
    cpufreq = psutil.cpu_freq()
    TextBox.insert(END, f"Max Frequency: {cpufreq.max:.2f}Mhz \n")
    TextBox.insert(END, f"Min Frequency: {cpufreq.min:.2f}Mhz \n")
    TextBox.insert(END, f"Current Frequency: {cpufreq.current:.2f}Mhz \n")
    # CPU usage
    TextBox.insert(END, "CPU Usage Per Core: \n")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        TextBox.insert(END, f"Core {i}: {percentage}% \n")
    TextBox.insert(END, f"Total CPU Usage: {psutil.cpu_percent()}% \n\n")

    TextBox.insert(END, "_ BATTERY INFO _ \n")
    info = list(psutil.sensors_battery())
    TextBox.insert(END, f" Percentage: {info[0]}\n")
    TextBox.insert(END, f" Plugged-in: {info[2]}")

# Memory Information
def MemoryInfo():
    TextBox.delete('1.0', END)
    r = "_____Memory Information By Codex Coder_____"
    TextBox.insert(END, r.center(200))
    TextBox.insert(END, "\n\n\n")
    # get the memory details
    svmem = psutil.virtual_memory()
    TextBox.insert(END, f"Total: {get_size(svmem.total)} \n")
    TextBox.insert(END, f"Available: {get_size(svmem.available)} \n")
    TextBox.insert(END, f"Used: {get_size(svmem.used)} \n")
    TextBox.insert(END, f"Percentage: {svmem.percent}% \n")

    # get the swap memory details (if exists)
    TextBox.insert(END, "_____SWAP MEMORY DETAILS (if exist)____\n\n")
    swap = psutil.swap_memory()
    TextBox.insert(END, f"Total: {get_size(swap.total)} \n")
    TextBox.insert(END, f"Free: {get_size(swap.free)} \n")
    TextBox.insert(END, f"Used: {get_size(swap.used)} \n")
    TextBox.insert(END, f"Percentage: {swap.percent}% ")

# Disk Information
def DiskInfo():
    TextBox.delete('1.0', END)
    r = "_____Disk Information By Codex Coder_____"
    TextBox.insert(END, r.center(200))
    TextBox.insert(END, "\n\n\n")
    r1="Partitions and Usage"
    TextBox.insert(END, r1.center(230))
    TextBox.insert(END, "\n\n")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        TextBox.insert(END, f"=== Device: {partition.device} === \n")
        TextBox.insert(END, f"  Mountpoint: {partition.mountpoint} \n")
        TextBox.insert(END, f"  File system type: {partition.fstype} \n")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        TextBox.insert(END, f"  Total Size: {get_size(partition_usage.total)} \n")
        TextBox.insert(END, f"  Used: {get_size(partition_usage.used)} \n")
        TextBox.insert(END, f"  Free: {get_size(partition_usage.free)} \n")
        TextBox.insert(END, f"  Percentage: {partition_usage.percent}% \n\n")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    TextBox.insert(END, f"Total read: {get_size(disk_io.read_bytes)} \n")
    TextBox.insert(END, f"Total write: {get_size(disk_io.write_bytes)} ")

# Network information
def NetworkInfo():
    TextBox.delete('1.0', END)
    r = "_____Network Information By Codex Coder_____"
    TextBox.insert(END, r.center(200))
    TextBox.insert(END, "\n\n\n")
    # get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            TextBox.insert(END, f"=== Interface: {interface_name} === \n")
            if str(address.family) == 'AddressFamily.AF_INET':
                TextBox.insert(END, f"  IP Address: {address.address} \n")
                TextBox.insert(END, f"  Netmask: {address.netmask} \n")
                TextBox.insert(END, f"  Broadcast IP: {address.broadcast} \n")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                TextBox.insert(END, f"  MAC Address: {address.address} \n")
                TextBox.insert(END, f"  Netmask: {address.netmask} \n")
                TextBox.insert(END, f"  Broadcast MAC: {address.broadcast} \n")
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    TextBox.insert(END, f"Total Bytes Sent: {get_size(net_io.bytes_sent)} \n")
    TextBox.insert(END, f"Total Bytes Received: {get_size(net_io.bytes_recv)} \n")

# GPU information
def GPUInfo():
    TextBox.delete('1.0', END)
    r = "_____GPU Information By Codex Coder_____"
    TextBox.insert(END, r.center(200))
    TextBox.insert(END, "\n\n\n")
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        # get the GPU id
        TextBox.insert(END, f" GPU ID : {gpu.id} \n",textalign="CENTRE")
        # name of GPU
        TextBox.insert(END, f"GPU NAME :  {gpu.name} \n")
        # get % percentage of GPU usage of that GPU
        TextBox.insert(END, f"Load : {gpu.load*100}% \n")
        # get free memory in MB format
        TextBox.insert(END, f"Memory Free : {gpu.memoryFree}MB \n")
        # get used memory
        TextBox.insert(END, f"Memory Used : {gpu.memoryUsed}MB \n")
        # get total memory
        TextBox.insert(END, f"Memory Total : {gpu.memoryTotal}MB \n")
        # get GPU temperature in Celsius
        TextBox.insert(END, f"Temperature : {gpu.temperature} °C \n")
        TextBox.insert(END, f"vvid : {gpu.uuid}")

# def Followme():
#    webbrowser.open('https://www.instagram.com/_python.py_/')
Button(root, text='System Information', bg='#f2bc94', fg='#00154f', font='Verdana 10 bold', command=SystemInfo).place(x=100, y=130)
Button(root, text='Boot Time', bg='#f2bc94', fg='#00154f', font='Verdana 10 bold', command=boottime).place(x=275, y=130)
Button(root, text='CPU Information', bg='#f2bc94', fg='#00154f', font='Verdana 10 bold', command= CPUInfo).place(x=380, y=130)
Button(root, text='Memory Information', bg='#f2bc94', fg='#00154f', font='Verdana 10 bold', command=MemoryInfo).place(x=525, y=130)
Button(root, text='Disk Information', bg='#f2bc94', fg='#00154f', font='Verdana 10 bold', command=DiskInfo).place(x=700, y=130)
Button(root, text='Network Information', bg='#f2bc94', fg='#00154f', font='Verdana 10 bold', command = NetworkInfo).place(x=845, y=130)
Button(root, text='Graphic Information', bg='#f2bc94', fg='#00154f', font='Verdana 10 bold', command=GPUInfo).place(x=1020, y=130)
# Button(root, text='Follow', bg='#f2bc94', fg='#00154f', font='Verdana 10 bold', width=10, command=Followme).place(x=20, y=280)
Button(root, text='Exit', bg='#f2bc94', fg='#00154f', font='Verdana 10 bold', command=exit).place(x=1195, y=130)


root.mainloop()