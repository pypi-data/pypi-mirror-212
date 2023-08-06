#!/usr/bin/env python3
import sys
from lxml import etree


def main(user_input: str):

    if len(sys.argv) < 2:
        print("Error: junit file text argument is missing.")
        print('Usage: python main.py "some text"')
        sys.exit(1)

    user_input = sys.argv[1]

    failedTestDetails = []
    allTests = []

    xmlDoc = etree.parse(user_input)
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
