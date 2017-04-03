var clean_css = require('gulp-clean-css'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    path = require('path'),
    rename = require('gulp-rename'),
    sass = require('gulp-sass'),
    sourcemaps = require('gulp-sourcemaps'),
    uglify = require('gulp-uglify');

function css_task () {
  var outfile = path.join('blackbook', 'static', 'css', 'blackbook.min.css'),
      clean_css_opts = {
        compatibility: ''
      },
      sass_opts = {
        outFile: outfile,
        sourceMap: true
      };

  return gulp.src(path.join('blackbook', 'static', 'css', 'src', 'blackbook.scss'))
    .pipe(sourcemaps.init())
    .pipe(sass(sass_opts).on('error', sass.logError))
    .pipe(clean_css(clean_css_opts))
    .pipe(rename('blackbook.min.css'))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(path.join('blackbook', 'static', 'css')));
}

function js_task (srcpath, destpath, filename, uglify_opts) {

  if (uglify_opts === undefined) {
      uglify_opts = {};
  }

  return gulp.src(srcpath)
    .pipe(sourcemaps.init())
    .pipe(concat(filename))
    .pipe(uglify(uglify_opts))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(destpath));
}

function blackbook_js_task () {

  return js_task(
      path.join('blackbook', 'static', 'js', 'src', 'blackbook*.js'),
      path.join('blackbook', 'static', 'js'),
      'blackbook.min.js'
  );

}

function collection_json_task () {

  return js_task(
      path.join('blackbook', 'static', 'js', 'src', 'collection_json.js'),
      path.join('blackbook', 'static', 'js'),
      'collection_json.min.js'
  );

}

gulp.task('css', css_task);
gulp.task('blackbook-js', blackbook_js_task);
gulp.task('collection-json-js', collection_json_task);

gulp.task('default', ['css', 'blackbook-js', 'collection-json-js']);