#!/usr/bin/env python

import argparse, sys, pysosutils, opsys, bios, memory, ps, virt, kernel, network, lspci, filesys

parser = argparse.ArgumentParser(description="Pysos is used to quickly parse and display information from a sosreport in a meaningful and human-readable manner")
parser.add_argument('target', nargs='+', help="Target directory, aka the sosreport root.")
parser.add_argument('-a', "--getall", action="store_true", help="Print all information (RHEV excluded)")
parser.add_argument('-b', "--bios", action="store_true", help="Print BIOS and dmidecode information")
parser.add_argument('-o', "--os", action="store_true", help="Print OS information")
parser.add_argument('-k', "--kdump", "--kernel", action="store_true", help="Print kdump and kernel information")
parser.add_argument('-c', "--cpu", action="store_true", help="Print CPU information ONLY")
parser.add_argument('-m', "--memory", action="store_true", help="Print memory information")
#parser.add_argument('-d', "--disk", action="store_true", help='Print /proc/partition information')
parser.add_argument('-f', "--filesys", action="store_true", help="Print filesystem information")
parser.add_argument('-l', "--lspci", action="store_true", help="Print lspci information")
parser.add_argument('-e', '--ethtool', action="store_true", help="Print ethtool information")
parser.add_argument('-g', "--bonding", action="store_true", help="Print bonding information")
parser.add_argument('-i', "--ip", action="store_true", help="Print IP information")
parser.add_argument('-n', "--netdev", action="store_true", help='Print proc/net/dev information')
parser.add_argument("--net", action="store_true", help="Alias for --ethtool, --bonding, --ip, --netdev")
parser.add_argument('-s', "--sysctl", action="store_true", help="Print common sysctl settings")
parser.add_argument('-p', "--ps", action="store_true", help="Print process information")
#parser.add_argument("--check", help='Check package for known bugs')
parser.add_argument('-r', "--rhev", action="store_true", help="Print RHEV information")
parser.add_argument("--db", action="store_true", help = "Print RHEV DB information")
parser.add_argument('-v', "--virt", action="store_true", help="Print KVM Virtualization information") 
#parser.add_argument('-y', "--yum", action="store_true", help='Print yum/RHN information')


def doStuff(**args):
    if args['getall']:
        args['os'] = True
        args['memory'] = True
        args['kdump'] = True
        args['cpu'] = True
        args['filesys'] = True
        args['sysctl'] = True
        args['ps'] = True
        args['ip'] = True
        args['bonding'] = True
        args['netdev']= True
        args['ethtool'] = True
        args['bios'] = True
        args['disk'] = True
        args['lspci'] = True
    if args['net']:
        args['ip'] = True
        args['bonding'] = True
        args['ethtool'] = True
        args['netdev'] = True
    if args['os']:
        obj = opsys.opsys(target)
        obj.displayOpSys()
        if args['cpu']:
            obj.displayCpuInfo()
            args['cpu'] = False
    if args['memory']:
        obj = memory.memory(target)
        obj.displayMemInfo()
    if  args['bios']:
        obj = bios.bios(target)
        obj.displayBiosInfo()
    if  args['kdump']:
        obj = kernel.kernel(target)
        obj.displayKernelInfo()
    if  args['cpu']:
        obj = opsys.opsys(target)
        obj.displayCpuInfo()
    if args['filesys']:
        obj = filesys.filesys(target)
        obj.displayFsInfo()
    #if  args['sysctl']:
    #    get_sysctl_info(target)
    if  args['ip']:
        obj = network.network(target)
        obj.displayIpInfo()
    if  args['bonding']:
        obj = network.network(target)
        obj.displayBondInfo()
    if  args['ethtool']:
        obj = network.network(target)
        obj.displayEthtoolInfo()
    if  args['netdev']:
        obj = network.network(target)
        obj.displayNetDevInfo()
    if  args['lspci']:
        obj = lspci.lspci(target)
        obj.displayAllLspciInfo()
    if args['rhev'] or args['virt']:
        obj = virt.virt(target)
        if args['db']:
            obj.showVirtPlat(target, db=True)
        else:
            obj.showVirtPlat(target)
    #if  args['disk']:
    #    get_storage_info(target, local)
    if  args['ps']:
        obj = ps.procInfo(target)
        obj.displayPsInfo()
    #if  args['check']:
    #    check_installed(target, args['check'], local)
    #if args['yum']:
    #    get_yum_info(target, local)



if __name__ == '__main__':
    args = parser.parse_args()
    target = args.target[0]
    if not target.endswith('/'):
        target = target + '/'	

    doStuff(**vars(args))



