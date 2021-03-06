#! /usr/bin/env python3
"""Create XML version of a FITS header."""

import sys
import argparse
import logging

import astropy.io.fits as pyfits

# To generate very rough XSD:
#   http://www.thaiopensource.com/relaxng/trang.html (best; install java)
#   http://xmlgrid.net/xml2xsd.html (online)
#
# Validate with:
#   fits_to_xml(myfile.fits, myfile.fits.xml)
#   java -jar trang.jar myfile.fits.xml ... <instrum>.xsd
#   xmllint --schema <instrum>.xsd myfile.fits.xml


used_fields=set([
    'DATE',
    'DATE-OBS',
    'DTACQNAM',
    'DTCALDAT',
    'DTINSTRU',
    'DTNSANAM',
    'DTPROPID',
    'DTSITE',
    'DTTELESC',
    'IMAGETYP',
    'OBSERVAT',
    'OBSTYPE',
    'PLDSID',
    'PLQNAME',
    'PLQUEUE',
    'PROCTYPE',
    'PRODTYPE',
    'SIMPLE',
    'TIME-OBS',
    ])
    
def fits_to_xml(fits_fname, xml_file=None, instrument='NA'):
    hdulist = pyfits.open(fits_fname)
    #xmlstr = '<fitsHeader instrument="{}">\n'.format(instrument)
    xmlstr = '<fitsHeader>\n'
    #!print('DBG: hdr={}'.format(hdulist[0].header.tostring()))
    hdr = hdulist[0].header
    for k,v in hdr.items():
        if k not in used_fields:
            continue
        if k == 'COMMENT': 
            continue
        if k == '': 
            continue
        #print('k={}, v={}'.format(k,v))
        xmlstr += '  <{key}>{value}</{key}>\n'.format(key=k, value=v)
    xmlstr += '</fitsHeader>\n'
    if xml_file != None:
        print(xmlstr, file=xml_file)
    return xmlstr


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
    parser.add_argument('xmlfile', type=argparse.FileType('w'),
                        help='Output XML file. XML format of FITS header.')
    parser.add_argument('--instrument',
                        help='Name of instrument',
                        default='NA')
    parser.add_argument('--loglevel',
                        help='Kind of diagnostic output',
                        choices=['CRTICAL', 'ERROR', 'WARNING',
                                 'INFO', 'DEBUG'],
                        default='WARNING')
    args = parser.parse_args()
    args.fitsfile.close()
    args.fitsfile = args.fitsfile.name
    #!args.outfile.close()
    #!args.outfile = args.outfile.name

    #!print 'My args=',args
    #!print 'infile=',args.infile

    log_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(log_level, int):
        parser.error('Invalid log level: %s' % args.loglevel)
    logging.basicConfig(level=log_level,
                        format='%(levelname)s %(message)s',
                        datefmt='%m-%d %H:%M')
    logging.debug('Debug output is enabled in %s !!!', sys.argv[0])
 
    fits_to_xml(args.fitsfile, args.xmlfile, instrument=args.instrument)

if __name__ == '__main__':
    main()
        
    
