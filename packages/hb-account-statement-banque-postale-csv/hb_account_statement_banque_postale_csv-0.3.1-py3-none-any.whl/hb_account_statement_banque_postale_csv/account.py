from io import BytesIO, TextIOWrapper
import csv
import calendar

from datetime import datetime
from decimal import Decimal as D

from trytond.pool import PoolMeta, Pool


class StatementImportStart(metaclass=PoolMeta):
    __name__ = 'account.statement.import.start'

    @classmethod
    def __setup__(cls):
        super(StatementImportStart, cls).__setup__()
        cls.file_format.selection.append(
            ('banque_postale_csv', "Banque Postale (CSV)"))


class StatementImport(metaclass=PoolMeta):
    __name__ = 'account.statement.import'

    def parse_banque_postale_csv(self, encoding='utf8'):
        with TextIOWrapper(BytesIO(self.start.file_),
                           encoding=encoding) as csvfile:
            read = csvfile.read()
            csvfile.seek(0)
            csvkwarg = {}
            if ';' in read:
                csvkwarg['delimiter'] = ';'
            elif '\t':
                csvkwarg['dialect'] = csv.excel_tab

            reader = csv.reader(csvfile, **csvkwarg)
            bank_statement = {'lines': []}
            row = next(reader)
            while self.is_not_empty(row):
                bank_statement[row[0].strip()] = row[1]
                row = next(reader)

            header = next(reader)

            for row in reader:
                bank_statement['lines'].append(dict(zip(header, row)))

            self.format_header(bank_statement)

        return [self.cast_to_tryton_statement(bank_statement)]

    def is_not_empty(self, row):
        if row == []:
            return False

        if len(row) == 3:
            if row == ['', '', '']:
                return False

        return True

    def format_header(self, bank_statement):
        type_ = bank_statement['Type']
        if type_ == 'COMPTE':
            return

        if type_ == 'CCP':
            if not bank_statement.get('Numéro Compte'):
                for key in ('', 'Numéro de compte', '\ufeffNuméro de compte'):
                    if key in bank_statement:
                        bank_statement['Numéro Compte'] = bank_statement.pop(
                            key)

            solde_key = None
            for key in bank_statement.keys():
                if key.startswith('Solde comptable au '):
                    solde_key = key

            bank_statement['Solde (EUROS)'] = bank_statement[
                solde_key].split(' ')[0]
            for line in bank_statement['lines']:
                if not line.get('Montant(EUROS)'):
                    line['Montant(EUROS)'] = line.pop('Montant')[:-1]

    def cast_to_tryton_statement(self, bank_statement):
        pool = Pool()
        Statement = pool.get('account.statement')
        Configuration = pool.get('account.configuration')

        statement = Statement()

        statement.name = bank_statement['Numéro Compte']
        statement.company = self.start.company

        statement.journal = Configuration(
            1).default_statement_journal_for_bp_csv

        bank_stmt_lines = self.cast_to_tryton_statement_lines(
            statement, bank_statement['lines'])

        bkstmt_date = max([l_.date for l_ in bank_stmt_lines])
        _, last_day = calendar.monthrange(bkstmt_date.year, bkstmt_date.month)
        bkstmt_date = bkstmt_date.replace(day=last_day)
        statement.date = bkstmt_date

        statement.end_balance = bank_statement['Solde (EUROS)'].replace(
            ',', '.')
        statement.start_balance = (
            D(statement.end_balance) - sum(
                [D(l_.amount) for l_ in bank_stmt_lines])
        )
        statement.number_of_lines = len(bank_stmt_lines)
        statement.total_amount = sum([D(l_.amount) for l_ in bank_stmt_lines])
        statement.lines = bank_stmt_lines
        return statement

    def cast_to_tryton_statement_lines(self, statement, stmt_lines):
        return [self.cast_to_tryton_statement_line(statement, stmt_line)
                for stmt_line in stmt_lines]

    def cast_to_tryton_statement_line(self, statement, stmt_line):
        pool = Pool()
        Line = pool.get('account.statement.line')

        line = Line()
        line.number = stmt_line['Libellé']
        line.amount = stmt_line['Montant(EUROS)'].replace(',', '.')
        line.date = datetime.strptime(stmt_line['Date'], '%d/%m/%Y').date()

        if hasattr(line, 'set_account_and_party_from_ml'):
            line.set_account_and_party_from_ml()

        if not hasattr(line, 'account'):
            line.account = statement.journal.account

        return line
