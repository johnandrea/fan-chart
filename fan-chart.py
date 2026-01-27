#!/usr/local/bin/python3

"""
Produce a genealogy fan chart (full circle).
Input is a GEDCOM file
Output an SVG file to std-out

Goals:
1: scriptable
2: text consistently  faces outward or vertically clockwise

The intention is that the output will be printed on a large sheet
at a print service such as Staples.
If necessary to convert the output to PDF: use Inkscape:
"inkscape --export-filename=NAME.pdf NAME.svg"
https://wiki.inkscape.org/wiki/Using_the_Command_Line

This code is released under the MIT License: https://opensource.org/licenses/MIT
Copyright (c) 2025 John A. Andrea

No support provided.

I may use the term "pixels" to represent distances.
"""

import sys
import argparse
import importlib.util
import os
import math

# define an svg page size
# arbitrary and square, but scalable
page_size = 600

# "standard" colour scheme
# based on https://colorbrewer2.org/?type=qualitative&scheme=Pastel1&n=9
slice_colours = ['#fbb4ae','#b3cde3','#ccebc5','#decbe4','#fed9a6']
slice_colours.extend( ['#ffffcc','#e5d8bd','#fddaec','#f2f2f2'] )

n_colours = len( slice_colours )

# even on a large sheet, no need for huge fonts
max_font_size = 20

# all the text sizes are based on this typeface
font_selection = 'font-family="Times New Roman,serif"'


def get_version():
    return '0.8.3'


def subtract_a_percentage( x, p ):
    return x - x * p / 100.0


def roundstr( x ):
    # output of 2 digits ought to be enough
    return str( round( x, 2 ) )


def compute_arc_length( radius, arc_degrees ):
    # standard trig function
    return radius * math.radians( arc_degrees )


def estimate_font_height( font_size ):
    # result in pixels
    return font_size * 2.0 / 3.0


def reverse_font_height( pixels ):
    # from pixels to estimated font size
    return pixels * 3.0 / 2.0


def setup_char_widths():
    # Return the estimated character width: slope of line per font size.
    # y-intercept is ignored (assumed zero): zero font size equals zero width
    # The small y-intercepts calculated were probably nothing more than
    # my mistakes in estimating the exact character spacing.

    results = dict()

    # These two were defined previously, to be used for characters
    # not matching the below definitions
    results["generic lower"] = 0.4615
    results["generic upper"] = 0.657

    results[" "] = 0.246
    results["a"] = 0.446
    results["A"] = 0.721
    results["b"] = 0.499
    results["B"] = 0.666
    results["c"] = 0.440
    results["C"] = 0.668
    results["d"] = 0.499
    results["D"] = 0.719
    results["e"] = 0.435
    results["E"] = 0.608
    results["f"] = 0.324
    results["F"] = 0.550
    results["g"] = 0.497
    results["G"] = 0.722
    results["h"] = 0.496
    results["H"] = 0.725
    results["i"] = 0.273
    results["I"] = 0.329
    results["j"] = 0.265
    results["J"] = 0.392
    results["k"] = 0.501
    results["K"] = 0.720
    results["l"] = 0.273
    results["L"] = 0.610
    results["m"] = 0.790
    results["M"] = 0.862
    results["n"] = 0.500
    results["N"] = 0.716
    results["o"] = 0.497
    results["O"] = 0.716
    results["p"] = 0.487
    results["P"] = 0.556
    results["q"] = 0.502
    results["Q"] = 0.734
    results["r"] = 0.322
    results["R"] = 0.668
    results["s"] = 0.380
    results["S"] = 0.553
    results["t"] = 0.269
    results["T"] = 0.616
    results["u"] = 0.500
    results["U"] = 0.721
    results["v"] = 0.498
    results["V"] = 0.717
    results["w"] = 0.722
    results["W"] = 0.960
    results["x"] = 0.498
    results["X"] = 0.722
    results["y"] = 0.495
    results["Y"] = 0.721
    results["z"] = 0.451
    results["Z"] = 0.625
    results["+"] = 0.574
    results["-"] = 0.334
    results["0"] = 0.496
    results["1"] = 0.457
    results["2"] = 0.494
    results["3"] = 0.491
    results["4"] = 0.494
    results["5"] = 0.492
    results["6"] = 0.496
    results["7"] = 0.493
    results["8"] = 0.494
    results["9"] = 0.497
    results["("] = 0.324
    results[")"] = 0.322
    return results


def estimate_string_width( font_size, s ):
    # For a given font size, return the approximate pixel
    # width of the string.

    result = 0
    for c in s:
        k = 'generic upper'
        if c in char_width_factors:
           k = c
        result += font_size * char_width_factors[k]

    ## What about kerning spacing. Presuming its included in the
    ## individual string widths, but add small extra width anyway.
    #result += char_width_factors[' '] * font_size

    return result


def font_to_fit_string( width, s ):
    # return the font size that will fit the given string to the width
    trial_font = 25
    s_w = estimate_string_width( trial_font, s )
    # from the width estimation: width = slope * fontsize
    # reverse it using a big character
    wide_char_w = trial_font * char_width_factors[widest_char]
    # so the font size to fit the string is the ratio
    result = width * wide_char_w / s_w
    return result


def calculate_generation_rings( n_gen ):
    # generation zero circle surrounded by rings for the other generations
    # Show the complete circles because it helps to visualize families which
    # don't reach the maximum generations.
    #
    # return a list with computed dimensions for each ring
    # with the index being the generation number

    # width of each ring - for now each is the same width
    # a little smaller then the whole page to leave a margin
    width = ( page_size - 20 ) / 2 / n_gen

    results = []

    # inside circle radius is the ring width
    inner = 0
    r = width
    for _ in range( n_gen ):
        results.append( {'outer':r, 'inner':inner} )
        # increase radius for each generation
        inner = r
        r += width

    return results


def outline_generations( rings ):
    # increase stroke width in order to hide any small drawing errors
    circle = '<circle cx="0" cy="0"'
    circle += ' fill="none" stroke-width="2" stroke="grey" r="'
    for detail in rings:
        print( circle + str(detail['outer']) + '"/>' )


def load_my_module( module_name, relative_path ):
    """
    Load a module in my own single .py file. Requires Python 3.6+
    Give the name of the module, not the file name.
    Give the path to the module relative to the calling program.
    Requires:
        import importlib.util
        import os
    Use like this:
        readgedcom = load_my_module( 'readgedcom', '../libs' )
        data = readgedcom.read_file( input-file )
    """
    assert isinstance( module_name, str ), 'Non-string passed as module name'
    assert isinstance( relative_path, str ), 'Non-string passed as relative path'

    file_path = os.path.dirname( os.path.realpath( __file__ ) )
    file_path += os.path.sep + relative_path
    file_path += os.path.sep + module_name + '.py'

    assert os.path.isfile( file_path ), 'Module file not found at ' + str(file_path)

    module_spec = importlib.util.spec_from_file_location( module_name, file_path )
    my_module = importlib.util.module_from_spec( module_spec )
    module_spec.loader.exec_module( my_module )

    return my_module


def get_program_options():
    results = {}

    colour_types = ['standard','bw']

    results['infile'] = None
    results['personid'] = None
    results['generations'] = 5
    results['id-item'] = 'xref'
    results['dates'] = False
    results['colour'] = 'standard'
    results['libpath'] = '.'

    arg_help = 'Draw fan chart.'
    parser = argparse.ArgumentParser( description=arg_help )

    arg_help = 'Maximum number of generations to show. Default ' + str(results['generations'])
    parser.add_argument( '--generations', default=results['generations'], type=int, help=arg_help )

    arg_help = 'How to find the person in the input. Default is the gedcom id "xref".'
    arg_help += ' Othewise choose "type.exid", "type.refnum", etc.'
    parser.add_argument( '--id-item', default=results['id-item'], type=str, help=arg_help )

    arg_help = 'Year will displayed.'
    parser.add_argument( '--dates', default=results['dates'], action='store_true', help=arg_help )

    arg_help = 'Colour scheme. Default:' + results['colour']
    parser.add_argument( '--colour', default=results['colour'], type=str, help=arg_help )

    # maybe this should be changed to have a type which better matched a directory
    arg_help = 'Location of the gedcom library. Default is current directory.'
    parser.add_argument( '--libpath', default=results['libpath'], type=str, help=arg_help )

    arg_help = 'Show version then exit.'
    parser.add_argument( '--version', action='version', version=get_version() )

    parser.add_argument('infile', type=argparse.FileType('r') )
    parser.add_argument('personid', type=str )

    args = parser.parse_args()

    results['infile'] = args.infile.name
    results['personid'] = args.personid
    results['id-item'] = args.id_item
    results['generations'] = args.generations
    results['dates'] = args.dates

    check_value = args.colour
    if check_value.lower() in colour_types:
       results['colour'] = check_value.lower()

    results['libpath'] = args.libpath

    return results


def get_indi_years( indi ):
    # return birth - death or birth- or -death
    # but None if both dates are empty
    # This version does not include parenthesis

    def get_indi_year( indi_data, tag ):
        # "best" year for birth, death, ...
        # or an empty string
        result = ''

        best = 0
        if readgedcom.BEST_EVENT_KEY in indi_data:
           if tag in indi_data[readgedcom.BEST_EVENT_KEY]:
              best = indi_data[readgedcom.BEST_EVENT_KEY][tag]
        if tag in indi_data:
           if indi_data[tag][best]['date']['is_known']:
              result = str( indi_data[tag][best]['date']['min']['year'] )
        return result

    result = None

    birth = get_indi_year( data[ikey][indi], 'birt' ).strip()
    death = get_indi_year( data[ikey][indi], 'deat' ).strip()
    if birth or death:
       result = birth +'-'+ death

    return result


def find_max_generations( indi, max_gen, n_gen ):
    gen_count = n_gen

    if n_gen <= max_gen:
       children = []
       if 'fams' in data[ikey][indi]:
          for fam in data[ikey][indi]['fams']:
              if 'chil' in data[fkey][fam]:
                 for child in data[fkey][fam]['chil']:
                     children.append( child )

       for child in children:
           gen_count = max( gen_count, find_max_generations( child, max_gen, n_gen + 1 ) )

    return gen_count


def compute_max_gen_children( indi, max_gen, n_gen ):
    # if every family had at least one descendant which reached the
    # maximum generation, how many children would that be at that generation

    n = 0

    if n_gen > max_gen:
       # the person (or person with spouse) at the end
       # counts as one slice

       n = 1

    else:

       n_fam = 0
       n_fam_with_children = 0
       children = []

       if 'fams' in data[ikey][indi]:
          for fam in data[ikey][indi]['fams']:
              fam_has_children = False

              n_fam += 1
              if 'chil' in data[fkey][fam]:
                 for child in data[fkey][fam]['chil']:
                     fam_has_children = True
                     children.append( child )
              if fam_has_children:
                 n_fam_with_children += 1

       n_children = len( children )

       if n_fam == 0:
          # no families, so can't go any further
          # this person counts as 1 slice

          n = 1

       elif n_children > 0:
          # next generation
          # but consider the childless families this person might have had
          n = n_fam - n_fam_with_children
          for child in children:
              n += compute_max_gen_children( child, max_gen, n_gen + 1 )

       else:
          # families, but no children,
          # so can't go another generation
          # but each family counts as a slice

          n = n_fam

    return n


def count_slices( indi, max_gen, n_gen ):
    # determine the number of slices for each person/family
    # which depends on the number of slices of descendants
    global diagram_data

    diagram_data[indi] = {}
    diagram_data[indi]['fams'] = []

    n = 0

    if n_gen > max_gen:
       # the person (or person with spouse) at the end
       # counts as one slice

       n = 1

    else:

       n_fam = 0
       n_fam_with_children = 0

       if 'fams' in data[ikey][indi]:
          for fam in data[ikey][indi]['fams']:
              fam_data = {}
              fam_data['fam'] = fam
              fam_data['slices'] = 0

              fam_has_children = False
              n_fam += 1
              n_children_slices = 0
              if 'chil' in data[fkey][fam]:
                 for child in data[fkey][fam]['chil']:
                     fam_has_children = True
                     # descend at this point because the count
                     # belongs to this family
                     n_children_slices += count_slices( child, max_gen, n_gen+1 )
              if fam_has_children:
                 n_fam_with_children += 1
                 fam_data['slices'] = n_children_slices
                 n += n_children_slices
              else:
                 # this family has only the one slice
                 fam_data['slices'] = 1

              # save this family
              diagram_data[indi]['fams'].append( fam_data )

       if n_fam == 0:
          # no families, so can't go any further
          # this person counts as 1 slice

          n = 1

       else:
          # had families, already counted children's slices, maybe none
          # consider the childless families this person might have had
          n += n_fam - n_fam_with_children

    # save this person
    diagram_data[indi]['slices'] = n

    return n


def output_header():
    size = str( page_size )
    print( '<?xml version="1.0" standalone="no"?>' )
    print( '<!-- generated by fan-chart.py', get_version(), '-->' )
    print( '<svg width="' + size + 'pt" height="' + size + 'pt"' )
    print( ' viewBox="0.00 0.00 ' + size + '.00 ' + size + '.00"' )
    print( ' version="1.1"' )
    print( ' xmlns="http://www.w3.org/2000/svg"' )
    print( ' xmlns:xlink="http://www.w3.org/1999/xlink">' )


def output_trailer():
    print( '</svg>' )


def output_name( d, inner, outer, draw_separator, prefix, indi ):
    # this is the distance where the text will be placed relative
    # to the height of the available area
    distance_factor = 0.9

    # should this be global ?
    # don't bother flipping to vertical if the font is this or above
    min_reasonable_font_size = 3

    name = '?'
    dates = ''
    if indi:
       # possibly the family has an unknown spouse
       name = data[ikey][indi]['name'][0]['html']
       if options['dates']:
          # in this test, the dates are simply appended to the name
          got_dates = get_indi_years( indi )
          if got_dates:
             dates = ' ' + got_dates
    name = prefix + name + dates

    half_d = math.radians( d/2.0 )
    text_baseline = inner + distance_factor * ( outer - inner )
    x = text_baseline * math.cos( half_d )
    y = text_baseline * math.sin( half_d )

    # the height of the area is the maximum font size
    # though a better heuristic must be used for sideways as well
    text_area_height = text_baseline - 4

    # estimate the width as the middle of the section
    text_area_width = compute_arc_length( inner+(outer-inner)/2, d )
    ## what if the inner arc is used
    #text_area_width = compute_arc_length( inner, d )

    # put the text on a curve,
    # no need for a separate graphic context
    path_id = 'text' + str(indi)

    # start by assuming lengthwise text
    path = 'M' + roundstr(x) +','+ roundstr(y)
    path += ' A' + roundstr(text_baseline) +','+ roundstr(text_baseline)
    path += ' 0 0 0'
    path += ' ' + roundstr(x) +','+ roundstr(-y)

    # save the originally calculated width
    text_area_size = text_area_width

    font_size = font_to_fit_string( text_area_size, name )

    # try to determine how to fit the text
    if text_area_height > text_area_width:
       # then try flipping it
       # unless the text still fits nicely in the shorter length
       if font_size < min_reasonable_font_size:
          # recompute all the sizes
          text_area_size = text_area_width
          # make a new path running vertically
          text_baseline = inner + distance_factor * ( outer - inner )
          x = text_baseline * math.cos( half_d )
          y = text_baseline * math.sin( half_d )

    if estimate_font_height(font_size) > text_area_height:
       # this is where a heuristic is needed to compare the available
       # width vs height
       font_size = 0.75 * reverse_font_height( text_area_size )

    if font_size > max_font_size:
       font_size = max_font_size

    string_length = estimate_string_width( font_size, name )

    # try to center it on the curve
    offset = text_area_size / 2 - string_length / 2

    # change to a percent (is that what the startOffset parameter needs?)
    offset = 100.0 * offset / text_area_size
    # bit of a margin, 1.5%
    offset = roundstr( offset + 1.5 ) + '%'

    font_options = ' font-size="' + roundstr(font_size) + '"'
    font_options += ' ' + font_selection
    # this style doesn't look good
    #font_options += ' style="fill:black; stroke:white;"'

    print( '<path id="' + path_id + '" d="' + path + '" style="fill:none;" />' )
    print( '<text ' + font_options + '>' )
    print( ' <textPath xlink:href="#' + path_id + '" startOffset="' + offset + '">' + name + '</textPath>' )
    print( '</text>' )

    ## show the curve
    # print( '<path d="' + path + '" style="stroke:red; fill:none;" />' )

    if draw_separator:
       # put a line in front of the name
       # used for separating multiple marriages
       x = outer * math.cos(half_d)
       y = outer * math.sin(half_d)
       line = 'M' + roundstr(x) +','+ roundstr(y)
       x = inner * math.cos(half_d)
       y = inner * math.sin(half_d)
       line += ' L' + roundstr(x) +','+ roundstr(y)
       print( '<path d="' + line + '" style="stroke:grey; stroke-width:2;" />' )


def output_a_slice( d, inner, outer, colour ):
    # slice of a ring given inner and outer radius
    # with center at 0,0 and centered on the x-axis

    half_d = math.radians( d / 2.0 )

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

    print( '<path style="stroke:grey; stroke-width:2; fill:' + colour +';"' )
    print( 'd="M' + p1 )
    r = roundstr(inner) + ',' + roundstr(inner)
    print( 'A' + r + ' 0 0 1 ' + p2 )
    print( 'L' + p3 )
    r = roundstr(outer) + ',' + roundstr(outer)
    print( 'A' + r + ' 0 0 0 ' + p4 )
    print( 'z" />' )

    ## for debugging text, put a line at the bottom of the slice
    #print( '<path d="M' + p3 + ' ' + p4 + '" style="stroke:red;" />' )


def find_spouse( fam, indi ):
    if indi:
       known = 'husb'
       other = 'wife'
       if known in data[fkey][fam]:
          if indi == data[fkey][fam][known][0]:
             if other in data[fkey][fam]:
                return data[fkey][fam][other][0]
       known = 'wife'
       other = 'husb'
       if known in data[fkey][fam]:
          if indi == data[fkey][fam][known][0]:
             if other in data[fkey][fam]:
                return data[fkey][fam][other][0]
    return None


def output_slices( gen, start_rotation, start_colour, colour_skip, start_fam, degrees_per_slice, slice_extra, ring_data, diagram_data ):
    # each slice rotates around the center

    colour_index = start_colour

    # colour skip is used so that children don't get the same colour as
    # a parents sibling, but don't let it get too big
    if colour_skip > 5:
       colour_skip = 2

    # rotate it up from the x-axis
    rotation = start_rotation

    first_child = True
    for child in data[fkey][start_fam]['chil']:
        n_slices = diagram_data[child]['slices']
        slice_degrees = degrees_per_slice * n_slices

        # how many familes does this person have
        n_fams = len( diagram_data[child]['fams'] )

        if first_child:
           first_child = False
           slice_degrees += slice_extra

        # rotate this much more as if it lined up with the x-axis
        rotation += slice_degrees / 2.0

        # each child gets their own graphic context
        g_rotate = 'rotate(' + roundstr(rotation) + ',0,0)'
        print( '<g transform="' + g_rotate + '">' )

        colour_index = colour_index % n_colours
        output_a_slice( slice_degrees, ring_data[gen]['inner'], ring_data[gen]['outer'], slice_colours[colour_index] )

        # a person with no families takes up the whole slice
        # but with families the person gets the upper half
        # and the spouse gets the lower half
        ring_inner = ring_data[gen]['inner']
        ring_outer = ring_data[gen]['outer']
        if n_fams > 0:
           ring_outer = ring_inner + ( ring_outer - ring_inner ) / 2.0

        output_name( slice_degrees, ring_inner, ring_outer, False, '', child )

        # output each spouse name, each gets their own graphic context
        if n_fams > 0:
           # the inner ring is the bottom of the "child" name
           # as computed above
           ring_inner = ring_outer + 2
           ring_outer = ring_data[gen]['outer']
           fam_sum = 0

           for fam_data in diagram_data[child]['fams']:
               fam = fam_data['fam']
               spouse = find_spouse( fam, child )
               fam_degrees = fam_data['slices'] * degrees_per_slice
               fam_rotation = 0 - slice_degrees /2 + fam_degrees /2 + fam_sum
               g_rotate = 'rotate(' + roundstr(fam_rotation) + ',0,0)'
               print( '<g transform="' + g_rotate + '">' )
               output_name( fam_degrees, ring_inner, ring_outer, True, '+ ', spouse )
               print( '</g>' )
               fam_sum += fam_degrees

        print( '</g>' )

        # next generation
        if n_fams > 0:
           child_rotation = rotation - slice_degrees / 2.0
           for next_fam_data in diagram_data[child]['fams']:
               next_fam = next_fam_data['fam']
               output_slices( gen+1, child_rotation, colour_index, colour_skip+2, next_fam, degrees_per_slice, 0, ring_data, diagram_data )
               next_slices = next_fam_data['slices']
               child_rotation += next_slices * degrees_per_slice

        # next child starts rotation where this child ended
        rotation += slice_degrees / 2.0
        colour_index += colour_skip
        if colour_index > n_colours:
           colour_index = 1


def output_start_names( fam, ring_outer ):
    # in testing mode there is only one family at the top,
    # wrap around almost half circle
    d = 170

    inner = ring_outer / 2
    outer = ring_outer

    rotate = 0
    prefix = ''
    for partner in ['husb','wife']:
        indi = None
        if partner in data[fkey][fam]:
           indi = data[fkey][fam][partner][0]
        print( '<g transform="rotate(' + str(rotate) + ',0,0)">' )
        output_name( d, inner, outer, False, prefix, indi )
        print( '</g>' )
        prefix = '+ '
        rotate = 180


# more globals
# page is square, get the center
cx = page_size / 2.0
cy = cx

char_width_factors = setup_char_widths()
# this is used to find font for widths
widest_char = ' '
for c in char_width_factors:
    if char_width_factors[c] > char_width_factors[widest_char]:
       widest_char = c


options = get_program_options()

if options['generations'] < 1:
   print( 'Generations must be more than zero', file=sys.stderr )
   sys.exit(1)

readgedcom = load_my_module( 'readgedcom', options['libpath'] )

# these are keys into the parsed sections of the returned data structure
ikey = readgedcom.PARSED_INDI
fkey = readgedcom.PARSED_FAM

data_opts = {}
data_opts['display-gedcom-warnings'] = True
data_opts['exit-on-no-families'] = True
data_opts['exit-on-missing-individuals'] = True
data_opts['exit-on-missing-families'] = True
data_opts['only-birth'] = True

data = readgedcom.read_file( options['infile'], data_opts )

id_match = readgedcom.find_individuals( data, options['id-item'], options['personid'] )
if len(id_match) == 1:

   start_person = id_match[0]

   # find the actual maximum number of generations
   # in case a too large number was given in the options

   max_generations = find_max_generations( start_person, options['generations'], 1 )

   if max_generations > 1:
      #print( 'max gen', max_generations, file=sys.stderr ) #debug

      # slice size is computed by
      # 360 degrees divided by the number of people reaching the outermost layer
      #
      # to get that number of people we have to pretend that every family has children
      # out to the max generation

      max_slices = compute_max_gen_children( start_person, max_generations, 1 )

      #print( 'slices', max_slices, file=sys.stderr ) #debug

      # truncate to a few decimal points because the output can't be infinitely exact
      slice_decimals = 1

      degrees_per_slice = round( 360.0 / max_slices, slice_decimals )

      # and the floating point division might not be exact,
      # so the (tiny) remainder should be added to the first slice in each generation

      slice_remainder = round( 360.0 - degrees_per_slice * max_slices, slice_decimals )

      diagram_data = {}

      count_slices( start_person, max_generations, 1 )

      output_header()

      ring_sizes = calculate_generation_rings( max_generations )

      # generation 0 is special - it is in the inner circle
      # there must be another generation or else the program would have exited
      # special case when start person has multiple families - handle in future

      # the first child starts at the top, so rotate it -90 deg from the x-axis
      # need to do something with colours too, first child should match parents

      # translate everything to the center of the page
      g_trans = 'translate(' + roundstr(cx) + ',' + roundstr(cy) + ')'
      print( '<g transform="' + g_trans + '">' )

      # testing is using only one start family
      start_fam = diagram_data[start_person]['fams'][0]['fam']

      output_start_names( start_fam, ring_sizes[0]['outer'] )

      output_slices( 1, -90.0, 0, 1, start_fam, degrees_per_slice, slice_remainder, ring_sizes, diagram_data )

      # show the rings on top of the slices
      outline_generations( ring_sizes )

      print( '</g>' )

      output_trailer()

   else:
      print( 'Selected person has no children.', file=sys.stderr )
      sys.exit(1)

else:
   if len(id_match) > 1:
      print( 'More than one person matches the given id', file=sys.stderr )
   else:
      print( 'No person matches the given id', file=sys.stderr )
   sys.exit(1)
