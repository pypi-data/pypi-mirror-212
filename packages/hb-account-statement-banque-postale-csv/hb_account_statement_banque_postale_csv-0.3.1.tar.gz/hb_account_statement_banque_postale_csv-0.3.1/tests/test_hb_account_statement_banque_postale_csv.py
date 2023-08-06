from trytond.tests.test_tryton import load_doc_tests
from trytond.tests.test_tryton import ModuleTestCase


class HbAccountStatementBanquePostaleCsvTestCase(ModuleTestCase):
    'Test Hb Account Statement Banque Postale Csv module'
    module = 'hb_account_statement_banque_postale_csv'


def load_tests(*args, **kwargs):
    return load_doc_tests(__name__, __file__, *args, **kwargs)

del ModuleTestCase
