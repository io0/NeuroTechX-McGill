# lade
[![npm version](https://img.shields.io/npm/v/lade.svg)](https://www.npmjs.com/package/lade)
[![Build Status](https://img.shields.io/travis/vlazar/lade.svg)](https://travis-ci.org/vlazar/lade)
[![Code Climate](https://img.shields.io/codeclimate/github/vlazar/lade.svg)](https://codeclimate.com/github/vlazar/lade)
[![Test Coverage](https://img.shields.io/codeclimate/coverage/github/vlazar/lade.svg)](https://codeclimate.com/github/vlazar/lade/coverage)
[![devDependencies Status](https://img.shields.io/david/dev/vlazar/lade.svg)](https://david-dm.org/vlazar/lade#info=devDependencies)
[![js-standard-style](https://img.shields.io/badge/code%20style-standard-brightgreen.svg)](https://github.com/feross/standard)

Defines object properties evaluated and cached on the first read.

## Usage

### Define lazy property

```javascript
var obj = {};

lade(obj, 'lazy', function() { return 40 + 2 });

obj.lazy;     // 42 (calls function, returns result as property value)
obj.lazy;     // 42 (uses cached property value from now on)

obj.lazy = 0; // overwrite property value
obj.lazy;     // 0
```

### Define plain property

```javascript
var obj = {};

lade(obj, 'prop', 'yes');

obj.prop;        // 'yes'

obj.prop = 'no'; // overwrite property value
obj.prop;        // 'no'
```
