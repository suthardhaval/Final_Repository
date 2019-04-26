from PyPDF2 import PdfFileMerger

merger = PdfFileMerger()

input1 = open("FinTech_1.pdf", "rb")
input2 = open("FinTech_2.pdf", "rb")
input3 = open("FinTech_3.pdf", "rb")
input4 = open("FinTech_4.pdf", "rb")

# append all files to create one file
merger.append(input1)
merger.append(input2)
merger.append(input3)
merger.append(input4)

# Write to an output PDF document
output = open("PDF_merge.pdf", "wb")
merger.write(output)
