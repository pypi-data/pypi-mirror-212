# virt-tools
Libvirt based tools to tune VMs on the worker nodes. It provides CLI interface as well as Python APIs.

## CLI
`virt-tools` supports the CLI: `fabric-virt-tools-cli`
```
Usage: fabric-virt-tools-cli [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --verbose
  --help         Show this message and exit.

Commands:
  cpu   CPU Pinning
  numa  Numa Tuning
```
### CPU Pinning and Information
`fabric-virt-tools-cli` supports CPU pinning and information commands as depicted below:
```
Usage: fabric-virt-tools-cli cpu [OPTIONS] COMMAND [ARGS]...

  CPU Pinning

Options:
  --help  Show this message and exit.

Commands:
  info  Query CPU Info for VM Guest and relevant host information as well
  pin   Pin vCPU to Host CPU
```
### Numa Pinning and Information
`fabric-virt-tools-cli` supports Numa pinning and information commands as depicted below:
```
Usage: fabric-virt-tools-cli numa [OPTIONS] COMMAND [ARGS]...

  Numa Tuning

Options:
  --help  Show this message and exit.

Commands:
  info  Query Numa Info for VM Guest and relevant host information as well
  tune  Pin Numa Node to the VM Guest
```

## Installation
This tool should be installed on the Worker nodes on each site. This CLI is used by the AMHandlers to pin CPU/Numa to the VM instances.

```
$ p3.6 install fabric-virt-tools
```

NOTE: This package depends on `libvirt-python`. `libvirt` running on the currently uses `python3.6` hence `pip3.6` install is recommended. This can be changed if the underlying platform i.e. `libvirt` uses a later version of `python`.

### Pre-requisites
Ensure that following are installed
```
virtualenv
virtualenvwrapper
```
NOTE: Any of the virtual environment tools (`venv`, `virtualenv`, or `virtualenvwrapper`) should work.
