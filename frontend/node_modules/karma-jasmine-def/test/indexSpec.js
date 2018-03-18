/* global describe, it, expect, def, subject */
describe('karma-jasmine', function () {
  it('is extended with def ()', function () {
    expect(typeof def).toBe('function')
  })

  it('is extended with subject ()', function () {
    expect(typeof subject).toBe('function')
  })
})
