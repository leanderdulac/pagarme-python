from pagarme import transaction
from tests.resources.dictionaries import transaction_dictionary


def test_calculate_installments_amount():
    array_installments = transaction.calculate_installments_amount(transaction_dictionary.CALCULATE_INTALLMENTS_AMOUNT)
    assert array_installments['installments'] is not None


def test_capture_transaction():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION_CAPTURE_FALSE)
    capture_transaction = transaction.capture(trx['id'], transaction_dictionary.REFUNDED_OR_CAPTURE_TRANSACTION)
    assert 'paid' == capture_transaction['status']


def test_create_transaction():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION)
    assert trx['id'] is not None


def test_create_transaction_with_split_rule_amount():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION_WITH_SPLIT_RULE_AMOUNT)
    assert trx['split_rules'] is not None


def test_create_transaction_with_split_rule_percentage():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION_WITH_SPLIT_RULE_PERCENTAGE)
    assert trx['split_rules'] is not None


def test_error_request():
    error = transaction.create(transaction_dictionary.INVALID_REQUEST)
    assert error[0]['type'] == 'invalid_parameter'


def test_find_all_postbacks():
    _transaction = transaction.create(transaction_dictionary.BOLETO_TRANSACTION)
    transaction.pay_boleto(_transaction['id'], transaction_dictionary.PAY_BOLETO)
    _transaction_paid = transaction.find_by(_transaction['id'])
    _postbacks = transaction.postbacks(_transaction_paid['id'])
    assert _postbacks[0]['model_id'] == str(_transaction_paid['id'])


def test_find_all_transaction_events():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION)
    all_events = transaction.events(trx['id'])
    assert all_events is not None


def test_find_all_transaction_operations():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION)
    all_operations = transaction.operations(trx['id'])
    assert all_operations[0]['id'] is not None


def test_find_all_transaction_payables():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION)
    all_payables = transaction.payables(trx['id'])
    assert all_payables is not None


def test_find_all_transactions():
    all_transactions = transaction.find_all()
    assert all_transactions is not None


def test_find_by():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION)
    find_trx = transaction.find_by(trx['id'])
    assert trx['id'] == find_trx['id']


def test_find_specific_payable():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION)
    all_payables = transaction.payables(trx['id'])
    specific_payable = transaction.specific_payable(trx['id'], all_payables[0]['id'])
    assert specific_payable['id'] is not None


def test_generate_card_hash_key():
    card_hash_key = transaction.generate_card_hash_key()
    assert card_hash_key is not None


def test_pay_boleto():
    trx = transaction.create(transaction_dictionary.BOLETO_TRANSACTION)
    pay_transaction = transaction.pay_boleto(trx['id'], transaction_dictionary.PAY_BOLETO)
    assert 'paid' == pay_transaction['status']


def test_postbacks_redeliver():
    _transaction = transaction.create(transaction_dictionary.BOLETO_TRANSACTION)
    transaction.pay_boleto(_transaction['id'], transaction_dictionary.PAY_BOLETO)
    _transaction_paid = transaction.find_by(_transaction['id'])
    _postbacks = transaction.postbacks(_transaction_paid['id'])
    redeliver = transaction.postback_redeliver(_transaction_paid['id'], _postbacks[0]['id'])
    assert redeliver['status'] == 'pending_retry'


def test_refund_transaction():
    trx = transaction.create(transaction_dictionary.VALID_CREDIT_CARD_TRANSACTION)
    refund_transaction = transaction.refund(trx['id'], transaction_dictionary.REFUNDED_OR_CAPTURE_TRANSACTION)
    refunded_transaction = transaction.find_by(refund_transaction['id'])
    assert 'refunded' == refunded_transaction['status']


def test_specific_postback():
    _transaction = transaction.create(transaction_dictionary.BOLETO_TRANSACTION)
    transaction.pay_boleto(_transaction['id'], transaction_dictionary.PAY_BOLETO)
    transaction_paid = transaction.find_by(_transaction['id'])
    postbacks = transaction.postbacks(transaction_paid['id'])
    specific_postback = transaction.specific_postback(transaction_paid['id'], postbacks[0]['id'])
    assert specific_postback['id'] == postbacks[0]['id']
