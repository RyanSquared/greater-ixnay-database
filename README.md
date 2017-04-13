## Installing

```sh
pip3 install [--user] [--upgrade] .
```

## Running

```sh
python3 -m gixnaydb
```

## Self-signed certificate verification

Please note that this is not the best way to enable TLS on a local copy of the
software but this is the easiest way to do so without CA verification. Let's
Encrypt is an easy way to get free certificates but requires a domain name to
use.

```sh
mkdir ssl
cd ssl
openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365
```
