class WikiPageHtmlGenerator:

    def __init__(self, footer=None, gitHash=None):
        self.footer=footer
        self.gitHash=gitHash

    '''
    Generate page data for a single parsed page.
    '''
    def genForPage(self, title, pageContent):
        out=""
        out+=("<html>\n")
        if self.gitHash:
            out+=f"<!-- {self.gitHash} -->\n"
        out+=("<head>\n")
        out+=('<meta charset="UTF-8">\n')
        out+=('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
        out+=("<title>"+title.replace("_", " ")+"</title>\n")
        out+=('<link rel="stylesheet" href="styles.css">')
        out+=("</head>\n")
        out+=("<body>\n")
        out+=('<script src="script.js"></script>\n')
        out+=('<div id="mw-page-base" class="noprint"></div>\n')
        out+=('<div id="mw-head-base" class="noprint"></div>')
        out+='''<button class="menu-toggle" onclick="toggleMenu()" aria-label="Toggle menu">&#9776;</button>
<div class="sidenav" id="sidenav">
<div class="sidenav-inner">
<ul class="sidenav-list">
<li class="sidenav-li"><a href="Main_Page.html">Main page</a></li>
<li class="sidenav-li"><a href="" onclick="return randomPage();">Random page</a></li>
<li class="sidenav-li"><a href="All_Pages.html">All Pages</a></li>
</ul>
</div>
</div>'''

        out+=(pageContent)

        out+=("</div>\n")
        out+=("</body>\n")
        if self.footer:
            out+=f"<footer><p>{self.footer}</p></footer>\n"
        out+=("</html>\n")

        return out

    '''
    Write the stylesheet out to the filesystem.
    '''
    def writeStyleSheet(self, path):
        text = '''
.mw-body h1, .mw-body-content h1, .mw-body-content h2 {
    margin-bottom: 0.25em;
    padding: 0;
    font-family: 'Linux Libertine','Georgia','Times',serif;
    line-height: 1.3;
}

h1 {
    font-size: 188%;
    font-weight: normal;
}

h1, h2 {
    margin-bottom: 0.6em;
    border-bottom: 1px solid #a2a9b1;
}

h1, h2, h3, h4, h5, h6 {
    color: #000;
    margin: 0;
    margin-bottom: 0px;
    padding-top: 0.5em;
    padding-bottom: 0.17em;
    overflow: hidden;
}

h2 {
    font-size: 150%;
    font-weight: normal;
}

html, body {
    font-family: sans-serif;
    background-color: #fff;
    color: #202122;
}

html {
    font-size: 100%;
}

.mw-body h1, .mw-body-content h1 {
    font-size: 1.8em;
}

.mw-body .firstHeading {
    overflow: visible;
}

p {
    margin: 0.4em 0 0.5em 0;
}

.mw-body-content p {
    margin: 0.5em 0;
}

.mw-content-ltr {
    direction: ltr;
}

.mw-body-content {
    font-size: 0.875em;
    font-size: calc(1em * 0.875);
    line-height: 1.6;
}

.mw-body, .parsoid-body {
    color: #202122;
    direction: ltr;
}

#mw-head {
    position: absolute;
    top: 0;
    right: 0;
    width: 100%;
}

li {
    margin-bottom: 0.1em;
}

.mw-content-ltr ul, .mw-content-rtl .mw-content-ltr ul {
    margin: 0.3em 0 0 1.6em;
    padding: 0;
}

ul {
    margin: 0.3em 0 0 1.6em;
    padding: 0;
    padding-top: 0px;
}

a.missing-page { color: #bf3c2c; }

.menu-toggle {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    width: 100%;
    z-index: 1000;
    background: #eee;
    border: none;
    border-bottom: 1px solid #ccc;
    padding: 12px 15px;
    font-size: 20px;
    cursor: pointer;
    text-align: left;
}

.sidenav {
    width: 180px;
    position: fixed;
    z-index: 999;
    top: 20px;
    left: 10px;
    background: #eee;
    overflow-x: hidden;
    padding: 8px 0;
    transition: transform 0.3s ease;
}

.sidenav a {
    display: block;
    color: inherit;
    text-decoration: none;
}

.sidenav a:hover {
    color: #064579;
}

#content, footer {
    margin-left: 200px;
}

ul.sidenav-list {
    list-style: none none;
    margin: 0;
}

li.sidenav-li {
    margin: 0;
    padding: 0.25em 0;
    font-size: 0.75em;
    line-height: 1.125em;
    word-wrap: break-word;
}

div.sidenav-inner {
    margin-left: 0.5em;
    padding-top: 0;
}

footer {
    color: #606060;
    margin-top: 30px;
    font-size: calc(1em * 0.875);
    line-height: 1.6;
}

/* ===== DARK MODE ===== */
@media (prefers-color-scheme: dark) {
    html, body {
        background-color: #1a1a1a;
        color: #e5e5e5;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #fff;
        border-bottom-color: #444;
    }

    .mw-body, .parsoid-body {
        color: #e5e5e5;
    }

    a {
        color: #82b1ff;
        text-decoration: none;
    }

    a:hover, a:focus {
        color: #a7c8ff;
        text-decoration: underline;
    }

    .sidenav {
        background: #2a2a2a;
    }

    .sidenav a {
        color: #d0d0d0;
    }

    .sidenav a:hover {
        color: #82b1ff;
    }

    .menu-toggle {
        background: #2a2a2a;
        border-bottom-color: #444;
        color: #e5e5e5;
    }

    footer {
        color: #aaaaaa;
    }
}

/* ===== MOBILE RESPONSIVE ===== */
@media screen and (max-width: 768px) {
    .menu-toggle {
        display: block;
    }

    .sidenav {
        top: 45px;
        left: 0;
        height: calc(100% - 45px);
        transform: translateX(-100%);
        box-shadow: 2px 0 5px rgba(0,0,0,0.3);
    }

    .sidenav.active {
        transform: translateX(0);
    }

    #content, footer {
        margin-left: 10px;
        margin-right: 10px;
        margin-top: 55px;
    }

    .mw-body-content {
        font-size: 1em;
    }

    h1 {
        font-size: 150%;
    }

    h2 {
        font-size: 130%;
    }

    .mw-body h1, .mw-body-content h1 {
        font-size: 1.5em;
    }

    li.sidenav-li {
        font-size: 0.85em;
        padding: 0.4em 0;
    }
}

@media screen and (max-width: 480px) {
    html {
        font-size: 90%;
    }

    h1 {
        font-size: 140%;
    }

    h2 {
        font-size: 120%;
    }

    .mw-body h1, .mw-body-content h1 {
        font-size: 1.4em;
    }

    #content, footer {
        margin-left: 5px;
        margin-right: 5px;
    }
}

        '''
        print("Writing stylesheet to %s" % path)
        with open(path, "w") as text_file:
            text_file.write(text)

    def writeJavascript(self, path, totalPages):
        text = '''
function randomPage(){
    let items = ['''

        for i in totalPages:
            text += '"' + i[0] + '.html",'

        text += '''];
    console.log("Going to random page");
    var item = items[Math.floor(Math.random()*items.length)];
    window.location.href = item;
    return false;
}

function toggleMenu() {
    const sidenav = document.getElementById('sidenav');
    sidenav.classList.toggle('active');
}

// Close menu when clicking outside on mobile
document.addEventListener('click', function(event) {
    const sidenav = document.getElementById('sidenav');
    const menuToggle = document.querySelector('.menu-toggle');

    if (window.innerWidth <= 768) {
        if (!sidenav.contains(event.target) && !menuToggle.contains(event.target)) {
            sidenav.classList.remove('active');
        }
    }
});
        '''
        print("Writing javascript to %s" % path)
        with open(path, "w") as text_file:
            text_file.write(text)