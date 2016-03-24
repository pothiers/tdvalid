#! /usr/bin/env python3
"""Validate FITS header against schema"""

import sys
import argparse
import logging
import subprocess
import yaml

import pykwalify.core as kwal

#import fits_xml as fx
from . import fits_yaml as fy

def validate_yaml(hdict, schema):
    k = kwal.Core(source_data=hdict, schema_files=[schema])
    k.validate()
    return k

##############################################################################

def main():
    "Parse command line arguments and do the work."
    #!print('EXECUTING: %s\n\n' % (' '.join(sys.argv)))
    parser = argparse.ArgumentParser(
        description='My shiny new python program',
        epilog='EXAMPLE: %(prog)s a b"'
        )
    parser.add_argument('--version', action='version', version='1.0.1')
    parser.add_argument('yamlfile', type=argparse.FileType('r'),
                        help='Input YAML personality file.')
    parser.add_argument('yamlschema',
                        help='YAML schema file' )
    parser.add_argument('--loglevel',
                        help='Kind of diagnostic output',
                        choices=['CRTICAL', 'ERROR', 'WARNING',
                                 'INFO', 'DEBUG'],
                        default='WARNING')
    args = parser.parse_args()

    log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(log_level, int):
        parser.error('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level=log_level,
                        format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M')
    logging.debug('Debug output is enabled in %s !!!', sys.argv[0])
 
    yd = yaml.safe_load(args.yamlfile)
    validate_yaml(yd, args.yamlschema)

if __name__ == '__main__':
    main()
        
    
