import re
from core.unified_template.num2text import Num2Text


class Num2Ordinal:
    orders = {3: {"m": {"nomn": "тысячный", "gent": "тысячного"},
                  "f": {"nomn": "тысячная", "gent": "тысячной"},
                  "n": {"nomn": "тысячное", "gent": "тысячного"}},
              6: {"m": {"nomn": "миллионный", "gent": "миллионного"},
                  "f": {"nomn": "миллионная", "gent": "миллионной"},
                  "n": {"nomn": "миллионное", "gent": "миллионного"}},
              9: {"m": {"nomn": "миллиардный", "gent": "миллиардного"},
                  "f": {"nomn": "миллиардная", "gent": "миллиардной"},
                  "n": {"nomn": "миллиардное", "gent": "миллиардного"}},
              12: {"m": {"nomn": "триллионный", "gent": "триллионного"},
                   "f": {"nomn": "триллионная", "gent": "триллионной"},
                   "n": {"nomn": "триллионное", "gent": "триллионного"}},
              15: {"m": {"nomn": "квадриллионный", "gent": "квадриллионного"},
                   "f": {"nomn": "квадриллионная", "gent": "квадриллионной"},
                   "n": {"nomn": "квадриллионное", "gent": "квадриллионного"}},
              18: {"m": {"nomn": "квадриллионный", "gent": "квадриллионного"},
                   "f": {"nomn": "квадриллионная", "gent": "квадриллионной"},
                   "n": {"nomn": "квадриллионное", "gent": "квадриллионного"}},
              21: {"m": {"nomn": "секстиллионный", "gent": "секстиллионного"},
                   "f": {"nomn": "секстиллионная", "gent": "секстиллионной"},
                   "n": {"nomn": "секстиллионное", "gent": "секстиллионного"}}}
    before_orders = {1: {"m": {"nomn": "одно", "gent": "одно"},
                         "f": {"nomn": "одно", "gent": "одно"},
                         "n": {"nomn": "одно", "gent": "одно"}},
                     2: {"m": {"nomn": "двух", "gent": "двух"},
                         "f": {"nomn": "двух", "gent": "двух"},
                         "n": {"nomn": "двух", "gent": "двух"}},
                     3: {"m": {"nomn": "трёх", "gent": "трёх"},
                         "f": {"nomn": "трёх", "gent": "трёх"},
                         "n": {"nomn": "трёх", "gent": "трёх"}},
                     4: {"m": {"nomn": "четырёх", "gent": "четырёх"},
                         "f": {"nomn": "четырёх", "gent": "четырёх"},
                         "n": {"nomn": "четырёх", "gent": "четырёх"}},
                     5: {"m": {"nomn": "пяти", "gent": "пяти"},
                         "f": {"nomn": "пяти", "gent": "пяти"},
                         "n": {"nomn": "пяти", "gent": "пяти"}},
                     6: {"m": {"nomn": "шести", "gent": "шести"},
                         "f": {"nomn": "шести", "gent": "шести"},
                         "n": {"nomn": "шести", "gent": "шести"}},
                     7: {"m": {"nomn": "семи", "gent": "семи"},
                         "f": {"nomn": "семи", "gent": "семи"},
                         "n": {"nomn": "семи", "gent": "семи"}},
                     8: {"m": {"nomn": "восьми", "gent": "восьми"},
                         "f": {"nomn": "восьми", "gent": "восьми"},
                         "n": {"nomn": "восьми", "gent": "восьми"}},
                     9: {"m": {"nomn": "девяти", "gent": "девяти"},
                         "f": {"nomn": "девяти", "gent": "девяти"},
                         "n": {"nomn": "девяти", "gent": "девяти"}},
                     10: {"m": {"nomn": "десяти", "gent": "десяти"},
                          "f": {"nomn": "десяти", "gent": "десяти"},
                          "n": {"nomn": "десяти", "gent": "десяти"}},
                     11: {"m": {"nomn": "одиннадцати", "gent": "одиннадцати"},
                          "f": {"nomn": "одиннадцати", "gent": "одиннадцати"},
                          "n": {"nomn": "одиннадцати", "gent": "одиннадцати"}},
                     12: {"m": {"nomn": "двенадцати", "gent": "двенадцати"},
                          "f": {"nomn": "двенадцати", "gent": "двенадцати"},
                          "n": {"nomn": "двенадцати", "gent": "двенадцати"}},
                     13: {"m": {"nomn": "тринадцати", "gent": "тринадцати"},
                          "f": {"nomn": "тринадцати", "gent": "тринадцати"},
                          "n": {"nomn": "тринадцати", "gent": "тринадцати"}},
                     14: {"m": {"nomn": "четырнадцати", "gent": "четырнадцати"},
                          "f": {"nomn": "четырнадцати", "gent": "четырнадцати"},
                          "n": {"nomn": "четырнадцати", "gent": "четырнадцати"}},
                     15: {"m": {"nomn": "пятнадцати", "gent": "пятнадцати"},
                          "f": {"nomn": "пятнадцати", "gent": "пятнадцати"},
                          "n": {"nomn": "пятнадцати", "gent": "пятнадцати"}},
                     16: {"m": {"nomn": "шестнадцати", "gent": "шестнадцати"},
                          "f": {"nomn": "шестнадцати", "gent": "шестнадцати"},
                          "n": {"nomn": "шестнадцати", "gent": "шестнадцати"}},
                     17: {"m": {"nomn": "семнадцати", "gent": "семнадцати"},
                          "f": {"nomn": "семнадцати", "gent": "семнадцати"},
                          "n": {"nomn": "семнадцати", "gent": "семнадцати"}},
                     18: {"m": {"nomn": "восемнадцати", "gent": "восемнадцати"},
                          "f": {"nomn": "восемнадцати", "gent": "восемнадцати"},
                          "n": {"nomn": "восемнадцати", "gent": "восемнадцати"}},
                     19: {"m": {"nomn": "девятнадцати", "gent": "девятнадцати"},
                          "f": {"nomn": "девятнадцати", "gent": "девятнадцати"},
                          "n": {"nomn": "девятнадцати", "gent": "девятнадцати"}},
                     20: {"m": {"nomn": "двадцати", "gent": "двадцати"},
                          "f": {"nomn": "двадцати", "gent": "двадцати"},
                          "n": {"nomn": "двадцати", "gent": "двадцати"}},
                     30: {"m": {"nomn": "тридцати", "gent": "тридцати"},
                          "f": {"nomn": "тридцати", "gent": "тридцати"},
                          "n": {"nomn": "тридцати", "gent": "тридцати"}},
                     40: {"m": {"nomn": "сороко", "gent": "сороко"},
                          "f": {"nomn": "сороко", "gent": "сороко"},
                          "n": {"nomn": "сороко", "gent": "сороко"}},
                     50: {"m": {"nomn": "пятидесяти", "gent": "пятидесяти"},
                          "f": {"nomn": "пятидесяти", "gent": "пятидесяти"},
                          "n": {"nomn": "пятидесяти", "gent": "пятидесяти"}},
                     60: {"m": {"nomn": "шестидесяти", "gent": "шестидесяти"},
                          "f": {"nomn": "шестидесяти", "gent": "шестидесяти"},
                          "n": {"nomn": "шестидесяти", "gent": "шестидесяти"}},
                     70: {"m": {"nomn": "семидесяти", "gent": "семидесяти"},
                          "f": {"nomn": "семидесяти", "gent": "семидесяти"},
                          "n": {"nomn": "семидесяти", "gent": "семидесяти"}},
                     80: {"m": {"nomn": "восьмидесяти", "gent": "восьмидесяти"},
                          "f": {"nomn": "восьмидесяти", "gent": "восьмидесяти"},
                          "n": {"nomn": "восьмидесяти", "gent": "восьмидесяти"}},
                     90: {"m": {"nomn": "девяносто", "gent": "девяносто"},
                          "f": {"nomn": "девяносто", "gent": "девяносто"},
                          "n": {"nomn": "девяносто", "gent": "девяносто"}},
                     100: {"m": {"nomn": "сто", "gent": "сто"},
                           "f": {"nomn": "сто", "gent": "сто"},
                           "n": {"nomn": "сто", "gent": "сто"}},
                     200: {"m": {"nomn": "двухсот", "gent": "двухсот"},
                           "f": {"nomn": "двухсот", "gent": "двухсот"},
                           "n": {"nomn": "двухсот", "gent": "двухсот"}},
                     300: {"m": {"nomn": "трехсот", "gent": "трехсот"},
                           "f": {"nomn": "трехсот", "gent": "трехсот"},
                           "n": {"nomn": "трехсот", "gent": "трехсот"}},
                     400: {"m": {"nomn": "четырёхсот", "gent": "четырёхсот"},
                           "f": {"nomn": "четырёхсот", "gent": "четырёхсот"},
                           "n": {"nomn": "четырёхсот", "gent": "четырёхсот"}},
                     500: {"m": {"nomn": "пятисот", "gent": "пятисот"},
                           "f": {"nomn": "пятисот", "gent": "пятисот"},
                           "n": {"nomn": "пятисот", "gent": "пятисот"}},
                     600: {"m": {"nomn": "шестисот", "gent": "шестисот"},
                           "f": {"nomn": "шестисот", "gent": "шестисот"},
                           "n": {"nomn": "шестисот", "gent": "шестисот"}},
                     700: {"m": {"nomn": "семисот", "gent": "семисот"},
                           "f": {"nomn": "семисот", "gent": "семисот"},
                           "n": {"nomn": "семисот", "gent": "семисот"}},
                     800: {"m": {"nomn": "восьмисот", "gent": "восьмисот"},
                           "f": {"nomn": "восьмисот", "gent": "восьмисот"},
                           "n": {"nomn": "восьмисот", "gent": "восьмисот"}},
                     900: {"m": {"nomn": "девятисот", "gent": "девятисот"},
                           "f": {"nomn": "девятисот", "gent": "девятисот"},
                           "n": {"nomn": "девятисот", "gent": "девятисот"}}}
    structured = {0: {"m": {"nomn": "нулевой", "gent": "нулевого"},
                      "f": {"nomn": "нулевая", "gent": "нулевой"},
                      "n": {"nomn": "нулевое", "gent": "нулевого"}},
                  1: {"m": {"nomn": "первый", "gent": "первого"},
                      "f": {"nomn": "первая", "gent": "первой"},
                      "n": {"nomn": "первое", "gent": "первого"}},
                  2: {"m": {"nomn": "второй", "gent": "второго"},
                      "f": {"nomn": "вторая", "gent": "второй"},
                      "n": {"nomn": "второе", "gent": "второго"}},
                  3: {"m": {"nomn": "третий", "gent": "третьего"},
                      "f": {"nomn": "третья", "gent": "третьей"},
                      "n": {"nomn": "третье", "gent": "третьего"}},
                  4: {"m": {"nomn": "четвёртый", "gent": "четвёртого"},
                      "f": {"nomn": "четвёртая", "gent": "четвёртой"},
                      "n": {"nomn": "четвёртое", "gent": "четвёртого"}},
                  5: {"m": {"nomn": "пятый", "gent": "пятого"},
                      "f": {"nomn": "пятая", "gent": "пятой"},
                      "n": {"nomn": "пятое", "gent": "пятого"}},
                  6: {"m": {"nomn": "шестой", "gent": "шестого"},
                      "f": {"nomn": "шестая", "gent": "шестой"},
                      "n": {"nomn": "шестое", "gent": "шестого"}},
                  7: {"m": {"nomn": "седьмой", "gent": "седьмого"},
                      "f": {"nomn": "седьмая", "gent": "седьмой"},
                      "n": {"nomn": "седьмое", "gent": "седьмого"}},
                  8: {"m": {"nomn": "восьмой", "gent": "восьмого"},
                      "f": {"nomn": "восьмая", "gent": "восьмой"},
                      "n": {"nomn": "восьмое", "gent": "восьмого"}},
                  9: {"m": {"nomn": "девятый", "gent": "девятого"},
                      "f": {"nomn": "девятая", "gent": "девятой"},
                      "n": {"nomn": "девятое", "gent": "девятого"}},
                  10: {"m": {"nomn": "десятый", "gent": "десятого"},
                       "f": {"nomn": "десятая", "gent": "десятой"},
                       "n": {"nomn": "десятое", "gent": "десятого"}},
                  11: {"m": {"nomn": "одиннадцатый", "gent": "одиннадцатого"},
                       "f": {"nomn": "одиннадцатая", "gent": "одиннадцатой"},
                       "n": {"nomn": "одиннадцатое", "gent": "одиннадцатого"}},
                  12: {"m": {"nomn": "двенадцатый", "gent": "двенадцатого"},
                       "f": {"nomn": "двенадцатая", "gent": "двенадцатой"},
                       "n": {"nomn": "двенадцатое", "gent": "двенадцатого"}},
                  13: {"m": {"nomn": "тринадцатый", "gent": "тринадцатого"},
                       "f": {"nomn": "тринадцатая", "gent": "тринадцатой"},
                       "n": {"nomn": "тринадцатое", "gent": "тринадцатого"}},
                  14: {"m": {"nomn": "четырнадцатый", "gent": "четырнадцатого"},
                       "f": {"nomn": "четырнадцатая", "gent": "четырнадцатой"},
                       "n": {"nomn": "четырнадцатое", "gent": "четырнадцатого"}},
                  15: {"m": {"nomn": "пятнадцатый", "gent": "пятнадцатого"},
                       "f": {"nomn": "пятнадцатая", "gent": "пятнадцатой"},
                       "n": {"nomn": "пятнадцатое", "gent": "пятнадцатого"}},
                  16: {"m": {"nomn": "шестнадцатый", "gent": "шестнадцатого"},
                       "f": {"nomn": "шестнадцатая", "gent": "шестнадцатой"},
                       "n": {"nomn": "шестнадцатое", "gent": "шестнадцатого"}},
                  17: {"m": {"nomn": "семнадцатый", "gent": "семнадцатого"},
                       "f": {"nomn": "семнадцатая", "gent": "семнадцатой"},
                       "n": {"nomn": "семнадцатое", "gent": "семнадцатого"}},
                  18: {"m": {"nomn": "восемнадцатый", "gent": "восемнадцатого"},
                       "f": {"nomn": "восемнадцатая", "gent": "восемнадцатой"},
                       "n": {"nomn": "восемнадцатое", "gent": "восемнадцатого"}},
                  19: {"m": {"nomn": "девятнадцатый", "gent": "девятнадцатого"},
                       "f": {"nomn": "девятнадцатая", "gent": "девятнадцатой"},
                       "n": {"nomn": "девятнадцатое", "gent": "девятнадцатого"}},
                  20: {"m": {"nomn": "двадцатый", "gent": "двадцатого"},
                       "f": {"nomn": "двадцатая", "gent": "двадцатой"},
                       "n": {"nomn": "двадцатое", "gent": "двадцатого"}},
                  30: {"m": {"nomn": "тридцатый", "gent": "тридцатого"},
                       "f": {"nomn": "тридцатая", "gent": "тридцатой"},
                       "n": {"nomn": "тридцатое", "gent": "тридцатого"}},
                  40: {"m": {"nomn": "сороковой", "gent": "сорокового"},
                       "f": {"nomn": "сороковая", "gent": "сороковой"},
                       "n": {"nomn": "сороковое", "gent": "сорокового"}},
                  50: {"m": {"nomn": "пятидесятый", "gent": "пятидесятого"},
                       "f": {"nomn": "пятидесятая", "gent": "пятидесятой"},
                       "n": {"nomn": "пятидесятое", "gent": "пятидесятого"}},
                  60: {"m": {"nomn": "шестидесятый", "gent": "шестидесятого"},
                       "f": {"nomn": "шестидесятая", "gent": "шестидесятой"},
                       "n": {"nomn": "шестидесятое", "gent": "шестидесятого"}},
                  70: {"m": {"nomn": "семидесятый", "gent": "семидесятого"},
                       "f": {"nomn": "семидесятая", "gent": "семидесятой"},
                       "n": {"nomn": "семидесятое", "gent": "семидесятого"}},
                  80: {"m": {"nomn": "восьмидесятый", "gent": "восьмидесятого"},
                       "f": {"nomn": "восьмидесятая", "gent": "восьмидесятой"},
                       "n": {"nomn": "восьмидесятое", "gent": "восьмидесятого"}},
                  90: {"m": {"nomn": "девяностый", "gent": "девяностого"},
                       "f": {"nomn": "девяностая", "gent": "девяностой"},
                       "n": {"nomn": "девяностое", "gent": "девяностого"}},
                  100: {"m": {"nomn": "сотый", "gent": "сотого"},
                        "f": {"nomn": "сотая", "gent": "сотой"},
                        "n": {"nomn": "сотое", "gent": "сотого"}},
                  200: {"m": {"nomn": "двухсотый", "gent": "двухсотого"},
                        "f": {"nomn": "двухсотая", "gent": "двухсотой"},
                        "n": {"nomn": "двухсотое", "gent": "двухсотого"}},
                  300: {"m": {"nomn": "трёхсотый", "gent": "трёхсотого"},
                        "f": {"nomn": "трёхсотая", "gent": "трёхсотой"},
                        "n": {"nomn": "трёхсотое", "gent": "трёхсотого"}},
                  400: {"m": {"nomn": "четырёхсотый", "gent": "четырёхсотого"},
                        "f": {"nomn": "четырёхсотая", "gent": "четырёхсотой"},
                        "n": {"nomn": "четырёхсотое", "gent": "четырёхсотого"}},
                  500: {"m": {"nomn": "пятисотый", "gent": "пятисотого"},
                        "f": {"nomn": "пятисотая", "gent": "пятисотой"},
                        "n": {"nomn": "пятисотое", "gent": "пятисотого"}},
                  600: {"m": {"nomn": "шестисотый", "gent": "шестисотого"},
                        "f": {"nomn": "шестисотая", "gent": "шестисотой"},
                        "n": {"nomn": "шестисотое", "gent": "шестисотого"}},
                  700: {"m": {"nomn": "семисотый", "gent": "семисотого"},
                        "f": {"nomn": "семисотая", "gent": "семисотой"},
                        "n": {"nomn": "семисотое", "gent": "семисотого"}},
                  800: {"m": {"nomn": "восьмисотый", "gent": "восьмисотого"},
                        "f": {"nomn": "восьмисотая", "gent": "восьмисотой"},
                        "n": {"nomn": "восьмисотое", "gent": "восьмисотого"}},
                  900: {"m": {"nomn": "девятисотый", "gent": "девятисотого"},
                        "f": {"nomn": "девятисотая", "gent": "девятисотой"},
                        "n": {"nomn": "девятисотое", "gent": "девятисотого"}},
                  1000: {"m": {"nomn": "тысячный", "gent": "тысячного"},
                         "f": {"nomn": "тысячная", "gent": "тысячной"},
                         "n": {"nomn": "тысячное", "gent": "тысячного"}}
                  }
    end2form = {
        'ый': {'sex': 'm', 'case': 'nomn'},
        'ий': {'sex': 'm', 'case': 'nomn'},
        'й': {'sex': 'm', 'case': 'nomn'},
        'ое': {'sex': 'n', 'case': 'nomn'},
        'ая': {'sex': 'f', 'case': 'nomn'},
        'ого': {'sex': 'm', 'case': 'gent'},
        'го': {'sex': 'm', 'case': 'gent'},
        'ой': {'sex': 'f', 'case': 'gent'}
    }

    def __init__(self, num2text=None):
        self.num2text = num2text or Num2Text()
        self.re_any_ord = re.compile("[+-]?\d+")
        self.re_explicit_ord = re.compile("(\d+)\-?((?:о?го)|(?:ы?й)|(?:и?й)|(?:ой)|(?:ая)|(?:ое))")

    def _gen_sub1000(self, sub1000, data, sex, case):
        if sub1000 in data:
            result = data[sub1000][sex][case]
        else:
            sub100 = sub1000 % 100
            up100 = sub1000 - sub100
            if sub100 in data:
                result = data[sub100][sex][case]
                if up100:
                    result = self.num2text(up100) + " " + result
            else:
                sub10 = sub100 % 10
                up10 = sub100 - sub10
                result = self.num2text(up100 + up10) + " " + data[sub10][sex][case]
        return result

    def _gen_sub1000_orders(self, sub1000, data, sex, case):
        if sub1000 in data:
            result = data[sub1000][sex][case]
        else:
            sub100 = sub1000 % 100
            up100 = sub1000 - sub100
            sub10 = sub100 % 10
            up10 = sub100 - sub10
            if sub100 in data:
                result = data[sub100][sex][case]
                if up100:
                    result = data[up100][sex][case] + result
            else:
                result = ""
                for num in (up100, up10, sub10):
                    if num:
                        result += data[num][sex][case]
        return result.strip()

    def replace_everything_in_text(self, text, sex='m', case='nomn', only_explicit=False):
        def repl(m):
            return " {} ".format(self(int(m.groups()[0]), **self.end2form[m.groups()[1]]))
        text = self.re_explicit_ord.sub(repl=repl, string=" {} ".format(text)).strip().replace("  ", " ").strip()
        if not only_explicit:
            def repl(x):
                return " {} ".format(self(int(x.group()), sex=sex, case=case))
            text = self.re_any_ord.sub(repl=repl, string=" {} ".format(text)).strip().replace("  ", " ").strip()
        return text

    def __call__(self, num: int, sex="m", case="nomn"):
        is_negative = num < 0
        num = abs(num)
        if num in self.structured:
            result = self.structured[num][sex][case]
        else:
            sub1000 = num % 1000
            up1000 = num - sub1000
            if sub1000 == 0:
                order_lvl = (len(str(up1000)) - len(str(up1000).rstrip("0"))) // 3 * 3
                order = 10 ** order_lvl
                up_order = up1000 // order
                raw_for_one_word = up_order % 1000
                result = (self._gen_sub1000_orders(raw_for_one_word, self.before_orders, sex, case) +
                          self.orders[order_lvl][sex][case])
                if result.startswith("одно"):
                    result = result[4:]
                raw_for_num = (up_order - raw_for_one_word) * order
                if raw_for_num:
                    result = self.num2text(raw_for_num) + " " + result
                    if result.startswith(("один ", "одна ", "одно ")):
                        result = result[5:]
            else:
                result = self._gen_sub1000(sub1000, self.structured, sex, case)
                if up1000:
                    result = self.num2text(up1000) + " " + result
                if result.startswith(("один ", "одна ", "одно ")):
                    result = result[5:]
        if is_negative:
            result = "минус " + result
        return result


if __name__ == "__main__":
    num2ord = Num2Ordinal()
    t = "На улице 2 день хорошая погода"
    print("Проверим режим замены вхождений по всему тексту: \"{}\"".format(t))
    print(num2ord.replace_everything_in_text(t))
    print()

    print(num2ord(1, sex="m", case="nomn") + " человек на Луне")
    print(num2ord(87, sex="f", case="nomn") + " ракетка мира")
    print(num2ord(-3, sex="m", case="nomn") + " этаж")
    print(num2ord(8, sex="n", case="gent") + " сентября")
    print(num2ord(934674, sex="n", case="nomn") + " бредовое число")
    print(num2ord(1234000))
    print()
    print("вводите числа:")

    while True:
        t = int(input("> "))
        print(num2ord(t))
