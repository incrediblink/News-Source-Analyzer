from bs4 import BeautifulSoup
import json
import glob

def getArticle():
  count = 0
  for article in glob.glob('articles/*.html'):
    f = open(article, "r")
    if f.mode == 'r':
      contents = f.read()
      soup = BeautifulSoup(contents, 'html.parser')
      titles = soup.findAll("span", attrs={ "class": "enHeadline" })
      for title in titles:
        ob = title.parent.next_sibling
        article = ""
        author = None
        while True:
          if not ob or ob.get("id") == "hd":
            temp = None
            for string in title.stripped_strings:
              temp = string

            file = open("data/" + str(count) + ".json", "w")
            file.write(json.dumps({
              "title": temp,
              "author": author,
              "article": article
            }, indent=2, separators=(',', ': ')))
            file.close()
            count += 1
            break
          classes = ob.get("class")
          if classes:
            if classes[0] == "author":
              for string in ob.stripped_strings:
                author = string
            elif classes[0] == "articleParagraph" and ob.string:
              for string in ob.stripped_strings:
                string = string.replace("\n", " ")
                string = string.replace("  ", " ")
                article += string + "\n"
          ob = ob.next_sibling
          while len(type(ob).__bases__) == 2:
            ob = ob.next_sibling
    f.close()
  return

def parseArticle():
  for filename in glob.glob('data/*.json'):
    f = open(filename, "r")
    if f.mode == 'r':
      data = json.loads(f.read())
      article = data.get("article", "")
      sentences = []
      sentence = ""
      quoteCount = 0
      for i in range(0, len(article)):
        char = article[i]
        if (char == " " or char == "\n") and sentence == "":
          pass
        elif quoteCount % 2 > 0 or char != ".":
          sentence += char
        elif char == ".":
          word = ""
          k = i - 1
          while article[k] != " ":
            word = article[k] + word
            k += -1
          if len(word) == 1 or word in { "Mr", "Mrs", "Prof", "Ms", "Sen",
            "Dr", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
            "Sept", "Oct", "Nov", "Dec" }:
            sentence += char
            print(word)
            print(char)
          elif (len(article) <= i + 1 or
            article[i + 1] == " " or
            article[i + 1] == "\n"):
            if len(article) <= i + 2 or article[i + 2].lower() != article[i + 2]:
              sentence += char
              sentences.append(sentence)
              sentence = ""
            else:
              sentence += char
          else:
            sentence += char
      data["sentences"] = sentences
      f.close()
      f = open(filename, "w")
      f.write(json.dumps(data, indent=2, separators=(',', ': ')))
      f.close()
  return

getArticle()
parseArticle()
