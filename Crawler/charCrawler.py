import requests
from lxml import html
from TibiaObjects.character import Character


def crawl(name):
    char = Character(name)
    pageContent = requests.get('http://www.tibia.com/community/?subtopic=characters&name=%s' %name)
    tree = html.fromstring(pageContent.content)

    if not tree.xpath('.//*/tr[contains(td[1], "Name")]/td[2]/text()'):
        return None

    char.level = retrieveData("Level", tree, name)
    char.world = retrieveData("World", tree, name)
    char.voc = retrieveData("Vocation", tree, name)
    char.sex = retrieveData("Sex", tree, name)
    char.achievement = retrieveData("Achievement Points", tree, name)
    char.residence = retrieveData("Residence", tree, name)
    char.guild = retrieveData("Guild", tree, name)


    return char


def retrieveData(attribute, tree, name):
    extra = ""
    try:
        extra = tree.xpath('.//*/tr[contains(td[1], "' + attribute + '")]/td[2]/a/text()')[0]
    except:
        'nothing'
    try:
        print(tree.xpath('.//*/tr[contains(td[1], "' + attribute + '")]/td[2]/text()')[0]+extra)
        return tree.xpath('.//*/tr[contains(td[1], "' + attribute + '")]/td[2]/text()')[0]+extra
    except IndexError as e:
        print(e)
        print(attribute + " for " + name + " not found.")
        return "-"


