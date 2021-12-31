from typing import List
from collections import defaultdict as ddict
from itertools import product

from lxml import etree

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

class CKY():
  def __init__(self, grammer: str) -> None:
    """文法規則を受けとって辞書に格納

    Args:
      grammer (str): 文法規則を一行に一つずつ書く
    """
    self.phrase_structure_rules = ddict(list)
    for line in grammer.strip().split("\n"):
      left, right = map(str.strip, line.split("->"))
      if "|" in right:
        words = right.split("|")
        for word in words:
          self.phrase_structure_rules[word].append(left)
      else:
        self.phrase_structure_rules[right].append(left)

  def _init_cky_table(self, length: int) -> List:
    """(length, length)のリストの各要素を[]で初期化

    Args:
        length (int): 入力系列の長さ
    """
    return [[[] for _ in range(length)] for _ in range(length)]

  def _generate_result(self)->List:
    """analayze()実行後に結果をxmlにエンコードして返却

    Returns:
        List: 結果のリスト、解析失敗の場合は空のリスをを返却
    """
    res = []
    for i, candidate in enumerate(self.cky_table[0][self.length-1]):
      if candidate[0] != "S":
        pass
      else:
        res.append(self._create_tree((0, self.length-1, i)))
    return res

  def _create_tree(self, index=(0,0,0)):
    i, j, k = index
    node = self.cky_table[i][j][k]
    elem = etree.Element(node[0], attrib=None, nsmap=None)
    child = node[1:]

    if len(child) == 1:
      elem.text = child[0]
      return elem
    else:
      first, second = child
      elem.append(self._create_tree(index=first[:3]))
      elem.append(self._create_tree(index=second[:3]))
      return elem

  def analyze(self, sentence: str)->List:
    tokens = sentence.split()
    self.length = len(tokens)
    self.cky_table = self._init_cky_table(self.length)

    # ckyテーブルの対角線を初期化
    for i, word in enumerate(tokens):
      for left in self.phrase_structure_rules[word]:
        # "N -> I"のような関係を(N, I)として記録
        self.cky_table[i][i].append((left, word))

    # 対角線から一つずつずらしていく
    for d in range(1,self.length): # [0, self.length)
      # 斜め下に進んでいく
      for i in range (self.length-d): # [0, self.length-d)
        j = i + d
        candidate = []
        for k in range(i, j): # [i, j)
          for a, b in product(range(len(self.cky_table[i][k])),
                              range(len(self.cky_table[k+1][j]))):
            candidate.append((a,b))
            # 左辺はタプルの一番左に記録
            key = f"{self.cky_table[i][k][a][0]} {self.cky_table[k+1][j][b][0]}"

            for left in self.phrase_structure_rules[key]:
              first, second = key.split()
              first, second = (i,k,a,first), (k+1,j,b,second)
              self.cky_table[i][j].append((left, first, second))
    return self._generate_result()


def main():
  cky = CKY(grammer)
  res = cky.analyze(sentence)
  for i, item in enumerate(res):
    print(f"解析結果{i+1}")
    print(etree.tostring(item, pretty_print=True).decode())

if __name__ == "__main__":
  main()
