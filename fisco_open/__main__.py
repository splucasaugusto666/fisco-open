import argparse,json,sys
from pathlib import Path
from .engine import calculate,compare
from .rtc import request_rtc,UPSTREAM

def main():
    p=argparse.ArgumentParser(description='FISCO OPEN research preview')
    p.add_argument('command',choices=['calculate','compare','rtc-regular','rtc-simples','upstream'])
    p.add_argument('file',nargs='?'); p.add_argument('--port',type=int)
    a=p.parse_args()
    try:
        if a.command=='upstream': result=UPSTREAM
        else:
            if not a.file: raise ValueError('Input JSON file required')
            path=Path(a.file)
            if path.stat().st_size>5*1024*1024: raise ValueError('Input exceeds 5 MiB')
            data=json.loads(path.read_text(encoding='utf-8'))
            if a.command=='calculate': result=calculate(data)
            elif a.command=='compare': result=compare(data)
            else: result=request_rtc(a.command[4:],data,a.port)
        print(json.dumps(result,ensure_ascii=False,indent=2)); return 0
    except (ValueError,TypeError,OSError,KeyError,ArithmeticError) as e:
        print('Input or execution rejected: '+str(e),file=sys.stderr); return 2
if __name__=='__main__': sys.exit(main())
