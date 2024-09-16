About
-----

This script reads the RRSet JSON definition with the Gcore DNS Provider scheme (https://api.gcore.com/docs/dns?#tag/RRsets/operation/CreateRRSet) and adds additional geo-balancing metadata to resource records based on their existing coordinates metadata (Latitude, Longitude).

Install
-------

```bash
apt-get install python3-geopy python3-pycountry
```

```bash
pip3 install -r requirements.txt
```

Usage
-----

You can pass RRSet json definition as file argument
```
./add_countries_to_rrset.py rrset_with_latlongs.json
```

or via stdin:
```
cat rrset_with_latlongs.json | ./add_countries_to_rrset.py -
```

The script can also create a new TXT RRSet with continent, country, and city in the TXT record content to simplify debugging using online tools like https://dnschecker.org/ or https://www.whatsmydns.net/.

TODO
----
- [ ] Use Gcore Permanent Token to perform updates in-place via Gcore DNS API
- [ ] Add metadata based on GeoIP databases (local mmdb or using online tools like ipinfo.io)
- [ ] Add RRSet examples
