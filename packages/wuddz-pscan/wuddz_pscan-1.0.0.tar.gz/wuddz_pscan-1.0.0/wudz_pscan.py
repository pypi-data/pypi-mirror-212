import argparse, sys, asyncio
from os import path, system
from socket import *
from ipaddress import (IPv4Network, IPv4Address)
system('')

class PortScanner:
    """Asynchronously Scan Specified Host(s)/Network(s)/IPRange(s) For Specified Open Tcp Ports."""
    def __init__(self, args):
        self.out = ''
        self.vc = 0
        self.hl = args.host
        self.pl = self.scan_ports(args.port)
        self.tc = args.tasks
        self.to = args.timeout
        if args.output:self.out = args.output
    
    def scan_ports(self, ports):
        """Return Specified Port(s) As List."""
        plst = [ports]
        if '-' in ports:
            pl = ports.split('-')
            plst = [p for p in range(int(pl[0]), int(pl[1])+1) if int(p) <= 65535]
        elif ',' in ports:plst = [p for p in ports.split(',') if int(p) <= 65535]
        return plst
    
    def scan_hosts(self, hosts):
        """Yield All Specified Host & Port Combinations As Generator Objects."""
        hl = [hosts]
        if path.isfile(hosts):hl = self.get_list(hosts)
        for h in hl:
            if '/' in str(h):
                for i in IPv4Network(str(h)):
                    for p in self.pl:
                        yield str(i), int(p)
            elif '-' in str(h):
                r = h.split('-') 
                for i in range(int(IPv4Address(r[0])), int(IPv4Address(r[1]))+1):
                    for p in self.pl:
                        yield str(IPv4Address(i)), int(p)
            elif ',' in str(h):
                for i in str(h).split(','):
                    for p in self.pl:
                        yield str(IPv4Address(i)), int(p)
            else:
                for p in self.pl:
                    yield str(IPv4Address(h)), int(p)
    
    def get_list(self, option):
        """Return Argument Or File Contents As List."""
        data = [option]
        if path.isfile(str(option)):
            with open(str(option), 'r', encoding='utf-8') as fr:
                data = [x for x in set(fr.read().splitlines())]
        return data
    
    async def port_scan(self, ip, port):
        """Execute TCP Connection With Ip & Port, Output To
           File Or Print To Screen & Close Connection."""
        try:
            r,w = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=self.to)
            self.vc += 1
            if self.out:
                with open(self.out, 'a', encoding='utf-8') as fw:
                    fw.write(f'{ip}:{port}\n')
            else:print(f'\033[1;32;40m[+] {ip}:{port}  Open\033[0m')
            w.close()
        except:pass
    
    async def main(self):
        """Iterate Each Host & Port Combination From Generator, Execute Asynchronous
           TCP Connections Limited To The Amount Of Threads Specified And Print Results
           To Screen Or Save To Output Text File."""
        tasks = set()
        print("\033[1;37;40m[-] Scanning Host(s)...\033[0m")
        for i, p in self.scan_hosts(self.hl):
            if len(tasks) >= self.tc:
                _done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            tasks.add(asyncio.create_task(self.port_scan(i, p)))
        await asyncio.wait(tasks)
        print("\033[1;33;40m[*] Found {} Host:Port\033[0m".format(str(self.vc)))

def cli_main():
    usage = ('Examples:\n'
             '    wudz-pscan -i 1.1.1.1 -p 80,443 -o output.txt -t 200 -m 1\n'
             '    wudz-pscan -i 1.1.1.1,2.2.2.2  ("Scans All 65535 Ports As Default")\n'
             '    wudz-pscan -i hosts.txt -p 80-445')
    parser = argparse.ArgumentParser(description="Scan Host(s)/Network(s)/IPRange(s) For Open Tcp Ports.",
                                     epilog=usage,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--host', type=str, required=True, help="Host Or File With Host On Each Line,\n"
                        "(formats -> 1.1.1.1 | 1.1.1.0/24 | 1.1.1.1-1.1.2.2 | 2.2.2.2,1.1.1.1).")
    parser.add_argument('-p', '--port', type=str, default="0-65535", help="Scan For Open Port(s),\n"
                        "(formats -> 80 | 1-443 | 25,80,445).")
    parser.add_argument('-o', '--output', type=str, default=None, help="Output File To Save Results.")
    parser.add_argument('-t', '--tasks', type=int, default=128, help="Amount Of Tasks To Run Asynchronously.")
    parser.add_argument('-m', '--timeout', type=float, default=0.5, help="Timeout(Float Value) "
                        "For Each Connection,\n(Default = 0.5: Lower Is Faster, Higher Is Slower Scan).")
    if len(sys.argv) == 1:parser.print_help()
    else:
        try:
            portscan = PortScanner(parser.parse_args())
            asyncio.run(portscan.main())
        except:sys.exit()
