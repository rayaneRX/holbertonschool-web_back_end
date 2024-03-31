// api.test.js
const request = require('supertest');
const app = require('./api');
const { expect } = require('chai');

describe('Cart page', () => {
  it('Correct status code when :id is a number', (done) => {
    request(app)
      .get('/cart/12')
      .expect(200, done);
  });

  it('Correct result when :id is a number', (done) => {
    request(app)
      .get('/cart/12')
      .expect('Payment methods for cart 12', done);
  });

  it('Correct status code when :id is NOT a number (=> 404)', (done) => {
    request(app)
      .get('/cart/hello')
      .expect(404, done);
  });

  it('Correct error message when :id is NOT a number (=> 404)', (done) => {
    request(app)
      .get('/cart/hello')
      .expect('Cannot GET /cart/hello', done);
  });
});
