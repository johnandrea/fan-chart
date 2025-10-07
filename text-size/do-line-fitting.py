import sys

page_width = 250
page_height = 7100
margin = 15

plot_width = page_width - 2 * margin
plot_height = 75
plot_inc = 2 * margin

def svg_header():
    print( '<?xml version="1.0" standalone="no"?>' )
    print( '<svg width="' + str(page_width) + 'pt" height="' + str(page_height) + 'pt"' )
    print( ' viewBox="0.00 0.00 ' + str(page_width) + '.00 ' + str(page_height) + '.00"' )
    print( ' version="1.1"' )
    print( ' xmlns="http://www.w3.org/2000/svg"' )
    print( ' xmlns:xlink="http://www.w3.org/1999/xlink">' )

def svg_trailer():
    print( '</svg>' )

def round2( x ):
    return str( round( x, 2 ) )

def round4( x ):
    return str( round( x, 4 ) )


def show_colour_text( x, y, f, c, s ):
    print( '<text font-size="' + round2(f) + '" font-family="Times New Roman,serif"' )
    print( ' x="' + round2(x) + '" y="' + round2(y) + '" fill="'+ c +'">' + s + '</text>' )

def x_axis_tic( x, s ):
    show_colour_text( x, plot_height-2, 6, 'green', s.replace('.0', '') )

def show_info( y, s, c ):
    f = 10
    show_colour_text( 3, y, f, c, s )
    return y + f + 2

def dot( x, y ):
    print( '<circle cx="' + round2(x) + '" cy="' + round2(y) + '"' )
    print( ' fill="green" stroke="green" r="2" />' )


def show_line( graph_origin_x, graph_origin_y, name, x, y, line_data ):
    slope = line_data[0]
    y_int = line_data[1]

    print( '<g transform="translate(' + round2(graph_origin_x) + ',' + round2(graph_origin_y) + ')">' )
    pos_y = 10
    colour = 'black'
    pos_y = show_info( pos_y, 'char: ' + name, colour )
    pos_y = show_info( pos_y, 'slope: ' + round4( slope ), colour )
    pos_y = show_info( pos_y, 'y int: ' + round4( y_int ), colour )
    if ( line_data[3] ):
       colour = 'red'
    pos_y = show_info( pos_y, 'R^2: ' + round4( line_data[2] ) +' '+ line_data[3], colour )

    min_x = 0
    max_x = max( x )
    min_y = 0
    max_y = max( y )

    x_axis_factor = plot_width / ( max_x - min_x )
    y_axis_factor = plot_height / ( max_y - min_y )

    # show the points
    for i in range( len(x) ):
        pos_x = x_axis_factor * ( x[i] - min_x )          
        pos_y = y_axis_factor * ( y[i] - min_y )
        # show y towards top
        dot( pos_x, 0 - pos_y + plot_height )

    # show the fit line
    pos_x_1 = x_axis_factor * ( 0.0 - min_x )
    pos_y_1 = y_axis_factor * ( y_int - min_y )
    pos_x_2 = x_axis_factor * ( max_x - min_x )
    pos_y_2 = y_axis_factor * ( (y_int + slope * max_x) - min_y )
    pos_1 = round2(pos_x_1) +','+ round2(0 - pos_y_1 + plot_height )
    pos_2 = round2(pos_x_2) +','+ round2(0 - pos_y_2 + plot_height )

    print( '<path d="M' + pos_1 + ' ' + pos_2 + '" style="stroke:blue;" />' )

    # x-axis
    pos_1 = '0,' + round2(plot_height)
    pos_2 = round2(plot_width) + ',' + round2(plot_height)
    print( '<path d="M' + pos_1 + ' ' + pos_2 + '" style="stroke:green;" />' )
    # axis label
    pos_x_1 = plot_width / 2
    pos_y_1 = plot_height + 6
    show_colour_text( pos_x_1, pos_y_1, 6, 'green', 'font size' )
    # tics
    for i in range( len(x) ):
        pos = x_axis_factor * ( x[i] - min_x ) 
        x_axis_tic( pos, round2(x[i] ) )

    # y-axis
    #pos_1 same
    pos_2 = '0,0'
    print( '<path d="M' + pos_1 + ' ' + pos_2 + '" style="stroke:green;" />' )
    # axis label
    pos_x_1 = -5
    pos_y_1 = 10
    for c in 'points':
        show_colour_text( pos_x_1, pos_y_1, 7, 'green', c )
        pos_y_1 += 7
 
    print( '</g>' )


def do_calc( name, n, x, y ):
    print( '', file=sys.stderr )
    print( name, file=sys.stderr )
    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    sum_x2 = 0.0
    for i in range( len(x) ):
        #print( name, x[i], y[i] )
        sum_x += x[i]
        sum_y += y[i]
        sum_xy += x[i] * y[i]
        sum_x2 += x[i] * x[i]

    denom = n * sum_xy - sum_x * sum_y
    numer = n * sum_x2 - sum_x * sum_x
    slope = denom / numer
    y_int = ( sum_y - slope * sum_x ) / n
    print( 'slope', slope, file=sys.stderr )
    print( 'y int', y_int, file=sys.stderr )

    #mean_x = sum_x / n
    mean_y = sum_y / n
    sst = 0.0
    ssr = 0.0
    for i in range( len(y) ):
        d = y[i] - mean_y
        sst += d * d
        y_hat = y_int + slope * x[i]
        d = y_hat - mean_y
        ssr += d * d
    r2 = ssr / sst
    warning = ''
    if r2 < 0.98:
       warning += '!'
    if r2 < 0.91:
       warning += '!'
    if r2 < 0.8:
       warning += '!'
    print( 'R^2', ssr / sst, warning, file=sys.stderr )
    return [ slope, y_int, r2, warning ]

# input file:
#    #char font-size number-chars width
#    a 9 22 90
#    a 12 22 120
#    a 20 20 180
#...


svg_header()

prev = None
n = 0
x = []
y = []

plot_y = margin

for line in sys.stdin:
    line = line.strip()
    if not line.startswith( '#' ):
       parts = line.split()
       if len(parts) == 4:
          if parts[0] != prev:
             if prev:
                results = do_calc( prev, n, x, y )
                show_line( margin, plot_y, prev, x, y, results )
                # start next item
                plot_y += plot_height + plot_inc
                x = []
                y = []
                n = 0
          prev = parts[0]
          n += 1
          x.append( float(parts[1]) )
          y.append( float(parts[3]) / float(parts[2]) )
       else:
          print( 'wrong items', line, file=sys.stderr )

if prev:
   results = do_calc( prev, n, x, y )
   show_line( margin, plot_y, prev, x, y, results )

svg_trailer()