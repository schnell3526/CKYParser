from cky import CKY

from lxml import etree

def main():
  sentence = "I saw a girl with a telescope"

  grammer = """
  S -> NP VP
  NP -> DET N
  NP -> NP PP
  VP -> V NP
  VP -> VP PP
  PP -> PREP NP
  N -> I|girl|telescope
  NP -> I|girl|telescope
  V -> saw
  VP -> saw
  DET -> a
  PREP -> with
  """

  cky = CKY(grammer)
  res = cky.analyze(sentence)
  for i, item in enumerate(res):
    print(f"解析結果{i+1}")
    print(etree.tostring(item, pretty_print=True).decode())

if __name__ == "__main__":
  main()
