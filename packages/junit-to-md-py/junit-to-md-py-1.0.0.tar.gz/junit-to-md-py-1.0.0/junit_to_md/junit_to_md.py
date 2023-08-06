from lxml import etree

def junit_to_md(user_input):
    failedTestDetails = []
    allTests = []

    try:
        xmlDoc = etree.parse(user_input)
    except Exception:
        print(f"Error parsing the text from junitOutput!")
        return

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
