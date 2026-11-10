# 📐 퀴즈 1문제 설계도
class Quiz: # Quiz 클래스
    def __init__(self, question, choices, answer): # 정보 담기
        self.question = question
        self.choices = choices
        self.answer = answer

    def show(self):
        print(self.question)          # 문제 출력
        for i in range(len(self.choices)):   # 선택지 4개 반복
            print(f"{i+1}. {self.choices[i]}")

    def ask(self):
        self.show()                        # 먼저 문제를 보여주고
        user = input("정답 번호: ")         # 답 입력받기
        if int(user) == self.answer:        # int는 정수. 문자를 숫자로 바꿔줌. 1도 문자 1과 숫자 1이 다름.
            print("정답이에요! 🎉")
            return True                   # return은 점수를 위해
        else:
            print(f"아쉬워요! 정답은 {self.answer}번! 😢")
            return False

# 📚 문제들 만들기
quizzes = [
    Quiz("김치의 원조 나라는?", ["대한민국", "중국", "대만", "일본"], 1),
    Quiz("피자의 원조 나라는?", ["미국", "이탈리아", "프랑스", "일본"], 2),
    Quiz("초밥은 어느 나라 음식일까요?", ["한국", "중국", "일본", "태국"], 3),
]
best_score = 0         # ← 이거 추가! 🏆

while True:
    print("===== 🍔 음식 퀴즈 게임 =====")
    print("1. 퀴즈 풀기")
    print("2. 퀴즈 추가")
    print("3. 퀴즈 목록")
    print("4. 최고 점수")
    print("5. 종료")

    choice = input("번호를 선택하세요: ")

    if choice == "1":
        score = 0                      # 점수 0에서 시작!
        for quiz in quizzes:           # 문제 하나씩 꺼내서
            if quiz.ask():             # 물어보고, 맞으면(True)
                score = score + 1      # 점수 +1!
        print(f"총 {score}점이에요! 🎯")  # 결과 발표!
        if score > best_score:         # 이번 점수가 최고 점수보다 높으면?
            best_score = score         # 최고 점수 갱신! 📈
            print("🎉 새로운 최고 점수 달성!")
        
    elif choice == "2":
        print("===== ✏️ 퀴즈 추가 =====")
        question = input("질문을 입력하세요: ")
        print("입력한 질문:", question)   # 확인용!
        choice1 = input("선택지 1번: ")
        choice2 = input("선택지 2번: ")
        choice3 = input("선택지 3번: ")
        choice4 = input("선택지 4번: ")
        choices = [choice1, choice2, choice3, choice4] # input 받은 choice1,2,3,4를 []대괄호를 사용해 리스트로 묶음
        answer = int(input("정답 번호 (1~4): ")) # 마찬가지로 int를 사용해 문자를 숫자로 변환해줌.
        new_quiz = Quiz(question, choices, answer)
        quizzes.append(new_quiz)
        print("퀴즈가 추가되었습니다! ✅")

    elif choice == "3":
        print("===== 📋 퀴즈 목록 =====")
        for quiz in quizzes:           # 문제 하나씩 꺼내서
            quiz.show()                # 보여주기!
            print()                    # 한 줄 띄우기 (보기 좋게!)

    elif choice == "4":
        print("===== 🏆 최고 점수 =====")
        if best_score == 0:           # 아직 0점이면 = 안 풀었으면
            print("아직 퀴즈를 풀지 않았어요! 😢")
        else:
            print(f"최고 점수는 {best_score}점이에요! 🏆")

    elif choice == "5":
        print("게임을 종료합니다! 👋")
        break

    else:
        print("⚠️ 1~5 사이의 번호를 입력해주세요!")



