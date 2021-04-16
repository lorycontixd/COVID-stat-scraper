import markdown
import subprocess
import os
from modules import mylogger as ml
import jinja2
from pathlib import Path

class ReportMaker():
    def __init__(self,base_path="results/",file="report.html"):
        self.base_path = base_path
        self.file = file
        self.filename = os.path.join(self.base_path,self.file)
        self.l = ml.Logger()
        self.report = ""

    def __create_results_dir(self):
        if not os.path.isdir("results"):
            subprocess.run(["mkdir","results"])

    def __create_header(self):
        """
Creates HTML header for report
"""

    def append_text(self,markdowntext,append_newline=True,**kwargs):
        template = jinja2.Template(markdowntext)
        expanded_text = template.render(**kwargs)
        self.report += expanded_text
        if append_newline:
            self.report += "\n\n"

    def compile(self):
        self.__create_results_dir()
        rep = markdown.markdown(self.report)
        file = open(self.filename,"w+")
        file.write(rep)
        self.l.info(f"Report written succesfully to {self.filename}!")


