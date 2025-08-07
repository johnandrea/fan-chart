# fan-chart.py

A program which will produce a full circle genealogy fan chart from a GEDCOM input.

Reasons for making my own program:

- scriptable
- orient the text for reading on a large printed sheet: horizontal to outside edge and consistently clockwise

## Features

- Scriptable.
- Output is an SVG file.
- Makes use of [readgedcom.py](https://github.com/johnandrea/readgedcom) library.

## Limitations

- Requires Python 3.6+

## Installation

No installation process. Copy the program and the library.

## Input

The input is a GEDCOM file exported from a genealogy program.

## Options

gedcom-file

Full path to the input file.

top-person

Id of the person at the top of the tree to be output. Value of this id depends on the "id-item" setting.

--id-item=value

Specify the item to identify the tester via each tester id. Default is "xref" which is the individual
XREF value in the GEDCOM file.
Other options might be "uuid", "refn", etc. If using a GEDCOM custom type specify it as "type." followed by
the type name, i.e. "type.extid", "type.refnumber", etc.

--generations=number

Maximum number of generations to output. Default 5.
In theory there is no upper limit, but around 12 the text gets too small to be useful for a reasonably
sized hardcopy paper sheet.

--colour=colour scheme

Currently only black and white.
Default BW.

--dates

Include dates in the output. Default is no option=no date.

--libpath=directory-containing-readgedcom

Location containing the readgedcom.py library file. The path is relative to the program being used. An absolute path will not work. Default is the same location as the program (".").

--version 

Display the version number then exit

## Usage

```
program in-file id-top-person > out.svg
```

## Bug reports

This code is provided with neither support nor warranty.

### Future enhancements

- More colours
- Describe ways to convert svg to pdf
- Handle non-ASCII names in a manner better for SVG output.

