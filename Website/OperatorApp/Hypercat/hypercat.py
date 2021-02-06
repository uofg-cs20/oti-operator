# HYPERCAT.PY
# Copyright (c) 2013 Pilgrim Beart <firstname.lastname@1248.io>
#
# A minimal library for working with Hypercat 3.0 catalogues.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import json


try:
    basestring
except NameError:
    basestring = str

REL = "rel"
VAL = "val"

# Catalogue structure
CATALOGUE_METADATA = "catalogue-metadata"    # Name of the array of metadata about the catalogue itself
ITEMS = "items"
HREF = "href"
ITEM_METADATA = "item-metadata" # Name of the array of metadata about each item in the catalogue

# Mandatory relations & types
ISCONTENTTYPE_RELATION = "urn:X-hypercat:rels:isContentType"  # Mandatory for catalogues, but not resources
CATALOGUE_TYPE = "application/vnd.hypercat.catalogue+json"
DESCRIPTION_RELATION = "urn:X-hypercat:rels:hasDescription:en"

# Optional relations & types
SUPPORTS_SEARCH_RELATION = "urn:X-hypercat:rels:supportsSearch"
SUPPORTS_SEARCH_VAL = "urn:X-hypercat:search:simple"
HAS_HOMEPAGE_RELATION = "urn:X-hypercat:rels:hasHomepage"
CONTAINS_CONTENT_TYPE_RELATION = "urn:X-hypercat:rels:containsContentType"

# We manage Catalogues and Resources as raw Python JSON objects (i.e. we construct them in their final form)

class Base:
    # Functionality common to both Catalogues and Resources
    def __init__(self):
        self.metadata = []  # Called either CATALOGUE_METADATA or RESOURCE_METADATA
        self.items = []     # Only for Catalogues. Held as list of instances.
        self.href = None    # Only for Resources

    def addRelation(self, rel, val):
        self.metadata += [{REL:rel, VAL:val}]

    def asJSONstr(self):
        """Return hypercat as a string, of minimum length"""
        return json.dumps(self.asJSON(), sort_keys=True, separators=(',', ':'))

    def setHref(self,href):
        self.href=href

class Hypercat(Base):
    """Create a valid Hypercat catalogue"""
    # Catalogues must be of type catalogue, have a description, and contain at least an empty array of items

    def __init__(self, description):
        super().__init__()
        assert isinstance(description, basestring), "Description argument must be a string"
        self.metadata = [
            { REL:ISCONTENTTYPE_RELATION, VAL:CATALOGUE_TYPE },
            { REL:DESCRIPTION_RELATION, VAL:description }]

    def asJSON(self, asChild=False):
        j = {}
        if(asChild):
            j[HREF] = self.href
            j[ITEM_METADATA] = self.metadata
        else:
            j[CATALOGUE_METADATA] = self.metadata
            j[ITEMS]=[]
            for c in self.items:
                j[ITEMS] += [c.asJSON(asChild=True)]
        return j

    def addItem(self, child, href):
        """Add a new item (a catalogue or resource) as a child of this catalogue."""
        assert isinstance(child, Base), "child must be a hypercat Catalogue or Resource"
        child.setHref(href)
        for item in self.items:
            assert item.href != href, "All items in a catalogue must have unique hrefs : "+href
        self.items += [child]           # Add new
        return

    def items(self):
        return self.items

    def supportsSimpleSearch(self):
        self.addRelation(SUPPORTS_SEARCH_RELATION, SUPPORTS_SEARCH_VAL)

    def hasHomepage(self, url):
        self.addRelation(HAS_HOMEPAGE_RELATION, url)

    def containsContentType(self, contentType):
        self.addRelation(CONTAINS_CONTENT_TYPE_RELATION, contentType)



#md is model dictionary
def createOperatorHypercat(md, modes):
    openT = 'urn:X-opentransport:rels:'
    h = Hypercat("OpenTransport Operator Catalogue")
    h.supportsSimpleSearch()
    no = 0
    for i in md:
        h2 = Hypercat(i['fields']['name'])
        h2.hasHomepage(i['fields']['homepage'])
        h2.addRelation(openT+'hasID', i['pk'])
        h2.addRelation(openT+'hasEmail', i['fields']['email'])
        h2.addRelation(openT+'hasPhone', i['fields']['phone'])
        h2.addRelation(openT+'hasDefaultLanguage', i['fields']['default_language'])
        if i['fields']['modes']:
            h2.addRelation(openT+'hasNumberModes', len(i['fields']['modes']))
            count = 1
            for mode in i['fields']['modes']:
                h2.addRelation(openT+'hasNumberMode'+str(count)+'#Code', mode)
                h2.addRelation(openT+'hasNumberMode'+str(count)+'#Description', modes.get(pk=mode).short_desc)
                count += 1
        h2.addRelation(openT+'hasNumberMIPTAURLs', 1)
        h2.addRelation(openT + 'hasMIPTAURL', i['fields']['miptaurl'])
        h.addItem(h2, i['fields']['api_url'])
        no+=1
    return [h.asJSON()]
#error: unsupported operand type(s) for -: 'str' and 'str'

# if __name__ == '__main__':
    # # Unit tests
    # import unittest
    # unittest.unittest()
