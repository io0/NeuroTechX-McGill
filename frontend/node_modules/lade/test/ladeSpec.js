/* global beforeEach, describe, it, expect, spyOn, lade */
describe('lade', function () {
  var obj

  beforeEach(function () {
    obj = {}
  })

  itWorks('with primitive initial value', {
    value:  'initial',
    result: 'initial'
  })
  
  itWorks('with function as initial value', {
    value:  function () { return 'initial' },
    result: 'initial'
  })

  describe('function as a value', function () {
    var callCount

    beforeEach(function () {
      callCount = 0
    })

    beforeEach(function () {
      lade(obj, 'prop', function () {
        callCount++
        return 'initial'
      })
    })

    it('is called on property read', function () {
      obj.prop
      expect(callCount).toBe(1)
    })

    it('is not called twice', function () {
      obj.prop
      obj.prop
      expect(callCount).toBe(1)
    })

    it('is not called without property read', function () {
      expect(callCount).toBe(0)
    })

    it('is not called on property write', function () {
      obj.prop = 'changed'
      expect(callCount).toBe(0)
    })
  })

  function itWorks (msg, options) {
    var subject

    describe(msg, function () {
      beforeEach(function () {
        subject = lade(obj, 'prop', options.value)
      })

      it('defines property', function () {
        expect(obj.hasOwnProperty('prop')).toBe(true)
      })

      it('returns original object', function () {
        expect(subject).toBe(obj)
      })

      describe('property', function() {
        it('has correct value', function () {
          expect(obj.prop).toBe(options.result)
        })

        it('can be changed to primitive value', function () {
          obj.prop = 'changed'
          expect(obj.prop).toBe('changed')
        })

        it('can be changed to function value', function () {
          var noop = function () {}
          obj.prop = noop
          expect(obj.prop).toBe(noop)
        })

        it('can be changed after read', function () {
          obj.prop
          obj.prop = 'changed'
          expect(obj.prop).toBe('changed')
        })
      })
    })
  }
})
