# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
fn = "~/Downloads/out.rtx"
ns = {"doc": "http://schema.redwood.com/report/rtx.xsd"}
# print(pd.options)

# cols = list(str(i) for i in range(1,60))
# cols


# %%
# dfc = pd.read_xml(fn, namespaces = ns, names=cols, xpath="//doc:columns/doc:column")
dfc = pd.read_xml(fn, namespaces = ns, xpath="//doc:columns/doc:column")

# df = pd.read_xml(fn, namespaces = ns)
# dfc.head(10)
cols = list(dfc["name"])
# cols.insert(0, "l",str)
cols.insert(0, "k")

# xsl = \
# '''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:doc="http://schema.redwood.com/report/rtx.xsd">
#     <xsl:output method="xml" omit-xml-declaration="no" indent="yes"/>
#     <xsl:strip-space elements="*"/>

#     <!-- IDENTITY TEMPLATE TO COPY XML AS IS -->
#     <xsl:template match="node()|@*">
#        <xsl:copy>
#          <xsl:apply-templates select="node()|@*"/>
#        </xsl:copy>
#     </xsl:template>
    
#     <!-- ENCLOSE zip NODES WITH DOUBLE QUOTES -->
#     <xsl:template match="doc:r">
#       <xsl:copy>
#         <xsl:variable name="quot">"</xsl:variable>
#         <xsl:value-of select="concat($quot, text(), $quot)"/>
#       </xsl:copy>
#     </xsl:template>
    
# </xsl:stylesheet>'''

# cols


# %%
# dfd = pd.read_xml(fn, namespaces = ns, stylesheet = xsl, names=cols, xpath="//doc:data/doc:r")

dfd = pd.read_xml(fn, namespaces = ns, names=cols, xpath="//doc:data/doc:r")

# df = pd.read_xml(fn, namespaces = ns)
dfd



# %%
