#! /usr/bin/env python3
"""Validate FITS header against schema"""

import sys
import argparse
import logging
import subprocess

import fits_xml as fx

def validate_header(xmlheader, rng=None):
    #!print('header={}'.format(xmlheader))
    try:
        str = subprocess.check_output(['xmllint',
                                       '--noout',
                                       '--relaxng', rng,
                                       '-'],
                                      universal_newlines=True,
                                      input=xmlheader)
    except subprocess.CalledProcessError as ex:
        logging.debug('Could not run XMLLINT: {}; {}'.format(ex, ex.output))
        return False
    return str

##############################################################################

def main():
    "Parse command line arguments and do the work."
    #!print('EXECUTING: %s\n\n' % (' '.join(sys.argv)))
    parser = argparse.ArgumentParser(
        description='My shiny new python program',
        epilog='EXAMPLE: %(prog)s a b"'
        )
    parser.add_argument('--version', action='version', version='1.0.1')
    parser.add_argument('fitsfile', type=argparse.FileType('r'),
                        help='Input FITS file. Read header from this.')
    parser.add_argument('schema',
                        help='Relax NG (.rng) schema file for instrument',
                        default='NA')
    parser.add_argument('--loglevel',
                        help='Kind of diagnostic output',
                        choices=['CRTICAL', 'ERROR', 'WARNING',
                                 'INFO', 'DEBUG'],
                        default='WARNING')
    args = parser.parse_args()
    args.fitsfile.close()
    args.fitsfile = args.fitsfile.name

    log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(log_level, int):
        parser.error('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level=log_level,
                        format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M')
    logging.debug('Debug output is enabled in %s !!!', sys.argv[0])
 
    xmlheader = fx.fits_to_xml(args.fitsfile)
    print(validate_header(xmlheader, rng=args.schema))

if __name__ == '__main__':
    main()
        
    
