var gulp = require('gulp');
var postcss      = require('gulp-postcss');
var sourcemaps   = require('gulp-sourcemaps');
var autoprefixer = require('autoprefixer');
var scss         = require('gulp-scss');
var livescript   = require('gulp-livescript');
var watch = require('gulp-watch');

gulp.task('css', function () {
    return gulp.src('src/*.scss')
        .pipe(sourcemaps.init())
        .pipe(scss())
        .pipe(postcss([ autoprefixer({ browsers: ['last 2 versions'] }) ]))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('dist'));
});

gulp.task('livescript', function() {
  return gulp.src('src/*.ls')
    .pipe(sourcemaps.init())
    .pipe(livescript({bare: true}))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('dist/'));
});

gulp.task('watch', function(){
  gulp.watch('src/*.scss', ['css']);
  gulp.watch('src/*.ls', ['livescript']);
})

gulp.task('default', ['css', 'livescript', 'watch']);