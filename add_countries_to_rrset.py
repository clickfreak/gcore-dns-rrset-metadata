#!/usr/bin/env python3

import json
import reverse_geocode
import pycountry_convert
import sys

# I removed filter_set_id and filters from json file rrset definition

def add_record_metadata(rrset, do_txt_rrset=False):
    for record in rrset.get("resource_records", []):
        latlong = record["meta"].get("latlong")
        if latlong:
            lat, lon = latlong
            location_metadata = reverse_geocode.search([(lat, lon)])
            print(location_metadata)
            country_code = location_metadata[0].get("country_code", None)

            if country_code:
                record["meta"]["countries"] = [country_code.lower()]
                continent = pycountry_convert.country_alpha2_to_continent_code(country_code.upper())
                record["meta"]["continents"] = [continent.lower()]
                if do_txt_rrset:
                    record['content'] = [" - ".join([continent,
                                                  location_metadata[0].get("country", '???'),
                                                  location_metadata[0].get("city", '???')])]
    if do_txt_rrset:
        rrset["type"] = "TXT"
    return rrset


def load_rrset(source):
    """
    Load RRSet JSON from a file or stdin.
    """
    try:
        if source == '-':
            rrset_str = json.loads(sys.stdin.read())
        else:
            with open(source, 'r') as file:
                rrset_str = json.load(file)
        return rrset_str
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error reading RRSet data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Add continent and country metadata to a DNS RRSet based on latlong coordinates.')
    parser.add_argument('source', metavar='SOURCE', type=str, 
                        help='the file path to the RRSet JSON or "-" to read from stdin')
    parser.add_argument('--do-txt-rrset', action='store_true',
                        help='replace "A" record type with "TXT" and replace IP address with country name')
    args = parser.parse_args()

    rrset = load_rrset(args.source)

    updated_rrset = add_record_metadata(rrset, do_txt_rrset=args.do_txt_rrset)
    del updated_rrset["name"]
    
    # Print the updated RRSet with country metadata added
    print(json.dumps(updated_rrset, indent=4))

