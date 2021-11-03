## -- This code opens an existing csv file and replaces the characters of the target column 
## -- through the values stored in a couple of dictionaries 
## -- Originally designed to format addresses

## FILES ##
csv1 = open(r'c:/route/file1.csv','r', encoding="utf-8")
csv1_new = open(r'c:/route/file1_new.csv','w', encoding="utf-8")

## FUNCTIONS ##

## Character format function
def formatline(line):

    chardict = {'\"' : '' , ',' : ' ,', '.' : '', '–' : '', '-' : ' ', '   ' : ' ', '  ' : ' '}  ## New rules here

    for char in chardict:
        line = line.replace(char, chardict[char])

    return line
    
## Word format function
def formatword(word):

    wordict = {'Street' : 'St' , 'Square' : 'Sq', 'Road' : 'Rd'}  ## New rules here

    title = word.title()

    if title in wordict:
        title = title.replace(title,wordict[title])

    return title


## FORMATTING ##

column_index = 1

for line in csv1.readlines():  
    
    ## Extract address
    columns = line.split(';')
    rawadd = columns[column_index]

    ## Fix characters in address
    rawadd1 = formatline(rawadd) 

    ## Extract words
    words = rawadd1.split(' ')

    fixadd = []
	
    ## Fix words
    for word in words:
                 
        formated = formatword(word)

        if formated not in fixadd:  ## Avoid duplicates
            fixadd.append(formated)    
        
    ## New address
    newadd = ' '.join(fixadd) 

    ## Copy to new file
    newline = line.replace(rawadd,newadd)
    csv1_new.write(newline)


## Close file
csv1.close()
csv1_new.close()
