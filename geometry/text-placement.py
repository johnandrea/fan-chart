import math

# simply show how to place text in slices

# margin in percentages of pixels for text within a slice
# this example is too large - just for demonstration
text_margin = 12

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
    # remind me of the grid directions
    plain_text( x - 10, y - 2, 10, 'x &#8594;' )
    plain_text( x - 10, y + 11, 10, 'y &#8595;' )

def draw_slice( inner, outer, d ):
    # compute corners of the slice
    # and return those values
    #
    # if it were centered along the x-axis
    # p1 = upper-left, p2 = lower-left
    # p3 = lower-right, p4 = upper-right

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

    # indexes: x, y, combined
    # p1 = 0: 0, 1, 2
    # p2 = 1: 0, 1, 2
    # p3 = 2: 0, 1, 2
    # p4 = 3: 0, 1, 2

    return [ [p1_x, p1_y, p1], [p2_x, p2_y, p2], [p3_x, p3_y, p3], [p4_x, p4_y, p4] ]

def text_on_path( path, path_id ):
    text = 'Full name'
    font_size = 15
    font_options = ' font-size="' + roundstr(font_size) + '"'
    font_options += ' font-family="Times New Roman,serif"'

    print( '<path id="' + path_id + '" d="' + path + '" style="fill:none;" />' )
    print( '<text ' + font_options + '>' )
    print( ' <textPath xlink:href="#' + path_id + '" startOffset="0%">' + text + '</textPath>' )
    print( '</text>' )

def debug_margin_dots( coords ):
    for i in [0,1,2,3]:
        print( '<circle cx="' + roundstr(coords[i][0]) + '" cy="' + roundstr(coords[i][1]) + '"' )
        print( ' fill="none" stroke="red" r="2" />' )

def horizontal_name( p3_list, p4_list ):
    path = 'M' + p3_list[2] + ' L' + p4_list[2]
    text_on_path( path, 'hpath1' )

def vertical_name( p2_list, p3_list ):
    path = 'M' + p2_list[2] + ' L' + p3_list[2]
    text_on_path( path, 'vpath2' )

def horizontal_name_base( p3_list, p4_list ):
    draw_line( p3_list[0], p3_list[1], p4_list[0], p4_list[1] )

def vertical_name_base( p2_list, p3_list ):
    draw_line( p2_list[0], p2_list[1], p3_list[0], p3_list[1] )

def add_text_margins( coords ):
    # same return format as the input slice coordinates
    results = []

    # exact copy
    #for i in [0,1,2,3]:
    #    x = coords[i][0]
    #    y = coords[i][1]
    #    both = coords[i][2]
    #    results.append( [x,y,both] )

    p1_x = coords[0][0]
    p1_y = coords[0][1]
    p2_x = coords[1][0]
    p2_y = coords[1][1]
    p3_x = coords[2][0]
    p3_y = coords[2][1]
    p4_x = coords[3][0]
    p4_y = coords[3][1]

    # essentially, shrink the corners of the slice
    # but this does mean treating the slice as a box rather than circle sector
    # so account for the inner and outer lengths with two lengths

    x_len = abs( p1_x - p4_x )
    y_len1 = abs( p1_y - p2_y )
    y_len2 = abs( p3_y - p4_y )

    x_diff = text_margin * x_len / 100.0
    y_diff1 = text_margin * y_len1 / 100.0
    y_diff2 = text_margin * y_len2 / 100.0

    p1_x += x_diff
    p2_x += x_diff
    p3_x -= x_diff
    p4_x -= x_diff
    p1_y += y_diff1
    p2_y -= y_diff1
    p3_y -= y_diff2
    p4_y += y_diff2

    results.append( [p1_x, p1_y, roundstr(p1_x) + ',' + roundstr(p1_y)] )
    results.append( [p2_x, p2_y, roundstr(p2_x) + ',' + roundstr(p2_y)] )
    results.append( [p3_x, p3_y, roundstr(p3_x) + ',' + roundstr(p3_y)] )
    results.append( [p4_x, p4_y, roundstr(p4_x) + ',' + roundstr(p4_y)] )

    return results

def slice_with_horizontal_name( x, y, inner, outer, slice_angle, rotate ):
    center = roundstr(x) + ',' + roundstr(y)
    print( '<g transform="translate(' + center + ')">' )
    print( '<g transform="rotate(' + str(rotate) + ')">' )
    slice_coords = draw_slice( inner, outer, slice_angle )
    coords = add_text_margins( slice_coords )
    debug_margin_dots( coords )
    horizontal_name_base( coords[2], coords[3] )
    horizontal_name( coords[2], coords[3] )
    print( '</g>' )
    print( '</g>' )

def slice_with_vertical_name( x, y, inner, outer, slice_angle, rotate ):
    center = roundstr(x) + ',' + roundstr(y)
    print( '<g transform="translate(' + center + ')">' )
    print( '<g transform="rotate(' + str(rotate) + ')">' )
    slice_coords = draw_slice( inner, outer, slice_angle )
    coords = add_text_margins( slice_coords )
    debug_margin_dots( coords )
    vertical_name_base( coords[1], coords[2] )
    vertical_name( coords[1], coords[2] )
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
