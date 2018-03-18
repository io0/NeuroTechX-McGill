# jasmine-def
[![npm version](https://img.shields.io/npm/v/jasmine-def.svg)](https://www.npmjs.com/package/jasmine-def)
[![Build Status](https://img.shields.io/travis/vlazar/jasmine-def.svg)](https://travis-ci.org/vlazar/jasmine-def)
[![Code Climate](https://img.shields.io/codeclimate/github/vlazar/jasmine-def.svg)](https://codeclimate.com/github/vlazar/jasmine-def)
[![Test Coverage](https://img.shields.io/codeclimate/coverage/github/vlazar/jasmine-def.svg)](https://codeclimate.com/github/vlazar/jasmine-def/coverage)
[![devDependencies Status](https://img.shields.io/david/dev/vlazar/jasmine-def.svg)](https://david-dm.org/vlazar/jasmine-def#info=devDependencies)
[![js-standard-style](https://img.shields.io/badge/code%20style-standard-brightgreen.svg)](https://github.com/feross/standard)

Define lazily evaluated test data via ```def()``` and ```subject()``` functions.

## Usage

### Without jasmine-def

```javascript
describe('old spec', function () {

  // order is important, options must be defined before subject
  beforeEach(function () {
    this.options = { foo: 'foo' };
  });

  beforeEach(function () {
    this.subject = new SomeObject(this.options)
  });

  it('works', function () {
    expect(this.options).toBeDefined();
    expect(this.subject).toBeDefined();
  });
});
```

### With jasmine-def

```javascript
describe('new shiny spec', function () {

  // order is not important, defined properties are lazy evaluated
  subject(function () {
    return new SomeObject(this.options)
  });

  def('options', function () {
    return { foo: 'foo' }
  });

  it('works', function () {
    expect(this.options).toBeDefined();
    expect(this.subject).toBeDefined();
  });
});
```
