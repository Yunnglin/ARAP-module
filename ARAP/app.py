from flask import Flask, request
import json
from utils.res_json import *
from utils.decimal_encoder import DecimalEncoder
from flasgger import Swagger, swag_from

from ARAPDao import ARAPDao

app = Flask(__name__)
Swagger(app)


@app.route('/')
def hello_world():
    """


        """
    return 'Hello World!'


def addPayRemain(_id, _days):
    arap = ARAPDao()
    rows = arap.query_purchase_pay(_id, _days)
    remain = arap.query_purchase_pay_remain(_id)
    if len(rows) >= 1:
        res = ARAPDao.to_purchase_pay_dict(rows)
        res[0]['remain'] = remain
        return res
    else:
        return False


def addReceiveRemain(_id, _days):
    arap = ARAPDao()
    rows = arap.query_sell_receive(_id, _days)
    remain = arap.query_sell_receive_remain(_id)
    if len(rows) >= 1:
        res = ARAPDao.to_sell_receive_dict(rows)
        res[0]['remain'] = remain
        return res
    else:
        return False


@app.route('/addPurchasePay', methods=['POST'])
@swag_from('api.yml')
def addPurchasePay():
    _json = request.json
    _purchaseId = _json.get('purchaseId')
    _reason = _json.get('reason')
    try:
        arap = ARAPDao()
        row = arap.add_purchase_pay(_purchaseId, _reason)
        if row == 1:
            return json.dumps(return_success('ok'), cls=DecimalEncoder)
        else:
            return json.dumps(return_unsuccess('添加应付失败'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('添加应付失败: ' + str(e)), ensure_ascii=False)


@app.route('/queryPurchasePay', methods=['POST'])
def queryPurchasePay():
    _json = request.json
    print(_json)
    _purchaseId = _json.get('purchaseId')
    _days = _json.get('days')
    try:
        res = addPayRemain(_purchaseId, _days)
        if res:
            return json.dumps(return_success(res),
                              cls=DecimalEncoder, ensure_ascii=False)
        else:
            return json.dumps(return_unsuccess('未查询到相关数据'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('Query Error: ' + str(e)))


@app.route('/addSellReceive', methods=['POST'])
def addSellReceive():
    _json = request.json
    _id = _json.get('sellId')
    _reason = _json.get('reason')
    try:
        arap = ARAPDao()
        row = arap.add_sell_receive(_id, _reason)
        if row == 1:
            return json.dumps(return_success('ok'), cls=DecimalEncoder)
        else:
            return json.dumps(return_unsuccess('添加应收失败'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('添加应收失败: ' + str(e)), ensure_ascii=False)


@app.route('/querySellReceive', methods=['POST'])
def querySellReceive():
    _json = request.json
    print(_json)
    _id = _json.get('sellId')
    _days = _json.get('days')
    try:
        res = addReceiveRemain(_id, _days)
        if res:
            return json.dumps(return_success(res),
                              cls=DecimalEncoder, ensure_ascii=False)
        else:
            return json.dumps(return_unsuccess("No related data"))
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('Query Error: ' + str(e)))


@app.route('/addPayment', methods=['POST'])
def addPayment():
    _json = request.json
    _id = _json.get('purchaseId')
    _amount = _json.get('amount')
    _date = _json.get('date')
    try:
        arap = ARAPDao()
        res = arap.add_payment(_id, _amount, _date)
        if res['row'] == 1:
            return json.dumps(return_success({'paymentId': res['id']}), cls=DecimalEncoder)
        else:
            return json.dumps(return_unsuccess('添加支出失败'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('添加支出失败: ' + str(e)), ensure_ascii=False)


@app.route('/queryPayment', methods=['POST'])
def queryPayment():
    _json = request.json
    _id = _json.get('purchaseId')
    _days = _json.get('days')
    try:
        arap = ARAPDao()
        res = arap.query_payment(_id, _days)
        return json.dumps(return_success(ARAPDao.to_pay_dict(res)),
                          cls=DecimalEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('Query Error: ' + str(e)))


@app.route('/addReceive', methods=['POST'])
def addReceive():
    _json = request.json
    _id = _json.get('sellId')
    _amount = _json.get('amount')
    _date = _json.get('date')
    try:
        arap = ARAPDao()
        res = arap.add_receive(_id, _amount, _date)
        if res['row'] == 1:
            return json.dumps(return_success({'receiveId': res['id']}), cls=DecimalEncoder)
        else:
            return json.dumps(return_unsuccess('添加收入失败'), ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('添加收入失败: ' + str(e)), ensure_ascii=False)


@app.route('/queryReceive', methods=['POST'])
def queryReceive():
    _json = request.json
    _id = _json.get('sellId')
    _days = _json.get('days')
    try:
        arap = ARAPDao()
        res = arap.query_receive(_id, _days)
        return json.dumps(return_success(ARAPDao.to_receive_dict(res)),
                          cls=DecimalEncoder, ensure_ascii=False)
    except Exception as e:
        print(e)
        return json.dumps(return_unsuccess('Query Error: ' + str(e)))


if __name__ == '__main__':
    app.run()
