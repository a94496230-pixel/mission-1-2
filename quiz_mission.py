import random

import json

def clean(text): # 저장할 수 없는 깨진 글자(서로게이트)를 제거
    return text.encode("utf-8", "ignore").decode("utf-8")

def input_number(prompt, low, high): # 반복적으로 사용된 while루프를 함수로 만들어 아래 적용. low~high 범위 숫자를 받을 때 까지 반복함.
    
    while True:
        value = input(prompt).strip()   # 앞뒤 공백 제거
        if value == "":                 # 빈 입력
            print("숫자를 입력해주세요!")
            continue
        try:
            num = int(value)
            if low <= num <= high:
                return num              # 올바른 값이면 돌려줌
            else:
                print(f"{low}~{high} 중에서 골라주세요!")
        except ValueError:
            print("숫자로 입력해주세요!")


# 📐 퀴즈 1문제 설계도
class Quiz: # Quiz 클래스
    def __init__(self, question, choices, answer, explanation=""): # 정보 담기
        self.question = question
        self.choices = choices
        self.answer = answer
        self.explanation = explanation

    def show(self):
        print()
        print(f"\033[1m{self.question}\033[0m")          # 문제 출력, \033[1m굵게, \033[0m 원래대로
        print()
        for i in range(len(self.choices)):   # 선택지 4개 반복
            print(f"{i+1}. {self.choices[i]}")

    def ask(self):
        self.show()
        print()                        # 먼저 문제를 보여줘.
        user = input_number("정답 번호: ", 1, 4)  # while 루프를 함수로 대체

        if user == self.answer:        # int는 정수. 문자를 숫자로 바꿔줌. 1도 문자 1과 숫자 1이 다름.
            print("정답이에요! 🎉")
            print()
            if self.explanation:       # 해설이 있는 문제일 경우
                print(f"💡 해설: {self.explanation}")  # 해설 출력!
            print()    
            return True                   # return은 점수를 위해
    
        else:
            print(f"아쉬워요! 정답은 {self.answer}번! 😢")
            print()
            if self.explanation:
                print(f"💡 해설: {self.explanation}")
            print()    
            return False


        

# QuizGame 클래스 추가 

class QuizGame:
    def __init__(self):                    # 👈 추가!
        self.best_score = 0                # 최고 점수
        self.quizzes = [                   # 퀴즈 목록 (self로!)
            Quiz(
                "int, str, bool, list, dict 자료형에 대한 설명으로 옳지 않은 것은?",
                ["int는 정수를 다루는 자료형이다.",
                 "bool은 True 또는 False 값을 가진다.",
                 "list는 여러 값을 순서대로 담는 자료형이다.",
                 "dict는 값을 순서(인덱스 번호)로만 꺼낼 수 있다."],
                4,
                "dict는 인덱스가 아니라 '키(key)'로 값을 꺼낸다. (순서로 꺼내는 건 list)"
                ),
            Quiz(
                "클래스의 __init__ 메서드에 대한 설명으로 옳은 것은?",
                ["프로그램이 종료될 때 자동으로 호출된다.",
                 "객체가 생성될 때 자동으로 호출되어 속성을 초기화한다.",
                 "클래스당 한 번만 호출되며 모든 객체가 값을 공유한다.",
                 "반드시 return 값을 지정해야 한다."],
                2,
                "__init__은 객체 생성 시 자동 호출되어 속성을 초기화하는 생성자다."
                ),
            Quiz(
                "인스턴스 메서드의 첫 번째 매개변수 self의 역할로 옳은 것은?",
                ["클래스 외부에서만 쓰이는 특별한 예약어다.",
                 "객체 자신을 가리켜 각 객체가 독립된 속성값을 갖게 한다.",
                 "생략해도 항상 정상 동작한다.",
                 "모든 객체가 같은 속성값을 공유하게 만든다."],
                2,
                "self는 객체 자신을 가리켜 각 객체가 독립된 속성값을 갖게 한다."
                ),
            Quiz(
                "state.json 같은 파일에 데이터를 저장했다가 다시 불러오는 이유로 가장 적절한 것은?",
                ["프로그램 실행 속도를 높이기 위해서",
                 "프로그램을 껐다 켜도 데이터가 유지되도록(데이터 영속성) 하기 위해서",
                 "코드 줄 수를 줄이기 위해서",
                 "메모리 사용량을 0으로 만들기 위해서"],
                2,
                "파일에 저장하면 프로그램을 껐다 켜도 데이터가 유지된다(데이터 영속성)."
                ),
            Quiz(
                "파일이 없거나 손상되었을 때 프로그램이 멈추지 않게 하는 방법으로 가장 적절한 것은?",
                ["try/except로 예외를 잡아 기본 데이터로 복구한다.",
                 "오류가 나면 프로그램을 즉시 강제 종료한다.",
                 "예외 처리 없이 그대로 실행한다.",
                 "파일이 생길 때까지 무한 반복한다."],
                1,
                "try/except로 예외를 잡으면 파일 오류에도 멈추지 않고 복구할 수 있다."
                ),
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
                    "answer": q.answer,
                    "explanation": q.explanation
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
                Quiz(d["question"], d["choices"], d["answer"], d["explanation"])
                for d in data["quizzes"]             # 딕셔너리 하나씩
            ]
        except FileNotFoundError: # 파일이 없을 경우
            print("저장된 데이터가 없어요! 새로 시작합니다 😊")
        except (json.JSONDecodeError, KeyError): # 파일이 손상 되었을 경우
            print("⚠️ 데이터 파일이 손상되어 기본 데이터로 복구합니다.")

    def all_quizzes(self):
        """기본 + 추가 문제를 합쳐서 돌려줌"""
        return self.quizzes + self.custom_quizzes

    def show_menu(self):              # 👈 self 꼭 넣기!
        print()                                    # 위쪽 여백
        print("=" * 30)                            # 구분선 (= 30개)
        print("      📝 미션2 퀴즈 게임")           # 제목 (앞에 공백으로 가운데 느낌)
        print("=" * 30)
        print("  1. 📚 퀴즈 풀기")
        print("  2. ➕ 퀴즈 추가")
        print("  3. 📋 퀴즈 목록")
        print("  4. 🗑️  퀴즈 삭제")   # 새로 추가
        print("  5. 🏆 최고 점수")
        print("  6. 🚪 종료")
        print("=" * 30)

    def show_list(self):
        print("===== 📋 퀴즈 목록 =====")
        for quiz in self.all_quizzes():          
            quiz.show()             
            print()     

    def play_quiz(self):
        score = 0
        quizzes = self.all_quizzes()
        if not quizzes:                      # 퀴즈가 하나도 없을경우.(미션내용. 코드에 기본문제가 포함되어있어 발생하지 않음)
            print("아직 퀴즈가 없어요! 먼저 추가해주세요 😊")
            return
        random.shuffle(quizzes)
        count = input_number(f"문제 수(최대 {len(quizzes)}): ", 1, len(quizzes))
        for quiz in quizzes[:count]:
            if quiz.ask():
                score = score + 1
        print(f"총 {count}문제 중 {score}점이에요! 🎯")

        if score > self.best_score:          # 👈 새 점수가 더 높으면?
            self.best_score = score          # 👈 최고 점수 갱신!
            self.save_data()
            print(f"🏆 신기록! 최고 점수: {self.best_score}점")
        else:
            print(f"현재 최고 점수는 {self.best_score}점이에요! 다음엔 더 잘할 수 있어요! 💪")

    def delete_quiz(self):  # 퀴즈 삭제 기능
        if not self.custom_quizzes:                          # 👈 추가퀴즈 없을 때 처리
            print("삭제할 수 있는 추가 퀴즈가 없어요!")
            return
        print("===== 추가 퀴즈 현황 =====")
        for i in range(len(self.custom_quizzes)):
            print(f"{i+1}. {self.custom_quizzes[i].question}")

        num = input_number("삭제할 번호: ", 1, len(self.custom_quizzes))
        del self.custom_quizzes[num-1]
        self.save_data()
        print("삭제했어요! 🗑️")    
        

    def run(self):
        while True:
            try:
                self.show_menu()                        # 메뉴 보여주기
                choice = input("번호 선택: ").strip()    # 입력받기.앞뒤의 공백제거

                if choice == "": # 공백 입력시
                    print("번호를 입력해주세요! 😊") 
                    continue  # 다시 메뉴로 돌아가기

                if choice == "1":
                    self.play_quiz()                # 퀴즈 풀기!

                elif choice == "2":
                    q = clean(input("문제: "))
                    c1 = clean(input("선택지 1: "))
                    c2 = clean(input("선택지 2: "))
                    c3 = clean(input("선택지 3: "))
                    c4 = clean(input("선택지 4: "))
                    a = input_number("정답 번호(1~4): ", 1, 4)   # 👈 숫자는 그대로 둬요!
                    e = clean(input("해설: "))          
                    new_quiz = Quiz(q, [c1, c2, c3, c4], a, e)     # 새 custom_quiz 만들기!
                    self.custom_quizzes.append(new_quiz)               # 목록에 추가!
                    self.save_data()                          # json 파일에 저장
                    print("퀴즈가 추가됐어요! ✨")

                elif choice == "3":
                    self.show_list()                # 목록 보기!

                elif choice == "4":
                    self.delete_quiz()          # 👈 삭제 기능 연결!

                elif choice == "5":
                    print(f"🏆 최고 점수는 {self.best_score}점이에요!")

                elif choice == "6":
                    print("게임을 종료해요! 👋")
                    break                           # 반복 끝!
                else:
                    print("1~6 중에서 골라주세요! 😊")

            except (KeyboardInterrupt, EOFError):   # Ctrl+C, 입력 종료
                print("\n안전하게 저장 후 종료할게요! 👋")
                self.save_data()                       # 저장 후 종료
                break    




        
game = QuizGame()      # 👈 인스턴스 만들기! (__init__ 실행됨)
game.run()           # 👈 game.play_quiz() 대신 이걸로!



