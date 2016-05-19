import sys
import shodan
import json
import argparse
import re
from pprint import pprint


class ShodanSearch(object):
    def __init__(self):
        self.VERBOSE = False
        self.SHODAN_API_KEY = ""
        self.APIHANDLE = shodan.Shodan(self.SHODAN_API_KEY)
        self.ALLFILTERS = ["after", "asn", "before", "city", "country", "geo", "has_screenshot", "hostname",
                           "html", "isp", "link", "net", "org", "os", "port", "postal", "product", "state",
                           "title", "version", "bitcoin.ip", "bitcoun.ip_count", "bitcoint.port",
                           "bitcoin.version", "ntp.ip", "ntp.ip_count", "ntp.more", "ntp.port"]
        self.FACETS = ["org",
                       "domain",
                       "os",
                       "port",
                       "asn",
                       "country"]

    def validate_query(self, querystr):
        if self.VERBOSE:
            print "[DEBUG] Query: " + querystr
        pattern = "(\S+):"
        matches = re.findall(pattern, querystr)
        for match in matches:
            if match not in self.ALLFILTERS:
                print match + " is not a valid filter. Try:\n "
                for item in self.ALLFILTERS:
                    print item
                sys.exit(1)

    def printinfo(self):
        info = self.APIHANDLE.info()
        pprint(info.get('query_credits'))

    def runquery(self, query, facets=None, count=False):

        if count and not facets:  # count is set, but facets is not
            if self.VERBOSE: print "[DEBUG] count: True / Facets: False"
            output = self.APIHANDLE.count(query)
        elif count and facets:  # count and facets are set
            if self.VERBOSE: print "[DEBUG] count: True / Facets: True"
            output = self.APIHANDLE.count(query, facets)
        elif not count and not facets:  # count is not set, and facets is not set
            if self.VERBOSE: print "[DEBUG] count: False / Facets: False"
            output = []
            try:
                cursor = self.APIHANDLE.search_cursor(query, minify=False)
                result = cursor.next()
                while result:
                    output.append(result)
                    result = cursor.next()

            except shodan.APIError as e:
                print e
            except StopIteration:
                pass

        elif not count and facets:  # count is not set, facets is set
            if self.VERBOSE: print "[DEBUG] count: False / Facets: True"
            output = self.APIHANDLE.search(query, facets=facets, minify=False)

        return output

    def output_results(self, results, outfile=None, count=False, facets=False):
        if count and not facets:  # count: true, facets: false
            print "Result count: " + str(results.get('total'))
        elif count and facets:  # count: true, facets: true
            print "Result count: " + str(results.get('total'))
            pprint(results.get('facets'))
        elif not count and facets:  # count: false, facets: true
            print "Facets:"
            pprint(results.get('facets'))
        elif outfile:
            print "Query returned " + str(len(results)) + " results. Writing to: " + outfile
            with open(outfile, 'a') as of:
                for match in results:
                    json.dump(match, of, indent=4)
                    of.write("\n")
                    count += 1
        else:
            pprint(results)

    def main(self):

        parser = argparse.ArgumentParser(description="Shodan Search Tool")
        parser.add_argument("--count",
                            action='store_true',
                            help="Return result count for the specified query")
        parser.add_argument("-q",
                            "--query",
                            required=True,
                            help="Query string")
        parser.add_argument("--facets",
                            action='store_true',
                            help="Returns the Top X items found (e.g. Top Ports, Top Organizations")
        parser.add_argument("--outfile",
                            help="Filename for exported results")
        parser.add_argument("-v",
                            "--verbose",
                            action='store_true',
                            help="Print debug output")

        args = parser.parse_args()

        # initialize local variables
        facets = False
        count = False
        outfile = None
        if args.facets: facets = self.FACETS
        if args.count: count = True
        if args.outfile: outfile = args.outfile

        # initialize global variables
        if args.verbose: ss.VERBOSE = True

        print "Starting Shodan Query"
        print "Current API credits: "
        self.printinfo()
        print "\n"

        query = args.query
        #self.validate_query(query)
        results = self.runquery(query, facets, count)
        self.output_results(results, outfile, count, facets)

        print "\nQuery complete"
        print "Current API Credts: "
        ss.printinfo()

if __name__ == '__main__':
    ss = ShodanSearch()
    ss.main()
    sys.exit(0)
