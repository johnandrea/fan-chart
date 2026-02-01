#import sys
import math

page_x = 500
page_y = 1000

def roundstr( x ):
    # output of 2 digits ought to be enough
    return str( round( x, 2 ) )


def output_header():
    print( '<?xml version="1.0" standalone="no"?>' )
    print( '<svg width="' + str(page_x) + 'pt" height="' + str(page_y) + 'pt"' )
    print( ' viewBox="0.00 0.00 ' + str(page_x) + '.00 ' + str(page_y) + '.00"' )
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

def setup_circles( x, y ):
    center = roundstr(x) + ',' + roundstr(y)

    # line along the x axis
    print( '<path d="M' + center + ' ' + roundstr(cx+page_x/2) + ',' + roundstr(y) + '" style="stroke:blue;" />' )
    # and a dot at the center
    red_dot( x, y )

    # show circles at both those radii
    print( '<circle cx="' + roundstr(x) + '" cy="' + roundstr(y) + '"' )
    print( ' fill="none" stroke="black" r="' + roundstr(inner) + '" />' )
    print( '<circle cx="' + roundstr(x) + '" cy="' + roundstr(y) + '"' )
    print( ' fill="none" stroke="black" r="' + roundstr(outer) + '" />' )

    # remind me of the directions
    output_text( x - 10, y - 2, 10, 'x &#8594;' )
    output_text( x - 10, y + 11, 10, 'y &#8595;' )

    # relative to center
    print( '<g transform="translate(' + center + ')">' )

def finish_circles():
    # undo the transform
    print( '</g>' )

def draw_sector():
    print( '<path style="stroke:grey; fill:lightgreen;"' )
    print( 'd="M' + p1 )
    r = roundstr(inner) + ',' + roundstr(inner)
    print( 'A' + r + ' 0 0 1 ' + p2 )
    print( 'L' + p3 )
    r = roundstr(outer) + ',' + roundstr(outer)
    print( 'A' + r + ' 0 0 0 ' + p4 )
    print( 'z" />' )

output_header()

# placement of first example
cx = 340
cy = 40
cy_inc = 295 - 40

# radius
inner = 80
outer = 150

# angle of segment
d = 15
half_d = math.radians( d/2.0 )

# instructions
x = 8
text_y = 15
y = text_y
f = 13
output_text( x, y, f, 'Narrow slices require sideway text from P7 to P8:' )
y += f + 2
output_text( x, y, f, 'new-d = factor * d/2' )
y += f + 2
output_text( x, y, f, 'slice-width = outer - inner' )
y += f + 2
output_text( x, y, f, 'length-margin = ( 1 - factor ) * slice-width' )
y += f + 2
output_text( x, y, f, 'new-inner = inner + length-margin' )
y += f + 2
output_text( x, y, f, 'new-outer = outer - length-margin' )
y += f + 2
output_text( x, y, f, 'P7: x=new-inner*cos(new-d), y=new-inner*sin(new-d)' )
y += f + 2
output_text( x, y, f, 'P8: x=new-outer*cos(new-d), y=new-outer*sin(new-d)' )

text_y += cy_inc
y = text_y
output_text( x, y, f, 'Text area:' )
y += f + 2
output_text( x, y, f, 'middle of the text line at M' )
y += f + 2
output_text( x, y, f, 'middle = new-inner + ( new-outer - new_inner )/2' )
y += f + 2
output_text( x, y, f, 'M: x=middle*cos(new-d), y=middle*sin(new-d)' )
y += f + 2
y += f + 2
output_text( x, y, f, 'height of text area at P9' )
y += f + 2
output_text( x, y, f, 'P9: x=P7[x], y=-P7[y]' )
y += f + 2
output_text( x, y, f, 'height = 2 * P7[y]' )

text_y += cy_inc
y = text_y
output_text( x, y, f, 'Place the text:' )
y += f + 2
output_text( x, y, f, 'path from p7 to p8' )
y += f + 2
output_text( x, y, f, 'place text along that path' )
y += f + 2
output_text( x, y, f, 'Also need to center text width about path middle.' )

text_y += cy_inc
y = text_y
output_text( x, y, f, 'Show the section rotated:' )

# first example
setup_circles( cx, cy )

# reverse y because in svg y increases downward
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

draw_sector()

# draw the line where the text would go

margin_d_factor = 0.8
margin_w_factor = 0.95

margined_d = margin_d_factor * half_d

slice_width = inner + ( outer - inner )/2
slice_margin = ( 1.0 - margin_w_factor ) * slice_width
margined_inner = inner + slice_margin
margined_outer = outer - slice_margin

p7_x = margined_inner * math.cos( margined_d )
p7_y = margined_inner * math.sin( margined_d )
blue_dot( p7_x, p7_y )
output_text( p7_x + 4, p7_y - 2, 10, 'P7' )
p7 = roundstr(p7_x) + ',' + roundstr(p7_y)

p8_x = margined_outer * math.cos( margined_d )
p8_y = margined_outer * math.sin( margined_d )
blue_dot( p8_x, p8_y )
output_text( p8_x + 4, p8_y - 2, 10, 'P8' )
p8 = roundstr(p8_x) + ',' + roundstr(p8_y)

# connect with a line
print( '<path d="M' + p7 + ' ' + p8 + '" style="stroke:red;" />' )

finish_circles()

# second example
cy += cy_inc
setup_circles( cx, cy )
center = roundstr(cx) + ',' + roundstr(cy)

draw_sector()

blue_dot( p7_x, p7_y )
output_text( p7_x + 4, p7_y - 2, 10, 'P7' )

blue_dot( p8_x, p8_y )
output_text( p8_x + 4, p8_y - 2, 10, 'P8' )

# connect with a line
print( '<path d="M' + p7 + ' ' + p8 + '" style="stroke:red;" />' )

middle = margined_inner + ( margined_outer - margined_inner ) / 2

m_x = middle * math.cos( margined_d )
m_y = middle * math.sin( margined_d )
blue_dot( m_x, m_y )
output_text( m_x, m_y - 4, 8, 'M' )

p9_x = p7_x
p9_y = 0 - p7_y
blue_dot( p9_x, p9_y )
output_text( p9_x, p9_y - 4, 8, 'P9' )
p9 = roundstr(p9_x) +','+ roundstr(p9_y)
# connect with a line
print( '<path d="M' + p7 + ' ' + p9 + '" style="stroke:red;" />' )

finish_circles()

# third example
cy += cy_inc
setup_circles( cx, cy )
draw_sector()

print( '<path id="text" d="M' + p7 + ' L' + p8 + '" style="fill:none;" />' )
print( '<text font_size="12" font-family="Times New Roman,serif">' )
print( ' <textPath xlink:href="#text" startOffset="5%">Words</textPath>' )
print( '</text>' )

finish_circles()

# fourth example
cy += cy_inc
setup_circles( cx, cy )
print( '<g transform="rotate(-35)">' )
draw_sector()
print( '<text font_size="12" font-family="Times New Roman,serif">' )
print( ' <textPath xlink:href="#text" startOffset="5%">Words</textPath>' )
print( '</text>' )
print( '</g>' )
finish_circles()

output_trailer()
