# folder_labels.py

## Idea

Print labels for folders (the non-digital ones, holding paper and stuff).

Each label holds:

- a letter (e.g. ｀B｀ for Batman)
- a number (e.g. ｀03｀)
- a description (e.g. ｀Batmobil｀)
- several items (e.g. ｀insurance｀, ｀repair bills｀, etc.)

### Why this structure?

Think of a couple or family, say, Batman and Robin,
who have folders for each one of them separately (labeled ｀B｀ and ｀R｀, respectively)
as well folders where they keep documents for them both as a Team (labeled ｀T｀).

Each one might have different folders,
such as Batman having documents concerning the ｀Batmobil｀ (｀insurance｀, ｀repair bills｀, etc.),
the employment of his butler ｀Alfred｀ (｀social security｀, ｀health care plan｀, etc.), and so on.

For additional ordering, the folders have numbers as well.

You can adapt the letters and styling to your needs using the file ｀config.py｀(see [below](#config-file)).
The data to be put on the labels is created using a CSV (Comma Separated Value) file,
which can be edited either using Excel (or something similar) or a simple text editor (see [below](#input-format)).

### Features

- Text scales if too wide for folder label
- Customizable: font, positioning of elements, papersize, are all adaptable
(with special support for different folder widths)

## Input format

To be able to have commas in an item, I decided to use tabulators as delimiters in the csv file.
If you use Excel or something similar to edit the csv, this should not cause problems.
If you use a text editor, be sure it does not replace tabs with spaces.
Alternatively, you can change the delimiter in the function ｀read_labels_from_file()｀ in ｀folder_labels.py｀.

Here is the sample input also found in ｀sample_input.csv｀:

｀｀｀csv
Batman	1	Alfred	social security#health care plan#employment contract	wide
Batman	2	Batmobile	construction plans#insurance#repair bills	wide
Robin	1	Robin Cycle	insurance#repair bills	narrow
Team	1	Batcave	cleaning rota#property tax	narrow
｀｀｀

## Config file

The file ｀config.py｀ consists of

- the ｀FontStyles｀ class to set font type, sizes, and also the symbol used in the item list
- the ｀Measures｀ class to set the height of the label, the papersize, and some offsets to space the different elements
- the ｀Width｀ class (an Enum), where you can set different folder widths
- the ｀Letter｀ class (an Enum), where you can set the letter corresponding to each person

The offsets in ｀Measures｀ can easily be changed, but you will have to experiment a little bit.
The provided values should be fine, though.

Note: ｀config.py｀ is included in ｀.gitignore｀, so private data cannot accidentaly be commited to a public server.
Therefore, you have to copy ｀config_example.py｀ to ｀config.py｀ and adapt at least some values.
Checkout the comments in ｀config_example.py｀ for that.

## How-to use

- Create a virtual environment, install the dependencies from ｀requirements.txt｀, activate the virtual environment
- Copy ｀config_example.py｀ to ｀config.py｀, adapt to your needs (see comments in the file for details)
- Copy ｀sample_input.csv｀ to ｀your_input.csv｀, enter your data
- Run the script like so:

｀｀｀bash
python3 folder_labels.py infile.csv outfile.pdf
｀｀｀

## Some remarks

This software uses the Reportlab Toolkit (cf. <https://docs.reportlab.com/>).
Thank you for providing this open source.

## Licence

This software is licenced under the GNU General Public Licence (see ｀LICENCE｀).
