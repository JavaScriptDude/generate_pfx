# export PKCS_PASSWORD=_passwordfoo_
# python3 ./generate_pfx.py --privkey "<path_to_privkey_pem>" --cert "<path_to_cert_pem>"

import os
import sys
from getopt import getopt as getopts
from OpenSSL import crypto

def main(argv):
    global opts

    def printCli(s=None, exitCode=-1):
        print("""generate_pfx.py
    [-p|--privkey] <path to private key pem>
    [-c|--cert] <path to certificate pem>
    [-o|--output] <path for pfx> (opt)
    . default to cert.pfx located in same directory as --cert
    [-C|--clobber] (opt)
    . Clobber pfx if already existing
    . Default to False
    [-d|--dryrun] (opt)
    . Will run all code except writing of pfx
    [-?|-h|--help] (opt)
    * (opt) = Optional
        """)
        if s is not None:
            print(s)
        if exitCode > -1: sys.exit(exitCode)

    print('.: generate_pfx.py started :.')

    if "PKCS_PASSWORD" not in os.environ:
        printCli("Missing PKCS Password in PKCS_PASSWORD environment variable!", exitCode=2)

    opts={
         'output': None
        ,'clobber': False
        ,'dryrun': False
    }

    # Command Line Options
    try:
        goOpts, goArgs = getopts(
             argv
            , "hcdp:c:o:"
            ,["help", "clobber", "dryrun", "privkey=", "cert=", "output="]
        )
    except getopt.GetoptError as exc:
        printCli(exc, exitCode=2)
    for o, v in goOpts:
        if o in ("-?", "-h", "--help"):
            printCli()
            sys.exit()
        elif o in ("-p", "--privkey"):
            opts['privkey'] = v.strip()
        elif o in ("-c", "--cert"):
            opts['cert'] = v.strip()
        elif o in ("-o", "--output"):
            opts['output'] = v.strip()
        elif o in ("-C", "--clobber"):
            opts['clobber'] = True
        elif o in ("-d", "--dryrun"):
            opts['dryrun'] = True



    # validate cli args
    k='privkey'; v=opts[k] if k in opts else None
    if v is None or v == '' :
        printCli("Private is not defined (--privkey).", exitCode=2)
    if not os.path.isfile(v):
        printCli("Private key not found (--privkey). Path = {}".format(v), exitCode=2)

    k='cert'; v=opts[k] if k in opts else None
    if v is None or v == '' :
        printCli("Certificate is not defined (--cert).", exitCode=2)
    if not os.path.isfile(v):
        printCli("Certificate not found (--cert). Path = {}".format(v), exitCode=2)

    k='output'; v=opts[k] if k in opts else None
    if v is None:
        (certpath, certfile) = os.path.split(opts['cert'])
        opts['pfx_pem']="{}/{}".format(certpath, certfile.replace(".pem", ".pfx"))    
    else:
        (pfxpath, pfxfile) = os.path.split(v)
        if not os.path.isdir(pfxpath):
            printCli("Folder given for output (--output) does not exist. Path = {}".format(v), exitCode=2)
        opts['pfx_pem']=v

    if os.path.isfile(opts['pfx_pem']) and not opts['clobber']:
        printCli("PFX already exists and clobber (--clobber) not specified. Ignoring. Pfx path = {}".format(opts['pfx_pem']), exitCode=2)

    # Read in cert
    cert = crypto.load_certificate(
        crypto.FILETYPE_PEM, open(opts['cert'], 'rt').read()
    )

    # Read in private key
    privkey = crypto.load_privatekey(
        crypto.FILETYPE_PEM, open(opts['privkey'], 'rt').read()
    )

    # Generate PFX
    pfx = crypto.PKCS12Type()
    pfx.set_privatekey(privkey)
    pfx.set_certificate(cert)
    pfxdata = pfx.export(os.environ["PKCS_PASSWORD"])

    # Write PFX to file
    if opts['dryrun']:
        print(" + Dry run set (--dryrun). pfx will not be written.")
        print(" + PFX file path = {}".format(opts['pfx_pem']))
    else:
        with open(opts['pfx_pem'], 'wb') as f:
            f.write(pfxdata)
        print(' + PFX File Created: {0}'.format(opts['pfx_pem']))
    
    
    print('.: done :.')


if __name__ == '__main__':
    main(sys.argv[1:])