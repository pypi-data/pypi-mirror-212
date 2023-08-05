from epos.printer import Printer
from epos.document import EposDocument
from epos.elements import Text, Feed, Barcode
from epos.constants import Align, BarcodeType, HRI

# Create a new printer object with 10.0.0.10 as ip
printer = Printer('10.0.0.10')
# Check if we can connect to the printer with no errors, otherwise exit
if not printer.try_connection():
    exit()
print('Connection with printer established.')

# Create a new EposDocument object
# This will contain all the individual elements
doc = EposDocument()

# Add an element directly to the body of the document
doc.add_body(Text('This is example text!\n'))
doc.add_body(Feed()) # Another way to add a newline

# It's also possible to first create the text object and then change the properties
t = Text('Some special text :O\n')
t.bold = True
t.align = Align.CENTER
t.double_width = False
t.width = 1
doc.add_body(t)

# Rotated text
t = Text('This text is rotated\n')
t.rotate = True
doc.add_body(t)

# Find max length in double mode
t = Text("|"*25)
t.double_width = True
t.double_height = True
t.rotate = False
t.reverse = True
t.align = Align.LEFT
t.bold = False
doc.add_body(t)

# Add 2 empty lines
doc.add_body(Feed(5))

# Add a barcode
doc.add_body(Barcode(BarcodeType.CODE39, '01234567890', align=Align.LEFT, width=2, height=64, hri=HRI.BELOW))

# Send the whole document to the printer
# This will automatially send a Cut at the end of the document body
r = printer.print(doc)
print(r)