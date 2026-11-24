"""Local-only adapters for documented RTC routes; transport is not fiscal validation."""
import json
from urllib.request import Request, build_opener, ProxyHandler, HTTPRedirectHandler
from urllib.error import URLError
from hashlib import sha256
from .engine import evidence
UPSTREAM={
 'regular':{'repo':'calculadora-rtc-regime-regular','commit':'150cccbe414d4a5edea703e4f7a424af5aa222c7','port':8080,'path':'/api/calculadora/regime-geral'},
 'simples':{'repo':'calculadora-rtc-simples-nacional','commit':'c5b0f01c8351c3f0d0795cc617b29d233e9f98df','port':8082,'path':'/api/calculadora/observabilidade/simples-nacional'},
 'danfse':{'repo':'calculadora-rtc-gerador-danfse','commit':'8d79e6b2f7fad6375340afcb51c85ed370c64a14','port':8080,'path':'/api/danfse'}}
class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs): return None

def request_rtc(kind,payload,port=None):
    if kind not in ('regular','simples'): raise ValueError('Unsupported calculator adapter')
    if not isinstance(payload,(dict,list)): raise ValueError('Expected JSON object or array')
    target=UPSTREAM[kind]; port=target['port'] if port is None else port
    if type(port) is not int or not 1<=port<=65535: raise ValueError('Invalid port')
    data=json.dumps(payload,allow_nan=False,separators=(',',':')).encode()
    if len(data)>5*1024*1024: raise ValueError('Payload exceeds 5 MiB')
    req=Request(f'http://127.0.0.1:{port}'+target['path'],data=data,headers={'Content-Type':'application/json','Accept':'application/json'},method='POST')
    try:
        with build_opener(ProxyHandler({}),NoRedirect()).open(req,timeout=15) as resp:
            if resp.headers.get_content_type()!='application/json': raise ValueError('Non-JSON upstream response')
            raw=resp.read(5*1024*1024+1)
    except (URLError,TimeoutError,OSError): raise ValueError('Local RTC service unavailable or returned HTTP error') from None
    if len(raw)>5*1024*1024: raise ValueError('Response exceeds 5 MiB')
    result={'status':'upstream_response_unvalidated','upstream_repo':target['repo'],'reference_commit':target['commit'],'running_commit_verified':False,'request_sha256':sha256(data).hexdigest(),'response_sha256':sha256(raw).hexdigest(),'response':json.loads(raw,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON')))}
    return {**result,'evidence_sha256':evidence(result)}
