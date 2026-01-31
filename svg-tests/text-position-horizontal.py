import math

page_size = 400

def roundstr( x ):
    # output of 2 digits ought to be enough
    return str( round( x, 2 ) )


def output_header():
    size = str( page_size )
    print( '<?xml version="1.0" standalone="no"?>' )
    print( '<svg width="' + size + 'pt" height="' + size + 'pt"' )
    print( ' viewBox="0.00 0.00 ' + size + '.00 ' + size + '.00"' )
    print( ' version="1.1"' )
    print( ' xmlns="http://www.w3.org/2000/svg"' )
    print( ' xmlns:xlink="http://www.w3.org/1999/xlink">' )


def output_trailer():
    print( '</svg>' )

def dot( x, y, colour ):
    print( '<circle cx="' + roundstr(x) + '" cy="' + roundstr(y) + '"' )
    print( ' fill="' +colour+ '" stroke="' +colour+ '" r="2" />' )

def red_dot( x, y ):
    dot( x, y, 'red' )

def blue_dot( x, y ):
    dot( x, y, 'blue' )

def output_text( x, y, size, s ):
    # need to escape characters in the text
    print( '<text font-size="' + roundstr(size) + '" font-family="Times New Roman,serif"' )
    print( ' x="' + roundstr(x) + '" y="' + roundstr(y) + '">' + s + '</text>' )


# more globals
# page is square, get the center
cx = page_size / 2.0
cy = cx
center = roundstr(cx) + ',' + roundstr(cy)

output_header()

# instructions
x = 8
y = 15
f = 13
output_text( x, y, f, 'put names about 3/4 down slice' )
y += f + 2
output_text( x, y, f, 'from t1 to t2' )
y += f + 2
output_text( x, y, f, 'd = slice angle' )
y += f + 2
output_text( x, y, f, 'offset = 0.15' )
y += f + 2
output_text( x, y, f, 'margin = 1% of d' )
y += f + 2
output_text( x, y, f, 'len = inner + ( 1 - offset ) * ( outer - inner )' )
y += f + 2
output_text( x, y, f, 't1: x=len*cos(d/2 - margin), y=len*sin(d/2 - margin)' )
y += f + 2
output_text( x, y, f, 't2: x=same, y=-y' )

# line along the x axis
print( '' )
print( '<!-- draw x axis -->' )
print( '<path d="M' + center + ' ' + roundstr(cx+page_size/2) + ',' + roundstr(cy) + '" style="stroke:blue;" />' )
print( '' )
print( '<!-- dot at the center -->' )
red_dot( cx, cy )

# radius
inner = 80
outer = 150

# show circles at both those radii
print( '' )
print( '<!-- inner and outer circles -->' )
print( '<circle cx="' + roundstr(cx) + '" cy="' + roundstr(cy) + '"' )
print( ' fill="none" stroke="black" r="' + roundstr(inner) + '" />' )
print( '<circle cx="' + roundstr(cx) + '" cy="' + roundstr(cy) + '"' )
print( ' fill="none" stroke="black" r="' + roundstr(outer) + '" />' )

# angle of segment
d = 40

half_d = math.radians( d/2.0 )
margin = 0.1 * d / 100.0 #horizontal, before&after text
#margin = 0.0

# relative to center
print( '' )
print( '<!-- transform to center -->' )
print( '<g transform="translate(' + center + ')">' )

# remind me of the directions
# draw arrows in the global x and y directions
print( '' )
print( '<!-- labels and arrows to show x & y directions -->' )
output_text( -10, -2, 10, 'x &#8594;' )
output_text( -10, 11, 10, 'y &#8595;' )

print( '' )
print( '<!-- graphic context for slice contents -->' )
print( '<g transform="rotate(26,0,0)">' )

# reverse y because in svg y increases downward
print( '' )
print( '<!-- dots on the \'corners\' of the slice -->' )
s1_x = inner * math.cos(half_d)
s1_y = - inner * math.sin(half_d)
s1 = roundstr(s1_x) + ',' + roundstr(s1_y)
# put a dot and text there
blue_dot( s1_x, s1_y )
#output_text( s1_x, s1_y - 5, 10, 's1' )

s2_x = s1_x
s2_y = - s1_y
s2 = roundstr(s2_x) + ',' + roundstr(s2_y)
blue_dot( s2_x, s2_y )
#output_text( s2_x, s2_y + 12, 10, 's2' )

s3_x = outer * math.cos(half_d)
s3_y = outer * math.sin(half_d)
s3 = roundstr(s3_x) + ',' + roundstr(s3_y)
blue_dot( s3_x, s3_y )
#output_text( s3_x + 5, s3_y, 10, 's3' )

s4_x = s3_x
s4_y = - s3_y
s4 = roundstr(s4_x) + ',' + roundstr(s4_y)
blue_dot( s4_x, s4_y )
#output_text( s4_x + 4, s4_y, 10, 's4' )

print( '' )
print( '<!-- fill the slice -->' )
print( '<path style="stroke:grey; fill:lightgreen;"' )
print( 'd="M' + s1 )
r = roundstr(inner) + ',' + roundstr(inner)
print( 'A' + r + ' 0 0 1 ' + s2 )
print( 'L' + s3 )
r = roundstr(outer) + ',' + roundstr(outer)
print( 'A' + r + ' 0 0 0 ' + s4 )
print( 'z" />' )

# space below text
offset = 0.15
length = inner + ( 1.0 - offset ) * ( outer - inner )

print( '' )
print( '<!-- points of text baseline across the slice -->' )
t1_x = length * math.cos(half_d - margin)
t1_y = length * math.sin(half_d - margin)
blue_dot( t1_x, t1_y )
output_text( t1_x - 11, t1_y + 12, 10, 't1' )
t1 = roundstr(t1_x) + ',' + roundstr(t1_y)

t2_x = t1_x
t2_y = 0.0 - t1_y
blue_dot( t2_x, t2_y )
output_text( t2_x - 11, t2_y - 6, 10, 't2' )
t2 = roundstr(t2_x) + ',' + roundstr(t2_y)

print( '' )
print( '<!-- arc path of text baseline across the slice -->' )
rx = roundstr(outer)
ry = roundstr(outer)
path = '<path style="stroke:red; fill:none;"'
path += '\nd="M' + t1
path += '\nA' + ry + ' ' + rx + ' 0 0 0 ' + t2 + '" />'
print( path )

print( '</g> <!-- finish slice context -->' )
print( '</g> <!-- finish center transform -->' )

output_trailer()
