def textFullColumn(text, maxColumn):
    textChars = []
    textLines = []
	charCount = 0
	width = maxColumn

    for i in range(len(text)):

        char = text[i]
    	textChars.append(char)

    if i == len(text) - 1 and(charCount < width):
        for j in range(width - charCount):
        textChars.append(' ')

    if ((char == '\n') or(charCount == width)):
        textLines.append(textChars)# print textLines
    	textChars = []
    	charCount = 0# print i

    elif i == len(text) - 1:
        textLines.append(textChars)
    	textChars = []
    	charCount = 0

    else :
        charCount += 1

    	textLinesReversed = itertools.chain( * textLines[::-1])
    	stringForPrinter = ''.join(list(textLinesReversed))
    return stringForPrinter
