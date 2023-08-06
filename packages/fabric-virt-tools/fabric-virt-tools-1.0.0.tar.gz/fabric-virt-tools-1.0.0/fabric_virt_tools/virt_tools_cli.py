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
#
import json
import traceback
from typing import List, Dict

import click

from fabric_virt_tools.cpu_tune import CpuTune
from fabric_virt_tools.numa_tune import NumaTune


@click.group()
@click.option('-v', '--verbose', is_flag=True)
@click.pass_context
def virt_tools_cli(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj['VERBOSE'] = verbose


@click.group()
@click.pass_context
def cpu(ctx):
    """ CPU Pinning
    """


@cpu.command()
@click.option('--domain_name', help='Virtual Guest Domain Name', required=True)
@click.pass_context
def info(ctx, domain_name: str):
    """ Query CPU Info for VM Guest and relevant host information as well
    """
    try:
        cpu_tune = CpuTune()
        cpu_info = cpu_tune.info(domain_name=domain_name)
        print(json.dumps(cpu_info))
    except Exception as e:
        traceback.print_exc()
        raise click.ClickException(f"virt_tools_cli: {e}")


@cpu.command()
@click.option('--domain_name', help='Virtual Guest Domain Name', required=True)
@click.option('--vcpu', help='Virtual CPU', required=True)
@click.option('--cpu', help='Physical CPU', required=True)
@click.pass_context
def pin(ctx, domain_name: str, vcpu: str, cpu: str):
    """ Pin vCPU to Host CPU
    """
    try:
        cpu_tune = CpuTune()
        cpu_tune.vcpu_pin(domain_name=domain_name, vcpu=vcpu, cpu=cpu)
        print(f"CPU pinning for {domain_name} for VCPU: {vcpu} to CPU {cpu} done!")
    except Exception as e:
        traceback.print_exc()
        raise click.ClickException(f"virt_tools_cli: {e}")


@click.group()
@click.pass_context
def numa(ctx):
    """ Numa Tuning
    """


@numa.command()
@click.option('--domain_name', help='Virtual Guest Domain Name', required=True)
@click.pass_context
def info(ctx, domain_name: str):
    """ Query Numa Info for VM Guest and relevant host information as well
    """
    try:
        numa_tune = NumaTune()
        numa_info = numa_tune.info(domain_name=domain_name)
        print(json.dumps(numa_info))
    except Exception as e:
        traceback.print_exc()
        raise click.ClickException(f"virt_tools_cli: {e}")


@numa.command()
@click.option('--domain_name', help='Virtual Guest Domain Name', required=True)
@click.option('--node_set', help='List of the nodes to be assigned', required=True, multiple=True)
@click.pass_context
def tune(ctx, domain_name: str, node_set: List[str]):
    """ Pin Numa Node to the VM Guest
    """
    try:
        numa_tune = NumaTune()
        numa_tune.numa_tune(domain_name=domain_name, node_set=node_set)
        print(f"Numa tuning for {domain_name} to {node_set} done!")
    except Exception as e:
        traceback.print_exc()
        raise click.ClickException(f"virt_tools_cli: {e}")


virt_tools_cli.add_command(cpu)
virt_tools_cli.add_command(numa)
