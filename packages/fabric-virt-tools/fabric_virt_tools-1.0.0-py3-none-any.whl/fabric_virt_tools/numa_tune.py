#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Komal Thareja (kthare10@renci.org)
import re
from typing import List, Dict, Any

import libvirt

from fabric_virt_tools.utils import Utils


class NumaTune:
    def __init__(self):
        self.connection = libvirt.open(None)

    @staticmethod
    def parse_numastat(*, numastat_output: List[str]) -> Dict[Any, dict]:
        """
        Parse numa stat output and convert it to JSON
        @param numastat_output: Numa State output
        """
        '''
        Numa Stat Output looks like:
        numa_info = ["",
                 "Per-node process memory usage (in MBs) for PID 2676600 (qemu-kvm)",
                 "         Node 0 Node 1 Total",
                 "         ------ ------ -----",
                 "Private   17531  15284 32815",
                 "Heap          0      6     6",
                 "Stack         0      0     0",
                 "Huge          0      0     0",
                 "-------  ------ ------ -----",
                 "Total     17531  15290 32821"
                 ]
        '''
        result = {}
        keys = []
        for line in numastat_output:
            # Ignore empty lines and headers
            if line == "" or "Per-node" in line or "--" in line:
                continue
            # Extract Numa Nodes
            elif "Node" in line:
                line = line.strip()
                regex_pattern = r'\b(\w+\s+\d+)\b|\b(\w+)\b'
                matches = re.findall(regex_pattern, line)
                # Flatten the list of tuples and remove empty strings
                keys = [match[0] or match[1] for match in matches if match[0] or match[1]]

                # Add empty dictionary for each Node and Total
                for x in keys:
                    result[x] = {}
            else:
                # Extract Different types of Memory for each Node and Total
                regex_pattern = r'(\b\w+\b)|(\b\d+\b)'
                matches = re.findall(regex_pattern, line)
                # Flatten the list of tuples and remove empty strings
                memory_values = [match[0] or match[1] for match in matches if match[0] or match[1]]
                # Index 0 contains the type of Memory and is used as a key
                idx = 1
                for x in keys:
                    result[x][memory_values[0]] = memory_values[idx]
                    idx += 1

        return result

    @staticmethod
    def parse_numactl(*, numactl_output: List[str]) -> Dict[Any, dict]:
        """
        Parse numa stat output and convert it to JSON
        @param numastat_output: Numa State output
        """
        '''
        Numa Stat Output looks like:
        numa_info = [
                     'available: 8 nodes (0-7)', 
                     'node 0 cpus: 0 1 2 3 4 5 6 7 64 65 66 67 68 69 70 71', 
                     'node 0 size: 63798 MB', 
                     'node 0 free: 59660 MB', 
                     'node 1 cpus: 8 9 10 11 12 13 14 15 72 73 74 75 76 77 78 79', 
                     'node 1 size: 64507 MB', 
                     'node 1 free: 63042 MB', 
                     'node 2 cpus: 16 17 18 19 20 21 22 23 80 81 82 83 84 85 86 87', 
                     'node 2 size: 64507 MB', 
                     'node 2 free: 63911 MB', 
                     'node 3 cpus: 24 25 26 27 28 29 30 31 88 89 90 91 92 93 94 95', 
                     'node 3 size: 64458 MB', 
                     'node 3 free: 30882 MB', 
                     'node 4 cpus: 32 33 34 35 36 37 38 39 96 97 98 99 100 101 102 103', 
                     'node 4 size: 64507 MB', 
                     'node 4 free: 64069 MB', 
                     'node 5 cpus: 40 41 42 43 44 45 46 47 104 105 106 107 108 109 110 111', 
                     'node 5 size: 64507 MB', 
                     'node 5 free: 63966 MB', 
                     'node 6 cpus: 48 49 50 51 52 53 54 55 112 113 114 115 116 117 118 119', 
                     'node 6 size: 64507 MB', 
                     'node 6 free: 61214 MB', 
                     'node 7 cpus: 56 57 58 59 60 61 62 63 120 121 122 123 124 125 126 127', 
                     'node 7 size: 64506 MB', 
                     'node 7 free: 63869 MB', 
                     'node distances:', 
                     'node   0   1   2   3   4   5   6   7 ', 
                     '  0:  10  12  12  12  32  32  32  32 ', 
                     '  1:  12  10  12  12  32  32  32  32 ', 
                     '  2:  12  12  10  12  32  32  32  32 ', 
                     '  3:  12  12  12  10  32  32  32  32 ', 
                     '  4:  32  32  32  32  10  12  12  12 ', 
                     '  5:  32  32  32  32  12  10  12  12 ', 
                     '  6:  32  32  32  32  12  12  10  12 ', 
                     '  7:  32  32  32  32  12  12  12  10 '
                     ]
        '''
        result = {}
        for line in numactl_output:
            # Ignore empty lines and headers
            if line == "":
                continue
            elif "available" in line:
                key, value = line.split(':')
                key = key.strip()
                value = value.strip()
                result[key] = value
            elif "node distances" in line:
                break
            else:
                key, value = line.split(':')
                key = key.strip()
                value = value.strip()
                regex_pattern = r"^(.*?)\s+(\w+)$"
                matches = re.match(regex_pattern, key)
                if matches:
                    node = matches.group(1)
                    key = matches.group(2)
                    if node not in result:
                        result[node] = {}
                    result[node][key] = value
                else:
                    result[key] = value
        return result

    def __get_host_numa_info(self):
        """
        Get Host Numa Information
        :return: JSON containing NUMA information from Host
        """
        host_info_output = Utils.execute_command(command=["numactl", "-H"]).splitlines()
        return self.parse_numactl(numactl_output=host_info_output)

    def __get_guest_numa_info(self, *, domain_name: str):
        """
        Get VM Guest Numa Information
        :param domain_name: domain name for VM Guest
        :return: JSON containing NUMA information for the VM Guest
        """
        guest_info_output = Utils.execute_command(command=["numastat", "-c", "-s", domain_name]).splitlines()
        return self.parse_numastat(numastat_output=guest_info_output)

    def info(self, *, domain_name: str):
        """
        Return NUMA information for the VM guest identified by domain_name and relevant information from Host
        :param domain_name: domain name for VM Guest
        :return: SON containing NUMA information for the VM Guest and Host
        """
        host_name = self.connection.getHostname()
        result = {host_name: self.__get_host_numa_info(),
                  domain_name: self.__get_guest_numa_info(domain_name=domain_name)}
        return result

    @staticmethod
    def __extract_node_set(*, node_set: str) -> List[str]:
        """
        Extract Node Numbers from the Node Set parameter of the VM Guest
        :param node_set: Node Set parameter of the VM Guest
        :return: Node Numbers
        """
        result = []
        ranges = node_set.split(',')
        for item in ranges:
            item = item.strip()
            if item == "":
                continue
            if '-' in item:
                start, end = item.split('-')
                result.extend([str(i) for i in range(int(start), int(end) + 1)])
            else:
                result.append(item)
        return result

    def __get_allocated_memory(self, *, requested_node_set: List[str], exclude_domains: List[str] = None) -> int:
        """
        Get Already allocated memory to the VMs which have been pinned to the requested nodes
        :param requested_node_set: Requested Node Set
        :param exclude_domains: List of domain names to exclude
        :return:
        """
        result = 0
        # Traverse through all the running VMs
        for domain_id in self.connection.listDomainsID():
            domain = self.connection.lookupByID(domain_id)

            # Exclude any domains in the exclude list
            if exclude_domains is not None and domain.name() in exclude_domains:
                continue

            # Determine the Numa Node Set assigned to the domain
            domain_numa_nodeset = self.__extract_node_set(node_set=domain.numaParameters().get('numa_nodeset'))

            # Find common elements between assigned and requested node set
            common_elements = list(set(domain_numa_nodeset).intersection(requested_node_set))
            if len(common_elements) > 0:
                # Get Guest Numa Infor
                domain_numa_info = self.__get_guest_numa_info(domain_name=domain.name())

                # Determine the allocated memory on the requested Numa Node
                for n in common_elements:
                    node_numa_allocated = domain_numa_info.get(f"Node {n}").get("Total")
                    result += int(node_numa_allocated)

        return result

    def numa_tune(self, *, domain_name: str, node_set: List[str]):
        """
        Tune Numa for VM guest to the requested nodes
        :param domain_name: Domain name for the VM
        :param node_set: Requested Node Set
        :return:
        """
        try:
            domain = self.connection.lookupByName(domain_name)
            # Unit is Bytes
            requested_memory = domain.maxMemory()
            # Convert to MB
            requested_memory /= 1024

            # Get Allocated memory already in use for the requested node set
            allocated_memory = self.__get_allocated_memory(requested_node_set=node_set, exclude_domains=[domain_name])

            # Get Host Numa Info
            host_numa = self.__get_host_numa_info()

            # Determine Total Memory for the Requested Numa Nodes
            total_memory = 0
            for node in node_set:
                node_info = host_numa.get(f"node {node}")
                total_memory_str = node_info.get("size").replace(" MB", "")
                total_memory += int(total_memory_str)

            # Verify requested memory can still be accommodated by requested Numa Nodes
            if requested_memory <= (total_memory - allocated_memory):
                Utils.execute_command(["virsh", "numatune", domain_name, "--nodeset", ','.join(node_set),
                                      "--live", "--config"])
            else:
                raise Exception(f"NUMA_TUNE_ERROR - Not enough memory available for {domain_name} on Numa Node: {node_set}")
        except libvirt.libvirtError as e:
            raise Exception(f"NUMA_TUNE_ERROR for {domain_name} e: {e}")


if __name__ == '__main__':
    numa_tune = NumaTune()
    print(numa_tune.info(domain_name='instance-0000106b'))
    numa_tune.numa_tune(domain_name='instance-0000106b', node_set=["5", "6"])

