class SangsuLang:
    def __init__(self):
        global sangsu_lang
        sangsu_lang = []

    def caculater(self, caculate):
        caculate = "".join(caculate).split("놔라!")
        if caculate[-1] == "":
            return self.error("놓으라고 놓을 리가 있", "냐")
        result = 1
        for i in range(len(caculate)):
            result *= caculate[i].count("아") - caculate[i].count("악")
        return result


    def compile(self, code, repeat):
        if code[0] != "안녕하세요 정상숩니다":
            return self.error("인사 해", "라")
        codes = []
        for cod in code:
            codes.append(cod.split(" "))
        del codes[0]
        for i in range(len(codes)):
            if codes[i][-1] == "정상숩니다":
                continue
            if codes[i][-1] != "요":
                return self.error("반말 하지 마", "라")
            del codes[i][-1]
        for i in range(len(codes)):
            if codes[i][0] == "테이저건" and codes[i][1] == "맞은" and codes[i][2] == "사람:":
                sangsu_lang.append(["VALUE", self.caculater(codes[i][3:])])

            elif codes[i][0] == "테이저건" and codes[i][1] == "쏜" and codes[i][2] == "사람:":
                myongsasu = 0
                for j in codes[i][3:]:
                    if j == "명사수":
                        myongsasu += 1
                    else:
                        break
                variables = 0
                for variable in sangsu_lang:
                    if variable[0] == "VALUE":
                        variables += 1
                if myongsasu == 0 or myongsasu > variables:
                    return self.error("아무것도 없는데 뭘 바꾸란거", "냐")
                j = 3
                while True:
                    if codes[i][j] == "명사수":
                        del codes[i][j]
                    else:
                        break
                newList = [x for x in sangsu_lang if x[0]=="VALUE"]
                newList[myongsasu-1] = self.caculater(codes[i][3:])
                k = 0
                for j in range(len(sangsu_lang)):
                    if sangsu_lang[j][0] == "VALUE":
                        k += 1
                        if k == myongsasu:
                            sangsu_lang[j] = ["VALUE", self.caculater(codes[i][3:])]

            elif codes[i][0] == "테이저건" and codes[i][1] == "쏜" and codes[i][2] == "명사수:":
                myongsasu = 0
                for j in codes[i][3:]:
                    if j == "명사수":
                        myongsasu += 1
                    else:
                        break
                variables = 0
                for variable in sangsu_lang:
                    if variable[0] == "VALUE":
                        variables += 1
                if myongsasu == 0 or myongsasu > variables:
                        return self.error("아무것도 없는데 뭘 바꾸란거", "냐")
                j = 3
                while True:
                    if codes[i][j] == "명사수":
                        del codes[i][j]
                    else:
                        break
                newList = [x for x in sangsu_lang if x[0]=="VALUE"]
                k = 0
                for j in range(len(sangsu_lang)):
                    if sangsu_lang[j][0] == "VALUE":
                        k += 1
                        if k == myongsasu:
                            sangsu_lang[j] = ["VALUE", newList[myongsasu-1][1] + self.caculater(codes[i][3:])]

            elif codes[i][0] == "CHECK" and codes[i][1] == "THIS" and codes[i][2] == "OUT" and codes[i][3] == "나는":
                newList = [x for x in sangsu_lang if x[0]=="VALUE"]
                if "명사수" in codes[i][4:] and "정상수" in codes[i][4:]:
                    return self.error("정상수가 명사수 총에 맞았", "다")
                elif codes[i][4] == "정" and codes[i][5] == "상" and codes[i][6] == "수":
                    sangsu_lang.append(["PRINT", chr(self.caculater(codes[i][7:]))])
                elif codes[i][4] == "명사수":
                    sangsu_lang.append(["PRINT", "\n"])
                elif codes[i][4:].count("정상수") == 0:
                    sangsu_lang.append(["PRINT", self.caculater(codes[i][4:])])
                elif codes[i][4:].count("정상수") > len(newList):
                        return self.error("그런거 없", "다")
                elif codes[i][4:].count("정상수") <= len(newList) and codes[i][4:].count("정상수") > 0:
                    sangsu = codes[i][4:].count("정상수")
                    hihi = codes[i][4:]
                    j = 0
                    while True:
                        if hihi == []:
                            break
                        elif hihi[j] == "정상수":
                            del hihi[j]
                        else:
                            break
                    aak = "아" in "".join(codes[i][4:]) or "악" in "".join(hihi)
                    if hihi == []:
                        sangsu_lang.append(["PRINT", newList[sangsu-1][1]])
                        continue
                    elif aak == True and "탕" not in "".join(hihi):
                        sangsu_lang.append(["PRINT", newList[sangsu-1][1] + self.caculater(hihi[0])])
                    elif aak == True and "탕" in "".join(hihi):
                        sangsu_lang.append(["PRINT", chr(newList[sangsu-1][1] + self.caculater(hihi[0]))])
                    elif hihi == ["탕"]:
                        sangsu_lang.append(["PRINT", chr(newList[sangsu-1][1])])

            elif codes[i] == ["안녕히", "계세요", "정상수였습니다"]:
                for sang in sangsu_lang:
                    if sang[0] == "VALUE":
                        continue
                    elif sang[0] == "PRINT":
                        if sang[1] == None:
                            print("\n", end='')
                        else:
                            print(sang[1], end='')

            elif codes[i][0] == "카운팅" and codes[i][1] == "스타~":
                hehe = []
                j = i+1
                while True:
                    if codes[j] == ["밤하늘의", "펄~"]:
                        break
                    if codes[j] == ["안녕하세요", "정상숩니다"]:
                        hehe.append(" ".join(codes[j]))
                    else:
                        hehe.append(" ".join(codes[j]) + " 요")
                    j += 1
                times = self.caculater([codes[i][2]])
                for j in range(times-1):
                    self.compile(hehe, True)
                i += len(hehe)

    def compileFile(self, code):
        try:
            with open(code, encoding='utf-8-sig') as mte_file:
                code = mte_file.read().splitlines()
                self.compile(code, False)
        except FileNotFoundError:
            self.error("파일이 없", "다")
        except UnicodeDecodeError:
            self.error("디코딩이 안된", "다")

    def error(self, ErrorName, daranya):
        if daranya == "다":
            print(ErrorName + "다 씨발롬아")
        elif daranya == "라":
            print(ErrorName + "라 씨발롬아")
        elif daranya == "냐":
            print(ErrorName + "냐 씨발롬아")

SangsuLang().compileFile('test.jss')
