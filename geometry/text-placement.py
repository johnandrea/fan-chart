import math

# simply show how to place text in slices

def roundstr( x ):
    # output of 2 digits ought to be enough
    return str( round( x, 2 ) )

def output_header( w, h ):
    print( '<?xml version="1.0" standalone="no"?>' )
    print( '<svg width="' + str(w) + 'pt" height="' + str(h) + 'pt"' )
    print( ' viewBox="0.00 0.00 ' + str(w) + '.00 ' + str(h) + '.00"' )
    print( ' version="1.1"' )
    print( ' xmlns="http://www.w3.org/2000/svg"' )
    print( ' xmlns:xlink="http://www.w3.org/1999/xlink">' )

def output_trailer():
    print( '</svg>' )

def draw_circle( x, y, radius ):
    print( '<circle cx="' + roundstr(x) + '" cy="' + roundstr(y) + '"' )
    print( ' fill="none" stroke="grey" r="' + roundstr(radius) + '" />' )

def draw_line( a, b, x, y ):
    start = roundstr(a) + ',' + roundstr(b)
    end = roundstr(x) + ',' + roundstr(y)
    print( '<path d="M' + start + ' ' + end + '" style="stroke:blue;" />' )

def draw_zero_line( x, y, size ):
    draw_line( x, y, x+size, y )

def plain_text( x, y, size, s ):
    # need to escape characters in the text
    print( '<text font-size="' + roundstr(size) + '" font-family="Times New Roman,serif"' )
    print( ' x="' + roundstr(x) + '" y="' + roundstr(y) + '">' + s + '</text>' )

def draw_labels( x, y ):
    # remind me of the directions
    plain_text( x - 10, y - 2, 10, 'x &#8594;' )
    plain_text( x - 10, y + 11, 10, 'y &#8595;' )

def draw_sector( inner, outer, d ):
    half_d = math.radians( d/2.0 )
    p1_x = inner * math.cos(half_d)
    p1_y = - inner * math.sin(half_d)
    p1 = roundstr(p1_x) + ',' + roundstr(p1_y)

    p2_x = p1_x
    p2_y = - p1_y
    p2 = roundstr(p2_x) + ',' + roundstr(p2_y)

    p3_x = outer * math.cos(half_d)
    p3_y = outer * math.sin(half_d)
    p3 = roundstr(p3_x) + ',' + roundstr(p3_y)

    p4_x = p3_x
    p4_y = - p3_y
    p4 = roundstr(p4_x) + ',' + roundstr(p4_y)

    print( '<path style="stroke:grey; fill:lightgreen;"' )
    print( 'd="M' + p1 )
    r = roundstr(inner) + ',' + roundstr(inner)
    print( 'A' + r + ' 0 0 1 ' + p2 )
    print( 'L' + p3 )
    r = roundstr(outer) + ',' + roundstr(outer)
    print( 'A' + r + ' 0 0 0 ' + p4 )
    print( 'z" />' )

def horizontal_name_base( outer, d ):
    half_d = math.radians( d/2.0 )

    p3_x = outer * math.cos(half_d)
    p3_y = outer * math.sin(half_d)

    p4_x = p3_x
    p4_y = - p3_y

    draw_line( p3_x, p3_y, p4_x, p4_y )

def vertical_name_base( inner, outer, d ):
    half_d = math.radians( d/2.0 )
    p1_x = inner * math.cos(half_d)
    p1_y = - inner * math.sin(half_d)

    p2_x = p1_x
    p2_y = - p1_y

    p3_x = outer * math.cos(half_d)
    p3_y = outer * math.sin(half_d)

    draw_line( p2_x, p2_y, p3_x, p3_y )

def slice_with_horizontal_name( x, y, inner, outer, slice_angle, rotate ):
    center = roundstr(x) + ',' + roundstr(y)
    print( '<g transform="translate(' + center + ')">' )
    print( '<g transform="rotate(' + str(rotate) + ')">' )
    draw_sector( inner, outer, slice_angle )
    horizontal_name_base( outer, slice_angle )
    print( '</g>' )
    print( '</g>' )

def slice_with_vertical_name( x, y, inner, outer, slice_angle, rotate ):
    center = roundstr(x) + ',' + roundstr(y)
    print( '<g transform="translate(' + center + ')">' )
    print( '<g transform="rotate(' + str(rotate) + ')">' )
    draw_sector( inner, outer, slice_angle )
    vertical_name_base( inner, outer, slice_angle )
    print( '</g>' )
    print( '</g>' )

# center of large circle
cx = 200
cy = 200

# radius of slices
inner = 100
outer = 180

output_header( 450, 400 )

draw_zero_line( cx, cy, outer + 50 )
draw_circle( cx, cy, outer )
draw_circle( cx, cy, inner )
draw_labels( cx, cy )

slice_with_horizontal_name( cx, cy, inner, outer, 24, -40 )
slice_with_vertical_name( cx, cy, inner, outer, 15, 18 )

output_trailer()
