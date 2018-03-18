/* global beforeEach, describe, it, expect, spyOn, def, subject */
describe('integration with jasmine', function () {
  describe('global', function () {
    it('is extended with def ()', function () {
      expect(typeof def).toBe('function')
    })

    it('is extended with subject ()', function () {
      expect(typeof subject).toBe('function')
    })
  })
})

describe('integration with lade', function () {
  beforeEach(function () {
    this.spy = spyOn(window, 'lade')
  })

  describe('def(prop, value)', function () {
    def('prop', 1)

    it('defines property with lade', function () {
      expect(this.spy).toHaveBeenCalledWith(this, 'prop', 1)
    })
  })

  describe('subject(value)', function () {
    subject(42)

    it('defines subject with lade', function () {
      expect(this.spy).toHaveBeenCalledWith(this, 'subject', 42)
    })
  })
})
