// api.test.js
const request = require('supertest');
const app = require('./api');
const { expect } = require('chai');

describe('Index page', () => {
  it('Correct status code', (done) => {
    request(app)
      .get('/')
      .expect(200, done);
  });

  it('Correct result', (done) => {
    request(app)
      .get('/')
      .expect('Welcome to the payment system', done);
  });
});
