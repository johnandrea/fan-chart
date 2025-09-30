#import sys
import math

page_size = 500

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

output_header()

# instructions
x = 8
y = 15
f = 13
output_text( x, y, f, 'narrow slices require sideway text' )
y += f + 2
output_text( x, y, f, 'from P7 to P8' )
y += f + 2
output_text( x, y, f, 'P7: x=inner, y=0' )
y += f + 2
output_text( x, y, f, 'P8: x=outer, y=0' )
y += f + 2
output_text( x, y, f, 'width = outer - inner' )
y += f + 2
output_text( x, y, f, 'middle N: x=inner + (outer-inner)/2, y=0' )

y = 260
output_text( x, y, f, 'second example' )
y += f + 2
output_text( x, y, f, 'text along the edge of the slice' )

# radius
inner = 80
outer = 150

# angle of segment
d = 15
half_d = math.radians( d/2.0 )

# placement of first example
cx = 300
cy = 40
center = roundstr(cx) + ',' + roundstr(cy)

# line along the x axis
print( '<path d="M' + center + ' ' + roundstr(cx+page_size/2) + ',' + roundstr(cy) + '" style="stroke:blue;" />' )
# and a dot at the center
red_dot( cx, cy )

# show circles at both those radii
print( '<circle cx="' + roundstr(cx) + '" cy="' + roundstr(cy) + '"' )
print( ' fill="none" stroke="black" r="' + roundstr(inner) + '" />' )
print( '<circle cx="' + roundstr(cx) + '" cy="' + roundstr(cy) + '"' )
print( ' fill="none" stroke="black" r="' + roundstr(outer) + '" />' )

# remind me of the directions
output_text( cx - 10, cy - 2, 10, 'x &#8594;' )
output_text( cx - 10, cy + 11, 10, 'y &#8595;' )

# relative to center
print( '<g transform="translate(' + center + ')">' )

# reverse y because in svg y increases downward
p1_x = inner * math.cos(half_d)
p1_y = - inner * math.sin(half_d)
p1 = roundstr(p1_x) + ',' + roundstr(p1_y)
# put a dot and text there
blue_dot( p1_x, p1_y )
#output_text( p1_x, p1_y - 5, 10, 'P1' )

p2_x = p1_x
p2_y = - p1_y
p2 = roundstr(p2_x) + ',' + roundstr(p2_y)
blue_dot( p2_x, p2_y )
#output_text( p2_x, p2_y + 12, 10, 'P2' )

p3_x = outer * math.cos(half_d)
p3_y = outer * math.sin(half_d)
p3 = roundstr(p3_x) + ',' + roundstr(p3_y)
blue_dot( p3_x, p3_y )
#output_text( p3_x + 5, p3_y, 10, 'P3' )

p4_x = p3_x
p4_y = - p3_y
p4 = roundstr(p4_x) + ',' + roundstr(p4_y)
blue_dot( p4_x, p4_y )
#output_text( p4_x + 4, p4_y, 10, 'P4' )

# begin the sector
print( '<path style="stroke:grey; fill:lightgreen;"' )
print( 'd="M' + p1 )
r = roundstr(inner) + ',' + roundstr(inner)
print( 'A' + r + ' 0 0 1 ' + p2 )
print( 'L' + p3 )
r = roundstr(outer) + ',' + roundstr(outer)
print( 'A' + r + ' 0 0 0 ' + p4 )
print( 'z" />' )

p7_x = inner
p7_y = 0
blue_dot( p7_x, p7_y )
output_text( p7_x + 4, p7_y - 2, 10, 'P7' )
p7 = roundstr(p7_x) + ',' + roundstr(p7_y)

p8_x = outer
p8_y = - 0
blue_dot( p8_x, p8_y )
output_text( p8_x + 4, p8_y - 2, 10, 'P8' )
p8 = roundstr(p8_x) + ',' + roundstr(p8_y)

n_x = inner + (outer - inner)/2
n_y = - 0
blue_dot( n_x, n_y )
output_text( n_x, n_y - 4, 8, 'N' )

# connect with a line
print( '<path d="M' + p7 + ' ' + p8 + '" style="stroke:red;" />' )

print( '</g>' )

# second example
cx = 300
cy = 380
center = roundstr(cx) + ',' + roundstr(cy)

# line along the x axis
print( '<path d="M' + center + ' ' + roundstr(cx+page_size/2) + ',' + roundstr(cy) + '" style="stroke:blue;" />' )
# and a dot at the center
red_dot( cx, cy )

# show circles at both those radii
print( '<circle cx="' + roundstr(cx) + '" cy="' + roundstr(cy) + '"' )
print( ' fill="none" stroke="black" r="' + roundstr(inner) + '" />' )
print( '<circle cx="' + roundstr(cx) + '" cy="' + roundstr(cy) + '"' )
print( ' fill="none" stroke="black" r="' + roundstr(outer) + '" />' )

# remind me of the directions
output_text( cx - 10, cy - 2, 10, 'x &#8594;' )
output_text( cx - 10, cy + 11, 10, 'y &#8595;' )

# relative to center
print( '<g transform="translate(' + center + ')">' )

# reverse y because in svg y increases downward
p1_x = inner * math.cos(half_d)
p1_y = - inner * math.sin(half_d)
p1 = roundstr(p1_x) + ',' + roundstr(p1_y)
# put a dot and text there
blue_dot( p1_x, p1_y )
#output_text( p1_x, p1_y - 5, 10, 'P1' )

p2_x = p1_x
p2_y = - p1_y
p2 = roundstr(p2_x) + ',' + roundstr(p2_y)
blue_dot( p2_x, p2_y )
#output_text( p2_x, p2_y + 12, 10, 'P2' )

p3_x = outer * math.cos(half_d)
p3_y = outer * math.sin(half_d)
p3 = roundstr(p3_x) + ',' + roundstr(p3_y)
blue_dot( p3_x, p3_y )
#output_text( p3_x + 5, p3_y, 10, 'P3' )

p4_x = p3_x
p4_y = - p3_y
p4 = roundstr(p4_x) + ',' + roundstr(p4_y)
blue_dot( p4_x, p4_y )
#output_text( p4_x + 4, p4_y, 10, 'P4' )

# begin the sector
print( '<path style="stroke:grey; fill:lightgreen;"' )
print( 'd="M' + p1 )
r = roundstr(inner) + ',' + roundstr(inner)
print( 'A' + r + ' 0 0 1 ' + p2 )
print( 'L' + p3 )
r = roundstr(outer) + ',' + roundstr(outer)
print( 'A' + r + ' 0 0 0 ' + p4 )
print( 'z" />' )

p7_x = inner
p7_y = 0
blue_dot( p7_x, p7_y )
output_text( p7_x + 4, p7_y - 2, 10, 'P7' )
p7 = roundstr(p7_x) + ',' + roundstr(p7_y)

p8_x = outer
p8_y = - 0
blue_dot( p8_x, p8_y )
output_text( p8_x + 4, p8_y - 2, 10, 'P8' )
p8 = roundstr(p8_x) + ',' + roundstr(p8_y)

n_x = inner + (outer - inner)/2
n_y = - 0
blue_dot( n_x, n_y )
output_text( n_x, n_y - 4, 8, 'N' )

# connect with a line
print( '<path d="M' + p7 + ' ' + p8 + '" style="stroke:red;" />' )

print( '</g>' )

output_trailer()
