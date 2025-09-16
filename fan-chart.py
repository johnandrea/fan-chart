#!/usr/local/bin/python3
import sys
import argparse
import importlib.util
import os
import math

# define an svg page size
# arbitrary and square, but scalable
page_size = 600

slice_colours = ['mediumturquoise','thistle', 'mistyrose', 'lightseagreen','lightblue']
slice_colours.extend( ['coral', 'khaki', 'lemonchiffon', 'lavenderblush'] )
slice_colours.extend( ['yellowgreen', 'tan', 'lightsteelblue', 'salmon','springgreen'] )


def get_version():
    return '0.3.1'


def subtract_a_percentage( x, p ):
    return x - x * p / 100.0


def roundstr( x ):
    # output of 2 digits ought to be enough
    return str( round( x, 2 ) )


def estimate_string_width( font_size, s ):
    # this is where i miss Postscript
    #
    # For a given font size, return the approximate pixel
    # width of the string.
    #
    # The SVG function stringlength is of no value because it changes kerning.
    #
    # Numbers come from a display of characters on a grid
    # them fitting the results to a line (which was suprisingly straight).
    # Probably should do it with a specific font rather than the default
    # and do it for each letter.
    #
    # y = mx + b
    # pixels_per_char = slope * font_size + intercept
    #
    # lowercase: slope=0.4615, intercept=0
    # uppercase: slope=0.657, intercept=-0.375

    # start with everything as upper case
    # which also takes care of digits, non-alpha, etc

    n_upper = len( s )

    # reduce by the number of lowercase
    # (is this pythonic)
    n_lower = 0
    for c in list( 'abcdefghijklmnopqrstuvwxyz' ):
        n_lower += s.count( c )

    pixels = ( n_upper - n_lower ) * ( 0.657 * font_size - 0.375 )
    pixels += n_lower * ( 0.4615 * font_size )

    return pixels


def font_to_fit_string( width, s ):
    # return the font size that will fit the given string to the width
    trial_font = 25
    pixels = estimate_string_width( trial_font, s )
    # assume a linear relationship between fonts and widths
    return trial_font * width / pixels


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

    date_types = ['none', 'year', 'full']
    colour_types = ['bw']

    results['infile'] = None
    results['personid'] = None
    results['generations'] = 5
    results['id-item'] = 'xref'
    results['dates'] = 'none'
    results['colour'] = 'bw'
    results['libpath'] = '.'

    arg_help = 'Draw fan chart.'
    parser = argparse.ArgumentParser( description=arg_help )

    arg_help = 'Maximum number of generations to show. Default ' + str(results['generations'])
    parser.add_argument( '--generations', default=results['generations'], type=int, help=arg_help )

    arg_help = 'How to find the person in the input. Default is the gedcom id "xref".'
    arg_help += ' Othewise choose "type.exid", "type.refnum", etc.'
    parser.add_argument( '--id-item', default=results['id-item'], type=str, help=arg_help )

    arg_help = 'Date style. One of none, year, none. Default:' + results['dates']
    parser.add_argument( '--dates', default=results['dates'], type=str, help=arg_help )

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

    check_value = args.dates
    if check_value.lower() in date_types:
       results['dates'] = check_value.lower()

    check_value = args.colour
    if check_value.lower() in colour_types:
       results['colour'] = check_value.lower()

    results['libpath'] = args.libpath

    return results


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
    distance_factor = 0.85
    font_size = 13

    name = '?'
    if indi:
       # possibly the family has an unknown spouse
       name = data[ikey][indi]['name'][0]['html']
    name = prefix + name
    string_length = estimate_string_width( font_size, name ) / 2.0
    # increase that estimate a bit for now
    string_length *= 1.33

    half_d = math.radians( d/2.0 )
    text_distance = inner + distance_factor * ( outer - inner )
    x = text_distance * math.cos( half_d )
    y = text_distance * math.sin( half_d )

    # put the text on a curve,
    # no need for a separate graphic context
    path_id = 'text' + str(indi)
    path = 'M' + roundstr(x) +','+ roundstr(y)
    path += ' A' + roundstr(text_distance) +','+ roundstr(text_distance)
    path += ' 0 0 0'
    path += ' ' + roundstr(x) +','+ roundstr(-y)

    # try to center it on the curve

    # trig formuls: length = r * angle
    # and shorten a bit for margins
    arc_length = subtract_a_percentage( text_distance * math.radians( d ), 5 )

    offset = arc_length / 2 - string_length / 2

    # change to a percent
    offset = 100.0 * offset / arc_length
    offset = roundstr( offset ) + '%'

    print( '<defs>' )
    print( '  <path id="' + path_id + '" d="' + path + '" />' )
    print( '</defs>' )
    print( '<text font-size="' + roundstr(font_size) + '" font-family="Times New Roman,serif">' )
    print( '  <textPath href="#' + path_id + '" startOffset="' + offset + '">' + name + '</textPath>' )
    print( '</text>' )

    if draw_separator:
       x = outer * math.cos(half_d)
       y = outer * math.sin(half_d)
       line = 'M' + roundstr(x) +','+ roundstr(y)
       x = inner * math.cos(half_d)
       y = inner * math.sin(half_d)
       line += ' L' + roundstr(x) +','+ roundstr(y)
       print( '<path d="' + line + '" style="stroke:grey; stroke-width:2;" />' )

    ## draw the path to debug - why is it not an arc
    #print( '<path d="' + path + '" style="stroke:red; fill:none;" />' )


def output_a_slice( d, inner, outer, colour ):
    # slice of a ring given inner and outer radius
    # with center at 0,0 and centered on the x-axis

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

        output_a_slice( slice_degrees, ring_data[gen]['inner'], ring_data[gen]['outer'], slice_colours[colour_index] )

        # a person with no families takes up the whole slice
        # but with families the person gets the upper half
        # and the spouse gets the lower half
        ring_inner = ring_data[gen]['inner']
        ring_outer = ring_data[gen]['outer']
        if n_fams > 0:
           ring_outer = ring_inner + ( ring_outer - ring_inner ) / 2.0

        output_name( slice_degrees, ring_inner, ring_outer, False, '', child )

        print( '</g>' )

        # output each spouse name, each gets their own graphic context
        if n_fams > 0:
           # the inner ring is the bottom of the "child" name
           # as computed above
           ring_inner = ring_outer + 2
           ring_outer = ring_data[gen]['outer']
           fam_rotation = rotation
           do_multi_fam_rotation = False
           if n_fams > 1:
              # then the first spouse needs to get a bit more
              do_multi_fam_rotation = True

           for fam_data in diagram_data[child]['fams']:
               fam = fam_data['fam']
               spouse = find_spouse( fam, child )
               fam_degrees = fam_data['slices'] * degrees_per_slice
               if do_multi_fam_rotation:
                  # just once
                  do_multi_fam_rotation = False
                  #fam_rotation -= ( n_fams - 1 ) * fam_degrees / 2.0
                  #fam_rotation -= ( diagram_data[child]['slices'] - 1 ) * fam_degrees / 2.0
               g_rotate = 'rotate(' + roundstr(fam_rotation) + ',0,0)'
               print( '<g transform="' + g_rotate + '">' )
               output_name( fam_degrees, ring_inner, ring_outer, True, '+ ', spouse )
               # and a line needs to be drawn to separate the families
               # if more than 1
               print( '</g>' )
               fam_rotation -= fam_degrees / 2.0

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
        if colour_index > len( slice_colours ):
           colour_index = 1


# more globals
# page is square, get the center
cx = page_size / 2.0
cy = cx


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

      #for indi in diagram_data:
      #    print( '', file=sys.stderr)
      #    print( indi, data[ikey][indi]['name'][0]['html'], file=sys.stderr )
      #    print( 'slices', diagram_data[indi]['slices'], file=sys.stderr )
      #    if diagram_data[indi]['fams']:
      #       print( 'fams:', file=sys.stderr )
      #       for fam_data in diagram_data[indi]['fams']:
      #           fam = fam_data['fam']
      #           husb = data[fkey][fam]['husb'][0]
      #           wife = data[fkey][fam]['wife'][0]
      #           other = husb
      #           if indi == husb:
      #              other = wife
      #           print( 'with', data[ikey][other]['name'][0]['html'], file=sys.stderr )
      #           print( 'fam', fam_data['fam'], 'slices', fam_data['slices'], file=sys.stderr )

      output_header()

      ring_sizes = calculate_generation_rings( max_generations )

      ## try showing some text
      ## try putting it inside the inner circle
      #test_string = 'test fitting text in circle'
      ## size of that circle is twice its radius
      #font_size = font_to_fit_string( 2*ring_sizes[0]['outer'], test_string )
      ## ok, what's the width going to be
      #string_width = estimate_string_width( font_size, test_string )
      ## x is center offset by half the string
      #x = cx - string_width / 2
      ## y is center offset by half the font size
      #y = cy + font_size / 2
      #output_text( x, y, font_size, test_string )
      ## what are those numbers
      #print( '<text font-size="10" x="10" y="20">d:' + roundstr(2*ring_sizes[0]['outer']) + '</text>' )
      #print( '<text font-size="10" x="10" y="40">font:' + roundstr(font_size) + '</text>' )
      #print( '<text font-size="10" x="10" y="60">width:' + roundstr(string_width) + '</text>' )
      ## show those places with dots
      #print( '<circle cx="' + roundstr(cx) + '" cy="' + roundstr(cy) + '"' )
      #print( ' fill="red" stroke="red" r="2" />' )
      #print( '<circle cx="' + roundstr(x) + '" cy="' + roundstr(y) + '"' )
      #print( ' fill="blue" stroke="blue" r="2" />' )

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
