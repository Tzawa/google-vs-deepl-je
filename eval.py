#!/usr/bin/env python3

import argparse
import os
import sys
import mojimoji
from janome.tokenizer import Tokenizer
from nltk import word_tokenize
from nltk.translate.bleu_score import sentence_bleu, corpus_bleu

class Segmenter():
    """文を単語(英語と日本語)や文字(中国語)に分割するクラス

    英語はnltk.word_tokenizeを用いて単語に分割する

    日本語はjanomeを用いて形態素に分割する

    中国語は文字単位に分割する

    Args:
        lang (str): 言語の指定 (en/ja/zh)

    Attributes:
        lang (str): 言語の指定 (en/ja/zh)
    """
    def __init__(self, lang="en"):
        self.lang = lang
        if lang == "en":
            self._segmenter = self.en_seg
        elif lang == "ja":
            self._ja_tokenizer = Tokenizer()
            self._segmenter = self.ja_seg
        elif lang == "zh":
            self._segmenter = self.char_seg
        else:
            sys.stderr.write("Invalid langauge: {}\n".format(lang))
            sys.exit()
            
    def __call__(self, fname, mode="hyp"):
        """指定されたファイル内の文を分割

        nltkのbleu計算関数の入力は以下の制約がある

        >>> sentence_bleu([reference1, reference2, reference3], hypothesis1)

        >>> list_of_references = [[ref1a, ref1b, ref1c], [ref2a]]
        >>> hypotheses = [hyp1, hyp2]
        >>> corpus_bleu(list_of_references, hypotheses)

        これに合わせるために、modeがhypの場合とrefの場合とで返り値の型が異なる

        Args:
            fname (str): 分割対象ファイル名
            mode (str): 分割モード指定 (hyp/ref)

        Returns:
            mode = hypの場合はlist、refの場合はlistのlist
        """
        result = []
        with open(fname, "r", encoding="utf8") as f:
            if mode == "hyp":
                for line in f:
                    result.append(self._segmenter(line.strip()))
            elif mode == "ref":
                for line in f:
                    result.append([self._segmenter(line.strip())])
            else:
                sys.stderr.write("Invalid mode: {}\n".format(mode))
                sys.exit()
        return result

    def en_seg(self, line):
        return word_tokenize(line.strip())
    def char_seg(self, line):
        return list(line.strip().replace(" ", "　"))
    def ja_seg(self, line):
        return self._ja_tokenizer.tokenize(mojimoji.han_to_zen(line.strip()).replace(" ", "　"), wakati=True)
    
def calc_bleu(hyp_file, ref_file, lang):
    """BLEUスコアを計算
    
    BLEUスコアは`nltk.translate.bleu_score`の
    `sentence_bleu`もしくは`corpus_bleu`により計算される。
    与えられた文の数が1の場合には自動的に`sentence_bleu`が使われ、
    それ以外の場合は`corpus_bleu`が使われる

    Args:
        hyp_file (str): hypothesis file (翻訳結果ファイル)
        ref_file (str): reference file (正解訳ファイル)
        lang (str): 言語指定 (ja/en/zh)
    """

    segmenter = Segmenter(args.language)
    hyps = segmenter(args.hyp_file, mode="hyp")
    refs = segmenter(args.ref_file, mode="ref")
    if len(hyps) == 1:
        sys.stderr.write("SENTENCE BLEU\n")
        print("{:.3f}".format(sentence_bleu(refs[0], hyps[0])*100.0))
    else:    
        sys.stderr.write("CORPUS BLEU\n")
        print("{:.3f}".format(corpus_bleu(refs, hyps)*100.0))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=os.path.basename(__file__))
    parser.add_argument('hyp_file', help='hypothesis file')
    parser.add_argument('ref_file', help='reference file')
    parser.add_argument('-l', '--language', help='language', default="en")
    args = parser.parse_args()

    calc_bleu(args.hyp_file, args.ref_file, args.language)
