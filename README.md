# MBR-extractor
A python based tool to extract and parse the MBR (Master Boot Record) data.
## System Supported
..* Windows
..* Linux
..* MacOS
## Requirement
Python 3
## Usage
`python mbr_extractor.py <cmd> <diskpath>`

**rawdump** - Dump the complete MBR sector of the disk specified
**parseinfo** - Parse and MBR sector and interpret its info
**check** - Check if the sector is valid MBR sector (may give false result)
