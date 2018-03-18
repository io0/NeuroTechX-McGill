module.exports = function(config) {
  config.set({
    frameworks: ['jasmine'],
    files: [
      'lib/**/*.js',
      'test/**/*Spec.js'
    ],
    browsers: process.env.TRAVIS ? ['ChromeTravisCI'] : ['Chrome'],
    customLaunchers: {
      ChromeTravisCI: {
        base: 'Chrome',
        flags: ['--no-sandbox']
      }
    },
    reporters: ['progress', 'coverage'],
    coverageReporter: {
      type: 'lcov',
      subdir: '.'
    },
    preprocessors: {
      'lib/**/*.js': ['coverage']
    },
    port: 9876,
    colors: true,
    logLevel: config.LOG_INFO,
    autoWatch: true,
    singleRun: false
  });
};
