import shodansearch
import os


ss = shodansearch.ShodanSearch()
ss.VERBOSE = False

nets = ['128.229.0.0/16',
        '63.110.107.192/28']

print "Current API Credits:"
ss.printinfo()
print

outfilepath = "/Users/user/Desktop/"
for net in nets:
    query = "net:'" + net + "'"
    outfilename = net.replace("/", "_") + "_shodan.json"
    ss.validate_query(query)
    print "Query: " + query
    results = ss.runquery(query,facets=['os', 'port'])
    ss.output_results(results, outfile=os.path.join(outfilepath, outfilename))
    #ss.output_results(results, facets=True)
    print

print
print "Current API Credits:"
ss.printinfo()

