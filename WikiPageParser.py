import os
import yaml
from pathlib import Path
import sys

class WikiPageParser:

    def __init__(self):
        self.totalPage = ""
        self.totalPages = []
        self.debugPrint = False
        self.availablePages = set()

    def printInfo(self, msg):
        if self.debugPrint:
            print(msg)

    def processYamlData(self, data):
        self.printInfo(data["type"])
        if data["type"] == "text":
            self.totalPage += data["text"]
            self.printInfo(data["text"])

        elif data["type"] == "internalreference":
            targetLinkAddress = data["target"][0]["text"]
            targetCaption = targetLinkAddress
            if "caption" in data and len(data["caption"]) > 0:
                targetCaption = data["caption"][0]["text"]

            # Avoid spaces in filenames.
            targetLinkAddress = targetLinkAddress.replace(" ", "_")

            # Check if the target exists
            exists = targetLinkAddress in self.availablePages
            cssClass = ' class="missing-page"' if not exists else ""

            self.totalPage += f'<a href="{targetLinkAddress}.html"{cssClass}>{targetCaption}</a>'

        elif data["type"] == "heading":
            depth = str(data["depth"])
            self.totalPage += f"\n\n<h{depth}>{data['caption'][0]['text']}</h{depth}>\n\n"
            for i in data["content"]:
                self.processYamlData(i)

        elif data["type"] == "paragraph":
            if "content" not in data:
                return
            self.totalPage += "<p>"
            for i in data["content"]:
                self.printInfo(i)
                self.processYamlData(i)
            self.totalPage += "</p>"

        elif data["type"] == "list":
            if "content" not in data:
                return
            self.totalPage += "<ul>"
            for i in data["content"]:
                self.printInfo(i)
                self.processYamlData(i)
            self.totalPage += "</ul>"

        elif data["type"] == "listitem":
            if "content" not in data:
                return
            self.totalPage += "<li>"
            for i in data["content"]:
                self.printInfo(i)
                self.processYamlData(i)
            self.totalPage += "</li>"

        elif data["type"] == "formatted":
            if "content" not in data:
                return
            self.totalPage += "<b>"
            for i in data["content"]:
                self.printInfo(i)
                self.processYamlData(i)
            self.totalPage += "</b>"

        elif data["type"] == "externalreference":
            if "target" not in data:
                return
            linkTarget = data["target"]
            caption = data["caption"][0]["text"]
            self.totalPage += f'<a href="{linkTarget}">{caption}</a>'

        else:
            self.printInfo("Ignoring tag")

    def scanAvailablePages(self, dirPath):
        """Scan directory for YAML files and store their page names."""
        for file in os.listdir(dirPath):
            if file.endswith(".yaml"):
                name = Path(file).stem  # strip .yaml
                idx = name.find(".")
                if idx != -1:
                    name = name[:idx]
                self.availablePages.add(name.replace(" ", "_"))

    def processDirectory(self, dirPath):
        """Scan all .yaml files and then process each one into HTML."""
        self.scanAvailablePages(dirPath)
        for file in os.listdir(dirPath):
            if file.endswith(".yaml"):
                targetFile = os.path.join(dirPath, file)
                print(targetFile)
                pageTitle = Path(file).name
                idx = pageTitle.find(".")
                pageTitle = pageTitle[:idx]
                self.processYamlFile(targetFile, pageTitle)

    def createPageWrapper(self, title, content):
        """Create the standard wiki page wrapper with div headers."""
        page = '<div id="content" class="mw-body" role="main">'
        page += f'<h1 id="firstHeading" class="firstHeading">{title}</h1>'
        page += '<div id="bodyContent" class="mw-body-content">'
        page += '<div id="mw-content-text" dir="ltr" class="mw-content-ltr" lang="en-GB">'
        page += '<div class="mw-parser-output">'
        page += content
        page += '</div></div></div></div>'
        return page

    def generateAllPagesIndex(self):
        """Generate an alphabetically sorted index of all pages."""
        # Sort pages alphabetically by title
        sortedPages = sorted(self.totalPages, key=lambda x: x[0].lower())

        # Build the content
        content = '<p>This page lists all available pages in alphabetical order.</p>'
        content += '<ul>'
        for pageTitle, _ in sortedPages:
            displayTitle = pageTitle.replace("_", " ")
            content += f'<li><a href="{pageTitle}.html">{displayTitle}</a></li>'
        content += '</ul>'

        return self.createPageWrapper("All Pages", content)

    def outputToDirectory(self, outDir, htmlGenerator):
        for i in self.totalPages:
            pathName = os.path.join(outDir, i[0] + ".html")
            with open(pathName, "w") as text_file:
                staticHtml = htmlGenerator.genForPage(i[0], i[1])
                text_file.write(staticHtml)

        # Generate and write the All Pages index
        allPagesContent = self.generateAllPagesIndex()
        allPagesPath = os.path.join(outDir, "All_Pages.html")
        with open(allPagesPath, "w") as text_file:
            staticHtml = htmlGenerator.genForPage("All_Pages", allPagesContent)
            text_file.write(staticHtml)

    def processYamlFile(self, filePath, pageTitle):
        strippedTitle = os.path.splitext(pageTitle)[0]
        self.totalPage = '<div id="content" class="mw-body" role="main">'
        self.totalPage += f'<h1 id="firstHeading" class="firstHeading">{strippedTitle.replace("_", " ")}</h1>'
        self.totalPage += '<div id="bodyContent" class="mw-body-content">'
        self.totalPage += '<div id="mw-content-text" dir="ltr" class="mw-content-ltr" lang="en-GB">'
        self.totalPage += '<div class="mw-parser-output">'
        with open(filePath, "r") as stream:
            try:
                yamlData = yaml.safe_load(stream)
                if "content" not in yamlData:
                    return
                for i in yamlData["content"]:
                    self.processYamlData(i)
                self.printInfo("\n\nfinal text")
                self.printInfo(self.totalPage)
            except yaml.YAMLError as exc:
                print(exc)
        self.totalPage += '</div></div></div>'
        self.totalPages.append((strippedTitle, self.totalPage))