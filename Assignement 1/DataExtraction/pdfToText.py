#source: https://medium.com/@justinboylantoomey/fast-text-extraction-with-python-and-tika-41ac34b0fe61
from tika import parser

file = 'PDF_merge.pdf'
f = open("final_data.txt","w",encoding="utf8")
# Parse data from file
file_data = parser.from_file(file)
# Get files text content
text = file_data['content']
f.write(text)