// 2-calcul_chai.test.js
const chai = require('chai');
const calculateNumber = require('./2-calcul_chai.js');

const { expect } = chai;

describe('calculateNumber', function() {
  describe('SUM operation', function() {
    it('should return the sum of rounded numbers', function() {
      expect(calculateNumber('SUM', 1.4, 4.5)).to.equal(6);
    });
  });

  describe('SUBTRACT operation', function() {
    it('should return the subtraction of rounded numbers', function() {
      expect(calculateNumber('SUBTRACT', 1.4, 4.5)).to.equal(-4);
    });
  });

  describe('DIVIDE operation', function() {
    it('should return the division of rounded numbers', function() {
      expect(calculateNumber('DIVIDE', 1.4, 4.5)).to.equal(0.2);
    });

    it('should return "Error" if the second argument is rounded to 0', function() {
      expect(calculateNumber('DIVIDE', 1.4, 0)).to.equal('Error');
    });
  });
});
