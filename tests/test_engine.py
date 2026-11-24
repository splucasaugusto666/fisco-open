import unittest,json,copy,threading
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from fisco_open.engine import calculate,compare,evidence
from fisco_open.rtc import request_rtc
BASE=json.loads((Path(__file__).resolve().parents[1]/'examples/commerce.json').read_text())
class Engine(unittest.TestCase):
    def test_golden(self): self.assertEqual(calculate(BASE)['estimated_das_brl'],'6685.00')
    def test_evidence(self):
        r=calculate(BASE); h=r.pop('evidence_sha256'); self.assertEqual(h,evidence(r))
    def test_boundary(self):
        for rbt,rate in [('180000','0.04'),('180000.01','0.073'),('360000','0.073'),('360000.01','0.095'),('720000','0.095'),('720000.01','0.107')]:
            self.assertEqual(calculate(dict(BASE,rbt12=rbt))['nominal_rate'],rate)
    def test_other_annex(self):
        self.assertEqual(calculate(dict(BASE,annex='V',rbt12='180000',revenue='10000'))['estimated_das_brl'],'1550.00')
        self.assertEqual(calculate(dict(BASE,annex='II',rbt12='180000',revenue='10000'))['estimated_das_brl'],'450.00')
    def test_reject(self):
        for k,v in [('period','2026-01-01'),('rbt12','0'),('rbt12','1800000.01'),('revenue','NaN'),('revenue',1.0),('revenue','-1'),('revenue','1.001'),('annex','III'),('assumptions',{})]:
            with self.subTest(k=k,v=v),self.assertRaises(ValueError): calculate(dict(BASE,**{k:v}))
    def test_no_false_eligibility(self):
        b=copy.deepcopy(BASE); b['assumptions']['confirmed_eligible']=False
        with self.assertRaises(ValueError): calculate(b)
    def test_zero_revenue(self): self.assertEqual(calculate(dict(BASE,revenue='0'))['estimated_das_brl'],'0.00')
    def test_compare(self):
        s=json.loads((Path(__file__).resolve().parents[1]/'examples/scenarios.json').read_text()); r=compare(s); self.assertEqual(r['scenarios'][0]['net_brl'],'29500.00')
        s[0]['eligibility_confirmed']=False
        with self.assertRaises(ValueError): compare(s)
class MockRTC(unittest.TestCase):
    def test_transport(self):
        class H(BaseHTTPRequestHandler):
            def do_POST(self):
                data=self.rfile.read(int(self.headers['Content-Length']))
                self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(json.dumps({'route':self.path,'payload':json.loads(data)}).encode())
            def log_message(self,*args): pass
        srv=HTTPServer(('127.0.0.1',0),H); t=threading.Thread(target=srv.serve_forever,daemon=True); t.start()
        try:
            for kind,path in [('regular','/api/calculadora/regime-geral'),('simples','/api/calculadora/observabilidade/simples-nacional')]:
                r=request_rtc(kind,{'synthetic':True},srv.server_port); self.assertEqual(r['response']['route'],path); self.assertFalse(r['running_commit_verified'])
        finally: srv.shutdown(); srv.server_close(); t.join()
