class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question   # 문제
        self.choices = choices     # 선택지 4개 (리스트)
        self.answer = answer       # 정답 번호 (1~4)

    def show(self):                          # 문제 보여주기
        print(self.question)
        for i in range(len(self.choices)):
            print(f"  {i + 1}. {self.choices[i]}")

    def ask(self):                           # 문제 내고 답 받기
        self.show()                          # 위에서 만든 show() 사용
        user = input("정답 번호를 입력하세요: ")

        if int(user) == self.answer:         # 입력한 번호 == 정답?
            print("정답입니다! 🎉")
        else:
            print(f"땡! 정답은 {self.answer}번이에요.")

quiz1 = Quiz(
    "세계에서 가장 많이 팔리는 패스트푸드는?",
    ["피자", "햄버거", "핫도그", "타코"],
    2)

quiz1.ask()




