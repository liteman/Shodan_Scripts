import sys
import shodan
import json


SHODAN_API_KEY = ""

APIHANDLE = shodan.Shodan(SHODAN_API_KEY)
OUTFILE = '/Users/user/Desktop/shodan_export.txt'

def main(args):
    try:
        query = args[1]
    except IndexError:
        print "Did you forget your query?"

    exportResults = []
    try:
        cursor = APIHANDLE.search_cursor(query)
        result = cursor.next()
        while result:
            exportResults.append(result)
            result = cursor.next()

    except shodan.APIError as e:
        print e
    except StopIteration:
        pass



    with open(OUTFILE, 'w') as outfile:
        json.dump(exportResults, outfile,indent=4)

    print "Query string: " + query
    print "Results exported to: " + OUTFILE
    print "Remaining API Query Credits: " + str(APIHANDLE.info()['query_credits'])

if __name__ == "__main__":
    main(sys.argv)