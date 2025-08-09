#!/usr/local/bin/python3
import sys
import argparse
import importlib.util
import os


def get_version():
    return '0.0.9'


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
    print( 'indi,max,gen', indi, max_gen, n_gen ) #debug
    # if every family had at least one descendant which reached the
    # maximum generation, how many children would that be at that generation

    n = 0

    if n_gen > max_gen:
       print( 'past max' ) #debug
       # the person (or person with spouse) at the end
       # counts as one slice

       n = 1

    else:

       n_fam = 0
       children = []

       if 'fams' in data[ikey][indi]:
          print( 'has fams' ) #debug
          for fam in data[ikey][indi]['fams']:
              print( 'fam', fam ) #debug
              n_fam += 1
              if 'chil' in data[fkey][fam]:
                 print( 'has children' ) #debug
                 for child in data[fkey][fam]['chil']:
                     children.append( child )

       n_children = len( children )

       if n_fam == 0:
          # no families, so can't go any further
          # this person counts as 1 slice

          n = 1

       elif n_children > 0:
          # go deeper
          for child in children:
              n += compute_max_gen_children( child, max_gen, n_gen + 1 )

       else:
          # families, but no children,
          # so can't go deeper,
          # but each family counts as a slice

          n = n_fam

    print( 'returning', n ) #debug
    return n


options = get_program_options()
#print( options ) #debug

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

   print( data[ikey][start_person]['name'][0]['html'] ) #debug

   # find the actual maximum number of generations
   # in case a too large number was given in the options

   max_generations = find_max_generations( start_person, options['generations'], 1 )

   if max_generations > 1:
      print( 'max gen', max_generations ) #debug

      # slice size is computed by
      # 360 degrees divided by the number of people reaching the outermost layer
      #
      # to get that number of people we have to pretend that every family has children
      # out to the max generation

      max_slices = compute_max_gen_children( start_person, max_generations, 1 )

      print( 'slices', max_slices ) #debug

      # truncate to a few decimal points because the output can't be infinitely exact
      slice_decimals = 1

      slice_size = round( 360.0 / max_slices, slice_decimals )

      # and the floating point division might not be exact,
      # so the (tiny) remainder should be added to the first slice in each generation

      slice_remainder = round( 360.0 - slice_size * max_slices, slice_decimals )

      print( 'slice', slice_size ) #debug
      print( 'remainder', slice_remainder ) #debug

   else:
      print( 'Selected person has no children.', file=sys.stderr )
      sys.exit(1)

else:
   if len(id_match) > 1:
      print( 'More than one person matches the given id', file=sys.stderr )
   else:
      print( 'No person matches the given id', file=sys.stderr )
   sys.exit(1)
