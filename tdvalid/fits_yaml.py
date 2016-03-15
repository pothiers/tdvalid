#! /usr/bin/env python3
"""Create YAML version of a FITS header."""
# For schema language, see:
#   https://raw.githubusercontent.com/Grokzen/pykwalify/master/docs/Validation%20Rules.md
# The original kwalify spec for schema is:
#   http://www.kuwata-lab.com/kwalify/ruby/users-guide.01.html#schema


import sys
import argparse
import logging
import yaml
import astropy.io.fits as pyfits

# To generate very rough XSD:
#   http://www.thaiopensource.com/relaxng/trang.html (best; install java)
#   http://xmlgrid.net/xml2xsd.html (online)
#
# Validate with:
#   fits_to_xml(myfile.fits, myfile.fits.xml)
#   java -jar trang.jar myfile.fits.xml ... <instrum>.xsd
#   xmllint --schema <instrum>.xsd myfile.fits.xml


USED_FIELDS=set([
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


def get_hdr_as_dict(fitsfile):
    hdict = dict()
    hdulist = pyfits.open(fitsfile)
    for field in USED_FIELDS:
        if field in hdulist[0].header:
            # use existing Primary HDU field
            hdict[field] = hdulist[0].header[field]
        else:
            # use last existing Extension HDU field
            for hdu in hdulist[1:]:
                if field in hdu.header:
                    hdict[field] = hdu.header[field]
    return hdict


    
def fits_to_yaml(fits_fname, yaml_stream, instrument='NA'):
    hdulist = pyfits.open(fits_fname)
    #!print('DBG: hdr={}'.format(hdulist[0].header.tostring()))
    hdr = get_hdr_as_dict(fits_fname)
    print(yaml.safe_dump(hdr, default_flow_style=False), file=yaml_stream)
    return hdr


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
    parser.add_argument('yamlfile', type=argparse.FileType('w'),
                        help='Output YAML file. YAML format of FITS header.')
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
 
    fits_to_yaml(args.fitsfile, args.yamlfile, instrument=args.instrument)

if __name__ == '__main__':
    main()
        
    
