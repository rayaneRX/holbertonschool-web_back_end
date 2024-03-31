// 5-payment.test.js
const sinon = require('sinon');
const assert = require('assert');
const sendPaymentRequestToApi = require('./5-payment');
const Utils = require('./utils');

describe('sendPaymentRequestToApi', function() {
  let calculateNumberStub;
  let consoleLogSpy;

  beforeEach(function() {
    calculateNumberStub = sinon.stub(Utils, 'calculateNumber').returns(10);
    consoleLogSpy = sinon.spy(console, 'log');
  });

  afterEach(function() {
    calculateNumberStub.restore();
    consoleLogSpy.restore();
  });

  it('should call Utils.calculateNumber and log the result correctly for totalAmount 100 and totalShipping 20', function() {
    sendPaymentRequestToApi(100, 20);

    assert(calculateNumberStub.calledOnceWithExactly('SUM', 100, 20));
    assert(consoleLogSpy.calledOnceWithExactly('The total is: 10'));
  });

  it('should call Utils.calculateNumber and log the result correctly for totalAmount 10 and totalShipping 10', function() {
    sendPaymentRequestToApi(10, 10);

    assert(calculateNumberStub.calledOnceWithExactly('SUM', 10, 10));
    assert(consoleLogSpy.calledOnceWithExactly('The total is: 10'));
  });
});
