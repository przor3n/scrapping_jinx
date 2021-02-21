#!/usr/bin/env python3

def write_response_to_file(response):
    with open('dupa', 'w') as f:
        body = response._get_body()

        if type(body) == bytes:
            f.write(response._get_body().decode('utf-8'))
        else:
            f.write(response._get_body().encode('utf-8'))
