"""Historical factor R classifier, not activity or regime eligibility advice."""
from datetime import date
from decimal import Decimal, localcontext
from .engine import money, evidence
from . import __version__

SOURCE = 'https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=92278'


def factor_r(inputs):
    required = {'period', 'fs12', 'rbt12r', 'confirmed_subject_to_factor_r', 'confirmed_full_12_month_history'}
    if not isinstance(inputs, dict) or set(inputs) != required:
        raise ValueError('Expected exact factor R input fields')
    period = date.fromisoformat(inputs['period'])
    if period.day != 1 or period.year != 2025:
        raise ValueError('Only historical 2025 monthly periods supported')
    if inputs['confirmed_subject_to_factor_r'] is not True or inputs['confirmed_full_12_month_history'] is not True:
        raise ValueError('Activity scope and full prior 12-month history must be confirmed externally')
    fs, rb = money(inputs['fs12']), money(inputs['rbt12r'])
    with localcontext() as c:
        c.prec = 40
        if rb == 0:
            ratio = Decimal('0.28') if fs > 0 else Decimal('0.01')
            annex = 'III' if fs > 0 else 'V'
        elif fs == 0:
            ratio, annex = Decimal('0.01'), 'V'
        else:
            ratio = fs / rb
            annex = 'III' if fs * 100 >= rb * 28 else 'V'
        result = {'status': 'historical_experimental_classification', 'engine_version': __version__,
                  'inputs': inputs, 'rule_id': 'BR-SN-FATOR-R-2025', 'jurisdiction': 'BR',
                  'source': SOURCE, 'provision': 'Res. CGSN 140/2018 art. 26, §7; LC 123 art. 18',
                  'factor_r': str(ratio), 'annex': annex, 'threshold': '0.28',
                  'limitations': ['Only established businesses with full 12-month history',
                                  'FS12 includes eligible paid payroll and charges; RBT12r includes domestic and export revenue',
                                  'Activity and Simples eligibility not inferred; no professional or PGDAS-D validation']}
    return {**result, 'evidence_sha256': evidence(result)}
