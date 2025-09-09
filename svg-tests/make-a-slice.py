#import sys
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
output_text( x, y, f, 'd is the internal angle of the slice' )
y += f + 2
output_text( x, y, f, 'translate graphic context to center' )
y += f + 2
output_text( x, y, f, '1: move to P1: x=inner*cos(d/2), y=-inner*sin(d/2)' )
y += f + 2
output_text( x, y, f, '2: arc to P2: x=same, y=-y, sweep=1' )
y += f + 2
output_text( x, y, f, '3: line to P3: x=outer*cos(d/2), y=outer*sin(d/2)' )
y += f + 2
output_text( x, y, f, '4: arc to P4: x=same, y=-y, sweep=0' )
y += f + 2
output_text( x, y, f, '5: close path' )

y = 400 - 120
output_text( x, y, f, 'arcs in a path:' )
y += f + 2
output_text( x, y, f, 'start at current point' )
y += f + 2
output_text( x, y, f, 'radiusX,radiusY' )
y += f + 2
output_text( x, y, f, 'space x-axis-roatation (usually zero)' )
y += f + 2
output_text( x, y, f, 'space large-arc-flag (usually zero)' )
y += f + 2
output_text( x, y, f, 'space sweep-flag (zero or one depending on direction)' )
y += f + 2
output_text( x, y, f, 'space endX,endY' )

# line along the x axis
print( '<path d="M' + center + ' ' + roundstr(cx+page_size/2) + ',' + roundstr(cy) + '" style="stroke:blue;" />' )
# and a dot at the center
red_dot( cx, cy )

# radius
inner = 80
outer = 150

# show circles at both those radii
print( '<circle cx="' + roundstr(cx) + '" cy="' + roundstr(cy) + '"' )
print( ' fill="none" stroke="black" r="' + roundstr(inner) + '" />' )
print( '<circle cx="' + roundstr(cx) + '" cy="' + roundstr(cy) + '"' )
print( ' fill="none" stroke="black" r="' + roundstr(outer) + '" />' )

# remind me of the directions
output_text( cx - 10, cy - 2, 10, 'x &#8594;' )
output_text( cx - 10, cy + 11, 10, 'y &#8595;' )


# angle of segment
d = 40

half_d = math.radians( d/2.0 )

# relative to center
print( '<g transform="translate(' + center + ')">' )

# reverse y because in svg y increases downward
p1_x = inner * math.cos(half_d)
p1_y = - inner * math.sin(half_d)
p1 = roundstr(p1_x) + ',' + roundstr(p1_y)
# put a dot and text there
blue_dot( p1_x, p1_y )
output_text( p1_x, p1_y - 5, 10, 'P1' )

p2_x = p1_x
p2_y = - p1_y
p2 = roundstr(p2_x) + ',' + roundstr(p2_y)
blue_dot( p2_x, p2_y )
output_text( p2_x, p2_y + 12, 10, 'P2' )

p3_x = outer * math.cos(half_d)
p3_y = outer * math.sin(half_d)
p3 = roundstr(p3_x) + ',' + roundstr(p3_y)
blue_dot( p3_x, p3_y )
output_text( p3_x + 5, p3_y, 10, 'P3' )

p4_x = p3_x
p4_y = - p3_y
p4 = roundstr(p4_x) + ',' + roundstr(p4_y)
blue_dot( p4_x, p4_y )
output_text( p4_x + 4, p4_y, 10, 'P4' )

# begin the sector
print( '<path style="stroke:grey; fill:lightgreen;"' )

# step 1
print( 'd="M' + p1 )

# step 2
r = roundstr(inner) + ',' + roundstr(inner)
print( 'A' + r + ' 0 0 1 ' + p2 )

# step 3
print( 'L' + p3 )

# step 4
r = roundstr(outer) + ',' + roundstr(outer)
print( 'A' + r + ' 0 0 0 ' + p4 )

# step 5 ends the sector path
print( 'z" />' )

print( '</g>' )

#                 print( '      a180,180 0 0 0 180,0' )
#                 print( '      l-40,-100' )
#                 print( '      a80,80 0 0 1 -100,0' )



output_trailer()
