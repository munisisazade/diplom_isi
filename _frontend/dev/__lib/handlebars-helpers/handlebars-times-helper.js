/**
 * Created by Labrin on 1/12/17.
 */

module.exports.register = function (Handlebars, options, params)  {
    Handlebars.registerHelper( 'times', function( n, block ) {
        var accum = '',
            i = -1;
        while( ++i < n ) {
            accum += block.fn( i );
        }
        return accum;
    });
};
