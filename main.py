"""Classify a change between two numeric semantic versions."""
import argparse,csv,io,json,math,re
from collections import Counter
from datetime import date,datetime
from pathlib import Path

import base64,ipaddress,uuid
from urllib.parse import parse_qsl,urlsplit
from http.cookies import SimpleCookie

def analyze(data):
    def parse(value):
        parts=value.split('.')
        if len(parts)!=3 or any(not p.isdigit() for p in parts):raise ValueError('Use numeric major.minor.patch')
        return tuple(map(int,parts))
    before,after=parse(data['before']),parse(data['after'])
    changed=next((name for name,a,b in zip(('major','minor','patch'),before,after) if a!=b),'none')
    return {'change':changed,'direction':'upgrade' if after>before else 'downgrade' if after<before else 'unchanged'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',type=Path,help='UTF-8 JSON input file')
    parser.add_argument('--explain',action='store_true',help='Send the local report to the configured chat gateway')
    args=parser.parse_args()
    report=analyze(json.loads(args.input.read_text(encoding='utf-8')))
    if args.explain:
        from gateway_client import explain
        print(explain(report))
    else:print(json.dumps(report,ensure_ascii=False,indent=2))
