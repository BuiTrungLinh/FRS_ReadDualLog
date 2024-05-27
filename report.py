import base64
import datetime as dt
import jinja2
import requests


def report_dualtest(dataList, totalPassed, totalMisread, totalNoread, outputPath, interface):
    # Step 1 - create jinja template object from file
    template = jinja2.Environment(
        loader=jinja2.FileSystemLoader("./templates"),
    ).get_template("report_template.html")

    # Step 2 - create data for report
    todayStr = dt.datetime.now().strftime("%H%M%S-%d-%b-%y")

    # create logo image
    with open("images/datalogic_logo.png", "rb") as f:
        logoImg = base64.b64encode(f.read()).decode()

    data = {}
    context = {
        "reportDtStr": todayStr,
        "dataTblRows": enumerate(dataList),
        "logoImg": logoImg,
        "totalDataPassed": totalPassed,
        "totalDataMisread": totalMisread,
        "totalDataNoread": totalNoread,
        "interface": interface,
        "bootstrapCss": requests.get("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css").text,
        "bootstrapJs": requests.get("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js").text
    }

    # Step 3 - render data in jinja template
    reportText = template.render(context)

    # Step 4 - Save genereate text as an HTML file
    pathOutput = f"./reports/dual_report_{todayStr}.html"
    if outputPath != '':
        pathOutput = f"{outputPath}/dual_report_{todayStr}.html"

    with open(pathOutput, mode='w') as f:
        f.write(reportText)
    # print("Report_File: {}".format(pathOutput))
    return pathOutput
