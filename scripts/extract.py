from boilerpipe.extract import Extractor
extractor = Extractor(extractor='KeepEverythingExtractor', url='http://bit.ly/L4Tv8P')
text = extractor.getText().encode('utf-8')
outfile = open('html.txt','w')
outfile.write(text)
outfile.close()
