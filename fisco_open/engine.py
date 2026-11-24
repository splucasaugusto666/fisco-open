"""Restricted historical Simples estimate; not an assessment or eligibility determination."""
from decimal import Decimal, localcontext, ROUND_HALF_UP
from datetime import date
from hashlib import sha256
import json
from . import __version__
D = Decimal
SOURCE = 'https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp123.htm'
# LC 123 art. 18 and annexes, first four bands; conservative historical subset.
LIMITS = tuple(map(D, ('180000','360000','720000','1800000')))
TABLE = {'I': [('0.04','0'),('0.073','5940'),('0.095','13860'),('0.107','22500')],
         'II': [('0.045','0'),('0.078','5940'),('0.10','13860'),('0.112','22500')],
         'III': [('0.06','0'),('0.112','9360'),('0.135','17640'),('0.16','35640')],
         'IV': [('0.045','0'),('0.09','8100'),('0.102','12420'),('0.14','39780')],
         'V': [('0.155','0'),('0.18','4500'),('0.195','9900'),('0.205','17100')]}
ASSUMPTIONS = ('confirmed_eligible','confirmed_annex','established_business','single_domestic_revenue','no_special_treatment','below_applicable_limits')
def money(value):
    if not isinstance(value, str): raise ValueError('Monetary values must be decimal strings')
    try: n = D(value)
    except Exception: raise ValueError('Invalid monetary value') from None
    if not n.is_finite() or n < 0 or n > D('1000000000000') or n.as_tuple().exponent < -2:
        raise ValueError('Expected nonnegative BRL amount with at most two decimal places')
    return n

def rounded(n): return format(n.quantize(D('.01'),rounding=ROUND_HALF_UP),'f')
def evidence(data):
    return sha256(json.dumps(data,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def calculate(inputs):
    if not isinstance(inputs,dict): raise ValueError('Expected object')
    required = {'period','annex','rbt12','revenue','assumptions'}
    if set(inputs)!=required: raise ValueError('Expected exactly: '+', '.join(sorted(required)))
    period = date.fromisoformat(inputs['period'])
    if period.day != 1 or not date(2025,1,1)<=period<=date(2025,12,1): raise ValueError('Unsupported period: historical 2025 monthly periods only')
    a=inputs['annex']; flags=inputs['assumptions']
    if a not in TABLE: raise ValueError('Unsupported annex')
    if not isinstance(flags,dict) or set(flags)!=set(ASSUMPTIONS) or any(flags[k] is not True for k in ASSUMPTIONS): raise ValueError('All scope conditions must be confirmed; no eligibility inference')
    r, revenue=money(inputs['rbt12']),money(inputs['revenue'])
    if not 0<r<=LIMITS[-1] or revenue>LIMITS[-1]: raise ValueError('Unsupported revenue range')
    i=next(i for i,b in enumerate(LIMITS) if r<=b)
    nominal,deduction=map(D,TABLE[a][i])
    with localcontext() as c:
        c.prec=40
        rate=(r*nominal-deduction)/r
        # Round at final estimate only, not a PGDAS-D allocation replica.
        total=rounded(revenue*(r*nominal-deduction)/r)
        result={'status':'experimental_estimate','engine_version':__version__,'inputs':inputs,'rule_id':f'BR-SN-{a}-2025-{i+1}', 'source':SOURCE,'provision':f'LC 123/2006 art. 18 and Annex {a}','jurisdiction':'BR','supported_period':['2025-01-01','2025-12-31'],'nominal_rate':str(nominal),'deduction_brl':rounded(deduction),'effective_rate':str(rate),'estimated_das_brl':total,'rounding':'final cent HALF_UP; allocation not reproduced','limitations':['No eligibility determination','No tax segregation or special treatments','No PGDAS-D parity or professional validation','No official RTC engine used in this calculation']}
    if a == 'IV':
        result['limitations'].append('Annex IV DAS excludes employer social security contributions (CPP); total burden is not calculated')
    return {**result,'evidence_sha256':evidence(result)}

def compare(scenarios):
    """Compare supplied hypothetical amounts; do not infer legal eligibility."""
    if not isinstance(scenarios,list) or not scenarios: raise ValueError('Nonempty scenario list required')
    out=[]; seen=set()
    for s in scenarios:
        fields={'name','revenue','costs','expenses','taxes','other_obligations','implementation_cost','eligibility_confirmed'}
        if not isinstance(s,dict) or set(s)!=fields or not isinstance(s['name'],str) or not s['name'] or s['name'] in seen: raise ValueError('Invalid or duplicate scenario')
        seen.add(s['name'])
        if s['eligibility_confirmed'] is not True: raise ValueError('Only externally confirmed eligible scenarios accepted')
        with localcontext() as c:
            c.prec=40
            net=money(s['revenue'])-sum(money(s[k]) for k in ('costs','expenses','taxes','other_obligations','implementation_cost'))
            out.append({'name':s['name'],'net_brl':rounded(net),'inputs':s})
    out.sort(key=lambda s:D(s['net_brl']),reverse=True)
    result={'status':'hypothetical_comparison','engine_version':__version__,'scenarios':out,'limitation':'Inputs and eligibility externally supplied; no regime recommendation. Compare equal time horizons and avoid double counting.'}
    return {**result,'evidence_sha256':evidence(result)}
