import random
import json

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
        self.show()                        # 먼저 문제를 보여줘.
        while True:
            try: # 보기를 제외한 답을 입력했을 경우 발생하는 오류 방지, 일단 시도!
                user = int(input("정답 번호: ")) # 입력한 값을 숫자로 변환
                if 1 <= user <= 4:              # 1~4 인지 확인
                    break
                else: print("1~4 중에서 골라주세요!") # 숫자인데 1~4가 아니다?
            except:
                print("보기에 해당하는 숫자로 입력해주세요!") # 숫자 외의 답을 입력했다?

        if user == self.answer:        # int는 정수. 문자를 숫자로 바꿔줌. 1도 문자 1과 숫자 1이 다름.
            print("정답이에요! 🎉")
            return True                   # return은 점수를 위해
        else:
            print(f"아쉬워요! 정답은 {self.answer}번! 😢")
            return False
        

# QuizGame 클래스 추가 

class QuizGame:
    def __init__(self):                    # 👈 추가!
        self.best_score = 0                # 최고 점수
        self.quizzes = [                   # 퀴즈 목록 (self로!)
            Quiz("김치의 원조 나라는?", ["대한민국", "중국", "대만", "일본"], 1),
            Quiz("피자의 원조 나라는?", ["미국", "이탈리아", "프랑스", "일본"], 2),
            Quiz("초밥은 어느 나라 음식일까요?", ["한국", "중국", "일본", "태국"], 3),
        ]
        self.custom_quizzes = []  # 추가문제를 위한 비어있는 리스트
        self.load_data() 

    def save_data(self):
        data = {
            "best_score": self.best_score,          # 최고 점수
            "quizzes": [                            # 퀴즈들을 딕셔너리로!
                {
                    "question": q.question,
                    "choices": q.choices,
                    "answer": q.answer
                }
                for q in self.custom_quizzes               # 퀴즈 하나씩 변환
            ]
        }
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("저장 완료!")

    def load_data(self):
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)                  # 파일 읽기
            self.best_score = data["best_score"]     # 점수는 그대로
            self.custom_quizzes = [                         # 👇 여기에서 추가문제 조립!
                Quiz(d["question"], d["choices"], d["answer"])
                for d in data["quizzes"]             # 딕셔너리 하나씩
            ]
        except:
            print("저장된 데이터가 없어요! 새로 시작합니다 😊")

    def all_quizzes(self):
        """기본 + 추가 문제를 합쳐서 돌려줌"""
        return self.quizzes + self.custom_quizzes

    def show_menu(self):              # 👈 self 꼭 넣기!
        print("===== 🍔 음식 퀴즈 게임 =====")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수")
        print("5. 종료")

    def show_list(self):
        print("===== 📋 퀴즈 목록 =====")
        for quiz in self.all_quizzes():          
            quiz.show()             
            print()     

    def play_quiz(self):
        score = 0
        quizzes = self.all_quizzes()
        random.shuffle(quizzes)
        for quiz in quizzes:
            if quiz.ask():
                score = score + 1
        print(f"총 {score}점이에요! 🎯")

        if score > self.best_score:          # 👈 새 점수가 더 높으면?
            self.best_score = score          # 👈 최고 점수 갱신!
            self.save_data()
            print(f"🏆 신기록! 최고 점수: {self.best_score}점")
        else:
            print(f"현재 최고 점수는 {self.best_score}점이에요! 다음엔 더 잘할 수 있어요! 💪")
        

    def run(self):
        while True:
            self.show_menu()                    # 메뉴 보여주기
            choice = input("번호 선택: ")        # 입력받기

            if choice == "1":
                self.play_quiz()                # 퀴즈 풀기!

            elif choice == "2":
                q = input("문제: ")                        # 문제 입력
                c1 = input("선택지 1: ")
                c2 = input("선택지 2: ")
                c3 = input("선택지 3: ")
                c4 = input("선택지 4: ")
                a = int(input("정답 번호(1~4): "))          # 정답 (숫자로!)
                new_quiz = Quiz(q, [c1, c2, c3, c4], a)     # 새 custom_quiz 만들기!
                self.custom_quizzes.append(new_quiz)               # 목록에 추가!
                self.save_data()                          # json 파일에 저장
                print("퀴즈가 추가됐어요! ✨")

            elif choice == "3":
                self.show_list()                # 목록 보기!

            elif choice == "4":
                print(f"🏆 최고 점수는 {self.best_score}점이에요!")

            elif choice == "5":
                print("게임을 종료해요! 👋")
                break                           # 반복 끝!
            else:
                print("아직 준비 중이에요! 😊")




        
game = QuizGame()      # 👈 인스턴스 만들기! (__init__ 실행됨)
game.run()           # 👈 game.play_quiz() 대신 이걸로!



