import sys
import math

page_width = 650
page_height = 1300

def roundstr( x ):
    # output of 2 digits ought to be enough
    return str( round( x, 2 ) )

def output_header():
    w = str( page_width )
    h = str( page_height )
    print( '<?xml version="1.0" standalone="no"?>' )
    print( '<svg width="' + w + 'pt" height="' + h + 'pt"' )
    print( ' viewBox="0.00 0.00 ' + w + '.00 ' + h + '.00"' )
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

def output_slice( d, inner, outer, colour, name ):
    half_d = math.radians( d/2.0 )

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

    print( '<path style="stroke:grey; fill:' + colour + ';"' )
    print( 'd="M' + p1 )
    r = roundstr(inner) + ',' + roundstr(inner)
    print( 'A' + r + ' 0 0 1 ' + p2 )
    print( 'L' + p3 )
    r = roundstr(outer) + ',' + roundstr(outer)
    print( 'A' + r + ' 0 0 0 ' + p4 )
    print( 'z" />' )

    output_text( p2_x, p2_y, 10, name )


def show_diagram( x, y, x_inc, slice, families ):

    cx = x
    cy = y

    #print( '', file=sys.stderr ) #debug
    #print( 'n fam', len(families), file=sys.stderr ) #debug
    for i in range(len(families)):
        #print( i, file=sys.stderr ) #debug
        center = roundstr(cx) + ',' + roundstr(cy)

        # draw the background slice first
        print( '<g transform="translate(' + center + ')">' )
        print( '<g transform="rotate(' + roundstr(slice['rotate']) + ')">' )

        if slice['x-axis']:
           # draw the x-axis
           print( '<path d="M0,0 l' + roundstr(page_width) + ',0" style="stroke:blue; fill:none;" />' )

        output_slice( slice['d'], slice['inner'], slice['outer'], slice['colour'], '' )

        # overlay with the completed families, up to the i'th one
        for j in range(i):
            #print( '   test', j, file=sys.stderr ) #debug
            fam = families[j]
            if fam['overlay']:
               #print( '     overlay', fam['colour'], file=sys.stderr ) #debug
               print( '<g transform="rotate(' + roundstr(fam['rotate']) + ',0,0)">' )
               output_slice( fam['d'], slice['fam_inner'], slice['outer'], fam['colour'], fam['name'] )
               print( '</g>' )

        # then the i'th one
        fam = families[i]
        #print( 'show', i, fam['colour'], file=sys.stderr ) #debug
        print( '<g transform="rotate(' + roundstr(fam['rotate']) + ',0,0)">' )
        output_slice( fam['d'], slice['fam_inner'], slice['outer'], fam['colour'], fam['name'] )
        print( '</g>' )

        print( '</g></g>' )
        cx += x_inc


output_header()

# instructions
x = 8
y = 15
f = 13
output_text( x, y, f, 'spouse name position' )
y += f + 2
output_text( x, y, f, 'within graphic context of' )
y += f + 2
output_text( x, y, f, 'person with the families' )

y += 30
output_text( x, y, f, 'first family' )

y = 200
output_text( x, y, f, 'rotate family slice to touch enclosing:' )
y += f + 2
output_text( x, y, f, 't = 0 - slice&#176;/2' )
y += f + 2
output_text( x, y, f, 't = t + fam_slice&#176;/2' )

y = 370
output_text( x, y, f, 'second family' )

y = 530
output_text( x, y, f, 'rotate second family to touch first:' )
y += f + 2
output_text( x, y, f, 'rotate up to slice then' )
y += f + 2
output_text( x, y, f, 'down whole angle of previous' )
y += f + 2
output_text( x, y, f, 's = 0 - slice&#176;/2 + fam[2]&#176;/2' )
y += f + 2
output_text( x, y, f, 's = s + fam[1]&#176;' )

y = 700
output_text( x, y, f, 'third family' )

y = 870
output_text( x, y, f, 'rotate third family to touch second:' )
y += f + 2
output_text( x, y, f, 'rotate up to slice then' )
y += f + 2
output_text( x, y, f, 'down whole angle of previous' )
y += f + 2
output_text( x, y, f, 's = 0 - slice&#176;/2 + fam[3]&#176;/2' )
y += f + 2
output_text( x, y, f, 's = s + fam[1]&#176; + fam[2]&#176;' )

y = 1030
output_text( x, y, f, 'finally, rotate the graphic context' )
y += f + 2
output_text( x, y, f, 'of each slice to show how' )
y += f + 2
output_text( x, y, f, 'contents also rotate' )

cx = 80
cy = 100
x_inc = 80
y_inc = 170

slice = {'d':60, 'inner':80, 'outer':150, 'colour':'lightgreen', 'fam_inner':120, 'rotate':0, 'x-axis':True}

fam_sets = []
fam_d_sum = 0

# first family
c = 'pink'
n = 'fam 1'
d = 15
rot = 0
fam_sets.append( {'d':d, 'rotate':rot, 'colour':c, 'name':n, 'overlay':True} )
show_diagram( cx, cy, x_inc, slice, fam_sets )

# first family rotated
cy += y_inc
rot = 0 - slice['d']/2 + d/2 + fam_d_sum
fam_sets.append( {'d':d, 'rotate':rot, 'colour':c, 'name':n, 'overlay':True} )
# don't show the previous unrotated one
fam_sets[-2]['overlay'] = False
fam_d_sum += d
show_diagram( cx, cy, x_inc, slice, fam_sets )

# second family
c = 'cyan'
n = 'fam 2'
cy += y_inc
d = 20
rot = 0
fam_sets.append( {'d':d, 'rotate':rot, 'colour':c, 'name':n, 'overlay':True} )
show_diagram( cx, cy, x_inc, slice, fam_sets )

# second family rotated
cy += y_inc
rot = 0 - slice['d']/2 + d/2 + fam_d_sum
fam_sets.append( {'d':d, 'rotate':rot, 'colour':c, 'name':n, 'overlay':True} )
# don't show the previous unrotated one
fam_sets[-2]['overlay'] = False
fam_d_sum += d
show_diagram( cx, cy, x_inc, slice, fam_sets )

# third family
c = 'orange'
n = 'fam 3'
cy += y_inc
d = 12
rot = 0
fam_sets.append( {'d':d, 'rotate':rot, 'colour':c, 'name':n, 'overlay':True} )
show_diagram( cx, cy, x_inc, slice, fam_sets )

# third family rotated
cy += y_inc
rot = 0 - slice['d']/2 + d/2 + fam_d_sum
fam_sets.append( {'d':d, 'rotate':rot, 'colour':c, 'name':n, 'overlay':True} )
# don't show the previous unrotated one
fam_sets[-2]['overlay'] = False
fam_d_sum += d
show_diagram( cx, cy, x_inc, slice, fam_sets )

# funally, rotate each one
slice['rotate'] = -70
slice['x-axis'] = False
cy += 1.6 * y_inc
show_diagram( cx, cy, x_inc, slice, fam_sets )

output_trailer()
