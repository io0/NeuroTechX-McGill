# karma-jasmine-def
[![npm version](https://img.shields.io/npm/v/karma-jasmine-def.svg)](https://www.npmjs.com/package/karma-jasmine-def)
[![Build Status](https://img.shields.io/travis/vlazar/karma-jasmine-def.svg)](https://travis-ci.org/vlazar/karma-jasmine-def)
[![Code Climate](https://img.shields.io/codeclimate/github/vlazar/karma-jasmine-def.svg)](https://codeclimate.com/github/vlazar/karma-jasmine-def)
[![Test Coverage](https://img.shields.io/codeclimate/coverage/github/vlazar/karma-jasmine-def.svg)](https://codeclimate.com/github/vlazar/karma-jasmine-def/coverage)
[![devDependencies Status](https://img.shields.io/david/dev/vlazar/karma-jasmine-def.svg)](https://david-dm.org/vlazar/karma-jasmine-def#info=devDependencies)
[![js-standard-style](https://img.shields.io/badge/code%20style-standard-brightgreen.svg)](https://github.com/feross/standard)

Adds ```def``` and ```subject``` functions - a better way to setup Jasmine test subjects.

## Usage

### Install

```
npm install karma-jasmine karma-jasmine-def --save-dev
```

### Configure Karma

```javascript
module.exports = function(config) {
  config.set({
    frameworks: ['jasmine', 'jasmine-def']
  });
};
```

### Write specs

```javascript
describe('a cleaner spec with lazy test subjects', function () {
  subject(function () {
    return new SomeObject(this.options);
  });

  def('options', function () {
    return { foo: 'foo' };
  });

  it('works', function () {
    expect(this.options).toBeDefined();
    expect(this.subject).toBeDefined();
  });
});
```
