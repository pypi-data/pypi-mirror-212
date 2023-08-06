# HAICU Control Script (haicu-ctl)

## Overview

Package and command line utility for controlling and sequencing the MLD1200

## Installation

The recommended installation method is via pip

  To install/upgrade:
    `pip install -U haicu`

  To run it locally from the source (from the `scripts/haicu` directory):
    `python -m haicu`

## Usage

Command:
`haicu-ctl [-h] [--version] [-v] [-l file] [-s SERIAL] [-j] {list,info,set,upload,program,convert,compare}`

Purpose:
Connects to an MLD1200 device and reads/writes registers, statuses, and memory. Also contains utility functions to create .RLE files for consumption by device.

Options:

`-h` or `--help`
Print out help for general usage or subcommand. Ie: `haicu-ctl -h` or `haicu-ctl set -h`

`--version`
Print out current version

`-v` or `--verbose`
  Increase logging level, can be used multiple times

`-l LOG_FILE` or `--log LOG_FILE`
  Specify log file name, instead of standard naming scheme

`-s SERIAL` or `--serial SERIAL`
  Specify serial number of MLD1200 to connect to

`-j` or `--json`
  For reads, format output in JSON. Only affects `set` (with no value), `info`, `status`, `control`, `memory`, and `bread`

The available subcommands are:

- `list` - List of available MLD1200 devices
- `info` - Get full report on MLD1200, all registers and status bits
- `set <regname> [data]` - Allows human-readable setting of register values. If data is omitted, returns current value in register
- `upload <file> <section>` - Upload a new sequence into MLD1200 from file. Choose section to load ('left','right','extension'). Does not start sequence.
- `program [config_file] [--auto/-a]` - Upload and start sequence. Can be passed a path to an INI file, otherwise tries to use 'haicu.ini' in current directory. The '--auto' option auto-reload the sequencer when it finishes, it will then start again on next trigger.
- `convert <infile> <outfile>` - Convert a derived format file 'infile' into RLE formatted file 'outfile'
- `compare <derived_file> <rle_file>` - Compare a derived file to an RLE file

Diagnostic subcommands:
- `memtest` - Test the selected MLD by writing and reading random values to DDR memory
- `status <addr>` - Low level readback of status register at given address
- `control <addr> [data]` - Low level read/write of control registers. Omit 'data' to return current value at given address
- `memory <addr> [data]` - Low level read/write of DDR memory. Omit 'data' to return current value at given address
- `bread <addr> <count>` - Low level block read of DDR memory section. Reads 'count' words out of DDR started at given address