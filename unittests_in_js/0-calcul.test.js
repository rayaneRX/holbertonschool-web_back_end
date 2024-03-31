const assert = require('assert');
const calculateNumber = require('./0-calcul');

describe('calculateNumber', function() {
  it('Return the correct sum of 2 positive integers', () => {
    assert.equal(calculateNumber(1, 3), 4);
    assert.equal(calculateNumber(5, 3), 8);
  }),
  it('Return the correct sum when 1 argument is a float', () => {
    assert.equal(calculateNumber(1, 3.7), 5);
    assert.equal(calculateNumber(3.7, 2), 6);
  }),
  it('Return the correct sum when both arguments are floats', () => {
    assert.equal(calculateNumber(1.5, 3.7), 6);
    assert.equal(calculateNumber(1.2, 3.7), 5);
  }),
  it('Return the correct sum of 2 negative integers', () => {
    assert.equal(calculateNumber(-1, -3), -4);
    assert.equal(calculateNumber(-5, -3), -8);
  }),
  it('Return the correct sum when 1 argument is positive and the other is negative', () => {
    assert.equal(calculateNumber(1, -3), -2);
    assert.equal(calculateNumber(-1, 3), 2);
  }),
  it('Throw an error if non-numeric values are provided', () => {
    assert.throws(() => calculateNumber("a", 2), Error);
    assert.throws(() => calculateNumber(2, "b"), Error);
    assert.throws(() => calculateNumber("a", "b"), Error);
  })
});