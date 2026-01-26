#!/usr/bin/env python3
import pycurl, os, json, io
from tqdm import tqdm


def upload_record_with_json(json_file, xsdb_url='https://xsecdb-xsdb-official.app.cern.ch'):
    c = pycurl.Curl()
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.COOKIEJAR, os.path.expanduser("~/private/xsdbdev-cookie.txt"))
    c.setopt(c.COOKIEFILE, os.path.expanduser("~/private/xsdbdev-cookie.txt"))
    c.setopt(c.HTTPHEADER, ['Content-Type:application/json', 'Accept:application/json'])
    c.setopt(c.VERBOSE, False)  # set to True for debug
    api_url = os.path.join(xsdb_url, 'api')
    c.setopt(c.URL, os.path.join(api_url, 'insert'))
    c.setopt(c.POST, True)
    byte_io = io.BytesIO()
    c.setopt(c.WRITEFUNCTION, byte_io.write)

    with open(json_file) as f:
        data = json.load(f)
    for record in data['records']:
        c.setopt(c.POSTFIELDS, json.dumps(record))
        c.perform()


def upload_records_with_json(json_dir='./json'):
    for json_file in tqdm(os.listdir(json_dir), desc="Uploading records to XSDB with JSON files"):
        if not json_file.endswith(".json"):
            continue
        json_file = os.path.join(json_dir, json_file)
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if '$' in content:
            print(f"Warning: {json_file} failed")
            continue  # skip unconverted files
        upload_record_with_json(json_file=json_file)


if __name__ == "__main__":
    upload_records_with_json()
