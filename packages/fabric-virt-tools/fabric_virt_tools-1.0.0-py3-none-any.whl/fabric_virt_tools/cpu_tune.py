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
import json
import subprocess
from typing import List, Dict

import libvirt

from fabric_virt_tools.utils import Utils


class CpuTune:
    """
    Supports CPU pinning for VM Guests and retrieving vCpuInfo
    """
    VCPU = "vcpu"
    CPU = "cpu"
    NUMA = "numa"
    FIELD = "field"
    DATA = "data"
    PINNED_CPUS = "pinned_cpus"
    CPU_AFFINITY = "CPU Affinity"

    def __init__(self):
        """
        Constructor
        """
        # Open a connection with libvirt
        self.connection = libvirt.open(None)

    def __get_pinned_cpus(self, *, exclude_domains: List[str] = None) -> List[str]:
        """
        Check all the running VMs and determine the host CPUs which are pinned
        :param exclude_domains: List of domain names to exclude
        :return: list of host CPUs which are pinned
        """
        pinned_cpu_list = []
        # Traverse through currently active VMs
        for domain_id in self.connection.listDomainsID():
            domain = self.connection.lookupByID(domain_id)

            # Exclude the domain if included in exclude list
            if exclude_domains is not None and domain.name() in exclude_domains:
                continue
            pins = domain.vcpuPinInfo()
            for (i, cpu_map) in enumerate(pins):
                # cpu_map is an bitfield (list of bools) with the length of available CPU cores
                # If a CPU is pinned, exactly one value is True, its index is indicating which
                # CPU we are talking about
                if cpu_map.count(True) == 1:
                    cpus = [str(i) for i, x in enumerate(cpu_map) if x]
                    for c in cpus:
                        pinned_cpu_list.append(c)
        return pinned_cpu_list

    def vcpu_pin(self, *, domain_name: str, vcpu: str, cpu: str):
        """
        Pin vCpus of  VM to specific Host Cpus
        :param domain_name: Domain Name for the VM Guest
        :param vcpu_cpu_map: Virtual CPU to Host CPU Map
        :return:
        """
        # Determine already pinned host cpus
        current_pinned_cpus = self.__get_pinned_cpus(exclude_domains=[domain_name])
        # Verify that the requested CPUs are not already pinned
        if cpu in current_pinned_cpus:
            raise Exception(f"CPU_PIN_ERROR: Requested CPU: {cpu} is already pinned to another domain")
        try:
            # Grab the Domain for the VM
            domain = self.connection.lookupByName(domain_name)
            # Determine the current CPU Map
            pins = domain.vcpuPinInfo()

            # Build new CPU Map based on the VCPU to Host CPU map requested for each VCPU
            cpu_map = pins[int(vcpu)]
            cpu_map = tuple([True if j == int(cpu) else False for j in range(len(cpu_map))])
            # Pin vCPU to the requested Host CPU
            domain.pinVcpuFlags(int(vcpu), cpu_map, libvirt.VIR_DOMAIN_AFFECT_CONFIG|libvirt.VIR_DOMAIN_AFFECT_LIVE)
        except libvirt.libvirtError as e:
            raise Exception(f"CPU_PIN_ERROR for {domain_name} e: {e}")

    @staticmethod
    def __get_host_cpu_info():
        """
        Get Host CPU Information using "lscpu -J" command
        :return: JSON object containing CPU and Numa parameters returned by lscpu
        """
        try:
            # Execute the command
            output = Utils.execute_command(["lscpu", "-J"])
            output_json = json.loads(output)["lscpu"]
            # Extract the output
            host = {}
            # Traverse the list
            for x in output_json:
                key = x[CpuTune.FIELD]
                value = x[CpuTune.DATA].replace(":", "")
                # Extract CPU/Numa parameters
                if CpuTune.CPU.upper() in key or CpuTune.NUMA in key:
                    host[key] = value
            return host
        except subprocess.CalledProcessError as e:
            return None

    @staticmethod
    def parse_vcpuinfo(*, vcpu_info_output: List[str]) -> List[Dict[str, str]]:
        """
        Parse vCpu Info and transform it to JSON
        @param vcpu_info_output: vCpu Info command output
        """
        '''
        Vcpuinfo Output looks like:
            cpu_info = ["VCPU:           0",
                "CPU:            27",
                "State:          running",
                "CPU time:       3.1s",
                "CPU Affinity:   yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy", 
                "", 
                "VCPU:           1", 
                "CPU:            9", 
                "State:          running", 
                "CPU Affinity:   yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy"
                ]
        '''
        result = []
        data = {}
        for line in vcpu_info_output:
            line = line.strip()
            if line == "":
                result.append(data.copy())
                data.clear()
            else:
                # Split the line at the first occurrence of ':' character
                key, value = line.split(':', 1)
                # Remove leading/trailing spaces from key and value
                key = key.strip()
                value = value.strip()
                # Add the key-value pair to the data dictionary
                data[key] = value
        return result

    def info(self, *, domain_name: str):
        """
        Determine CPU Info for the VM Guest and the host
        :param domain_name:
        :return:
        """
        # Determine Host Name
        host_name = self.connection.getHostname()
        # Get Host CPU Information
        host_info = self.__get_host_cpu_info()
        # Get Pinned CPUs
        pinned_cpus = self.__get_pinned_cpus(exclude_domains=[domain_name])
        host_info[CpuTune.PINNED_CPUS] = pinned_cpus
        # Get vCPU Information
        vcpu_info_output = Utils.execute_command(command=["virsh", "vcpuinfo", domain_name]).splitlines()
        vcpu_info = self.parse_vcpuinfo(vcpu_info_output=vcpu_info_output)

        try:
            domain = self.connection.lookupByName(domain_name)
            pins = domain.vcpuPinInfo()
            # Update CPU Affinity for each vCPU
            for (i, cpu_map) in enumerate(pins):
                cpus = [str(i) for i, x in enumerate(cpu_map) if x]
                vcpu_info[i][CpuTune.CPU_AFFINITY] = ','.join(cpus)
        except libvirt.libvirtError as e:
            raise Exception(f"CPU_PIN_ERROR for {domain_name} e: {e}")

        # Return Host and Guest vCPU Info
        result = {host_name: host_info,
                  domain_name: vcpu_info}
        return result


if __name__ == '__main__':
    cpu_tune = CpuTune()
    cpu_tune.vcpu_pin(domain_name='instance-0000106b', vcpu="0", cpu="114")

    print(cpu_tune.info(domain_name='instance-0000106b'))
