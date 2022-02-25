<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:foo="foo.bar/"
    version="1.0">
    <xsl:output method="text"/>
    <xsl:template match="tei:TEI">
        <xsl:apply-templates select=".//tei:body"/>
    </xsl:template> 
    <xsl:template match="tei:body">
        <xsl:apply-templates select="tei:div"/>
    </xsl:template> 
    <xsl:template match="tei:corr"/>
    <xsl:template match="tei:div">
        <xsl:apply-templates/>
    </xsl:template>
    <xsl:template match="tei:pb">
        <xsl:text>[Page]
</xsl:text>
    </xsl:template>
    <xsl:template match="tei:lb">
        <xsl:text>
</xsl:text>
    </xsl:template>
        <xsl:template match="tei:p">
            <xsl:text>
</xsl:text>
            <xsl:apply-templates />
            <xsl:text>
</xsl:text>
    </xsl:template>
    <xsl:template match="tei:dateline|tei:signed">
            <xsl:text>
</xsl:text>
            <xsl:apply-templates />
    </xsl:template>
    <xsl:template match="text()">
        <xsl:value-of select="foo:spaces(.)"/>  
    </xsl:template>
    
</xsl:stylesheet>