# generate_pfx
CLI Python script to generate pfx files for supplied private key and certificate

## Usage:

```text
Usage: python3 ./generate_pfx [-h] [-d] [-C] -p <private_key_pem> -c <certificate_pem> [-o <output_pfx>]

Parameters:
 --privkey (-p) path/to/priv_key.pem  path to private key
 --cert (-c) path/to/cert.pem         path to certificate
 --output (-o) path/to/key.pfx        default to cert.pfx located in same directory as --cert
 --help (-h)                          Prints cli usage
 --dryrun (-d)                        Will run all code except writing of pfx
 --clobber (-C)                       Overwrite pfx if already existing
```
Important: set an environment variable PKCS_PASSWORD to the password you want eg:

```export PKCS_PASSWORD=_foobar_```
