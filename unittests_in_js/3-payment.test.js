// 3-payment.test.js
const sinon = require('sinon');
const assert = require('assert');
const sendPaymentRequestToApi = require('./3-payment');
const Utils = require('./utils');

describe('sendPaymentRequestToApi', function() {
  it('should call Utils.calculateNumber with correct arguments and log the result', function() {
    const calculateNumberStub = sinon.stub(Utils, 'calculateNumber').returns(10);
    const consoleLogSpy = sinon.spy(console, 'log');

    sendPaymentRequestToApi(100, 20);

    assert(calculateNumberStub.calledOnceWithExactly('SUM', 100, 20));
    assert(consoleLogSpy.calledOnceWithExactly('The total is: 10'));

    // Restore stub and spy
    calculateNumberStub.restore();
    consoleLogSpy.restore();
  });
});
