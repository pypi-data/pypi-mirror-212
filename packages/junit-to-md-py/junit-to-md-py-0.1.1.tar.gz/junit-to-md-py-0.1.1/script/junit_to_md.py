#!/usr/bin/env python3
import sys
from lxml import etree
import xml.etree.ElementTree as ET


def junit_to_md(user_input: str):

    failedTestDetails = []
    allTests = []

    try:
        xmlDoc = etree.parse(user_input)
    except ET.ParseError:
        print("Error: junit file parse error.")
        sys.exit(1)

    suites = xmlDoc.xpath("//testsuite")
    for suite in suites:
        tests = suite.xpath(".//testcase")
        for test in tests:
            allTests.append(test)
            failures = test.xpath(".//failure")
            for failure in failures:
                failedTestDetails.append(
                    suite.get("name")
                    + "/"
                    + test.get("name")
                    + "\n\n```\n"
                    + failure.text
                    + "\n```"
                )

    if failedTestDetails:
        returnMsg = "### Test Failures:\n"
        for failure in failedTestDetails:
            returnMsg += "- " + failure + "\n"
        print(returnMsg)
    else:
        print("")
    sys.exit(0)
