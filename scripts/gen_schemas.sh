#!/bin/bash -e
# PURPOSE: Generate XML schemas (.xsd) from XML exemplars
#
# EXAMPLE:
#
# AUTHORS: S.Pothier

cmd=`basename $0`
dir=`dirname $0`

SCRIPT=$(readlink -f $0)      #Absolute path to this script
SCRIPTPATH=$(dirname $SCRIPT) #Absolute path this script is in

usage="USAGE: $cmd [options] [reportFile]
OPTIONS:
  -p <progress>:: Number of progress updates per second (default=0)
  -v <verbosity>:: higher number for more output (default=0)

"

VERBOSE=0
PROGRESS=0
while getopts "hp:v:" opt; do
    echo "opt=<$opt>"
    case $opt in
	    h)
            echo "$usage"
            exit 1
            ;;
        v)
            VERBOSE=$OPTARG
            ;;
        p)
            PROGRESS=$OPTARG # how often to report progress
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            exit 1
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            exit 1
            ;;

    esac
done
#echo "OPTIND=$OPTIND"
for (( x=1; x<$OPTIND; x++ )); do shift; done


RAC=0 # Required Argument Count
if [ $# -lt $RAC ]; then
    echo "Not enough non-option arguments. Expect at least $RAC."
    echo >&2 "$usage"
    exit 2
fi


#!echo "PROGRESS=$PROGRESS"
#!echo "VERBOSE=$VERBOSE"
#!echo "Remaining arguments:"
#!for arg do echo '--> '"\`$arg'" ; done

jardir=~/sandbox/tdvalid/scripts


##############################################################################

for dir in ~/data/scraped/mtn_raw/*; do
    echo "Generate XSD for: $dir"
    instrum=`basename $dir`
    for fits in $dir/*.fits.fz; do
        #! echo "Generate XML for: $fits"
        fits_xml.py --instrument $instrum $fits $fits.xml
    done
    java -jar $jardir/trang.jar $dir/*.fits.fz.xml $instrum.rng
    java -jar $jardir/trang.jar $dir/*.fits.fz.xml $instrum.rnc
    java -jar $jardir/trang.jar $dir/*.fits.fz.xml $instrum.dtd
    java -jar $jardir/trang.jar $dir/*.fits.fz.xml $instrum.xsd    
done

# xmllint --noout --schema ct4m-decam.xsd /home/pothiers/data/scraped/mtn_raw/ct4m-decam/DECam_00482540.fits.fz.xml

##############################################################################
# Local Variables:
# fill-column:75
# mode:sh
# End:

