var gulp        = require('gulp'),
    $           = require('gulp-load-plugins')(),
    path        = require('path'),
    browserSync = require('browser-sync'),
    through2    = require('through2'),
    reload      = browserSync.reload,
    browserify  = require('browserify'),
    del         = require('del'),
    argv        = require('yargs').argv;

gulp.task('browser-sync', function() {
  browserSync({
    open: !!argv.open,
    notify: !!argv.notify,
    server: {
      baseDir: "./dist"
    }
  });
});

gulp.task('compass', function() {
  return gulp.src('src/stylesheets/**/*.{scss,sass}')
    .pipe($.plumber())
    .pipe($.compass({
      css: 'dist/stylesheets',
      sass: 'src/stylesheets'
    }))
    .pipe(gulp.dest('dist/stylesheets'));
});

gulp.task('css', function() {
  return gulp.src([
    'node_modules/ion-rangeslider/css/ion.rangeSlider.css',
    'node_modules/ion-rangeslider/css/ion.rangeSlider.skinFlat.css'
  ]).pipe($.plumber())
    .pipe(gulp.dest('dist/stylesheets'));
});

gulp.task('js', function() {
  return gulp.src('src/scripts/main.js')
    .pipe($.plumber())
    .pipe(through2.obj(function (file, enc, next) {
      browserify(file.path, { debug: true })
        .transform(require('babelify'))
        .transform(require('debowerify'))
        .bundle(function (err, res) {
          if (err) { return next(err); }
          file.contents = res;
            next(null, file);
        });
      }))
      .on('error', function (error) {
        console.log(error.stack);
        this.emit('end')
    })
  .pipe( $.rename('app.js'))
  .pipe( gulp.dest('dist/scripts/'));
});

gulp.task('legacyjs', function() {
  return gulp.src('src/scripts/cola.v3.js')
    .pipe(gulp.dest('dist/scripts/'));
});


gulp.task('clean', function(cb) {
  del('./dist', cb);
});

gulp.task('images', function() {
  return gulp.src([
      'src/images/**/*',
      'node_modules/ion-rangeslider/img/sprite-skin-flat.png'
    ]).pipe($.imagemin({
      progressive: true
    }))
    .pipe(gulp.dest('./dist/img'))
})

gulp.task('templates', function() {
  return gulp.src('src/**/*.html')
    .pipe($.plumber())
    .pipe( gulp.dest('dist/') )
});



gulp.task('build', ['css', 'compass', 'js', 'legacyjs', 'templates', 'images']);

gulp.task('serve', ['build', 'browser-sync'], function () {
  gulp.watch('src/stylesheets/**/*.{scss,sass}',['compass', reload]);
  gulp.watch('node_modules/**/*.{css}',['css', reload]);
  gulp.watch('src/scripts/**/*.js',['js', reload]);
  gulp.watch([
    'src/images/**/*',
    'node_modules/**/*.png'
  ],['images', reload]);
  gulp.watch('src/*.html',['templates', reload]);
});

gulp.task('default', ['serve']);
