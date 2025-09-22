#!/usr/bin/env python3
import pycurl, os, json


def insert_xsdb_with_file(json_file):
    base_url = 'https://xsecdb-xsdb-official.app.cern.ch'
    api_url = os.path.join(base_url, 'api')

    c = pycurl.Curl()
    c.setopt(c.FOLLOWLOCATION, 1)
    c.setopt(c.COOKIEJAR, os.path.expanduser("~/private/xsdbdev-cookie.txt"))
    c.setopt(c.COOKIEFILE, os.path.expanduser("~/private/xsdbdev-cookie.txt"))
    c.setopt(c.HTTPHEADER, ['Content-Type:application/json', 'Accept:application/json'])
    c.setopt(c.VERBOSE, False)  # set to True for debug
    c.setopt(c.URL, os.path.join(api_url, 'insert'))
    c.setopt(c.POST, True)
    byte_io = io.BytesIO()
    c.setopt(c.WRITEFUNCTION, byte_io.write)

    with open(os.path.expanduser(json_file)) as data_file:    
        data = json.load(data_file)
    for record in data['records']:
        c.setopt(c.POSTFIELDS, json.dumps(record))
        c.perform()
    print(f'Successfully uploaded {json_file}')


def insert_xsdb_records(json_dir='./json'):
    for filename in os.listdir(json_dir):
        if not filename.endswith(".json"): 
            continue
        process_name = filename.split(".")[0]
        print(process_name)
        
        json_file = os.path.join(json_dir, filename)
        with open(json_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if '$' in content:
            print("json corrupted, skipping")
        else:
            print("json OK, uploading")
            insert_xsdb_with_file(json_file)


if __name__ == "__main__":
    insert_xsdb_records(json_dir='./json', log_dir='./insert_xsdb_logs')
