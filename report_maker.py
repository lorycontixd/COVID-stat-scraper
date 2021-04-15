import markdown
import subprocess
import os

class ReportMaker():
    def __init__(self,filename="results/report.html"):
        self.raw_report = ""
        self.filename = filename

    def __create_results_dir(self):
        if not os.path.isdir("results"):
            subprocess.run(["mkdir","results"])

    def append(self,markdowntext):
        self.raw_report += markdowntext

    def compile(self):
        self.__create_results_dir()
        rep = markdown.markdown(self.raw_report)
        file = open(self.filename,"w+")
        file.write(rep)

