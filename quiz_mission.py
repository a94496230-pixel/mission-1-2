import random  # import는 도구상자를 가져오는 명령어

import json

import os  # 추가내용: 파일 경로 계산(state.json 위치 고정)과 손상 파일 백업(.bak)에 사용

from datetime import datetime # from A import B 는 A에서 B만 가져온다. 앞의 datetime은 모듈(상자), 뒤는 여러 도구중 하나(datetime, date, time, ...)

# 추가내용: state.json을 "실행 위치"가 아니라 "이 파일이 있는 폴더(프로젝트 루트)"에 고정
STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")

def clean(text): # def 정의해. clean 이라는 이름. text라는 매개변수를 받는다.
    return text.encode("utf-8", "ignore").decode("utf-8") # return 보여줘. text를, encode하고 불가능한건 ignore한 다음 decode한 값을.

def input_number(prompt, low, high): # 반복적으로 사용된 while루프를 함수로 만들어 아래 적용. low~high 범위 숫자를 받을 때 까지 반복함.
    
    while True: # 무한 반복
        value = input(prompt).strip()   # 입력값의 .strip() 앞뒤 공백 제거
        if value == "":                 # 빈입력시 
            print("숫자를 입력해주세요!")  # 안내 멘트 출력
            continue                    # continue -> 루프의 처음으로.
        try:                            # 시도해봐
            num = int(value)            # 문자로 입력된 값(3)을 숫자(3)으로 변환. -> 실패 가능함.
            if low <= num <= high:      # 범위 지정
                return num              # 올바른 값이면 값을 돌려주고(표시), 루프 종료. return은 함수를 종료하고 값을 반환함.
            else:                       # 범위 밖의 숫자가 입력될 경우
                print(f"{low}~{high} 중에서 골라주세요!")  # 안내 멘트 표시, 루프기 때문에 다시 처음으로 돌아감.
        except ValueError:              # ValueError, 타입은 맞지만 내용이 부적절할 때 발생하는 에러. int("abc")를 보면 int는 문자열을 받을 수 있어 타입은 맞지만, 해당 문자는 숫자로 변환이 불가능 값이라 나오는 에러.
            print("숫자로 입력해주세요!")

            ### 중요사항. if 뒤에 elif가 아니라 try를 쓴 이유. if elif else는 조건문이지만, try except는 예외처리문이다. try에서 에러가 발생하면 except로 넘어가고, 에러가 없으면 except를 건너뛰고 다음으로 넘어간다. 따라서 if elif else로 하면 ValueError가 발생하면 프로그램이 종료되지만, try except로 하면 ValueError가 발생해도 프로그램이 종료되지 않고 안내 멘트만 출력하고 다시 루프의 처음으로 돌아간다.


# 추가내용: 문제/선택지처럼 "비어 있으면 안 되는" 문자 입력을 받는 함수. input_number와 같은 방식(빈 입력이면 안내 후 다시 입력)
def input_text(prompt):
    while True:
        value = clean(input(prompt).strip())  # 앞뒤 공백 제거 후 clean 적용
        if value == "":                       # 빈 입력(그냥 Enter)이면
            print("빈 입력이에요! 내용을 입력해주세요!")
            continue                          # 다시 입력받기
        return value


class Quiz: # Quiz 클래스, 문제를 하나 찍어내기 위한 틀
    def __init__(self, question, choices, answer, explanation="", hint=""): # __init__ 객체가 생성될 때 자동실행. self는 만들어지는 객체, q,c,a,e,h로 문제가 구성됨.
        self.question = question            # self.question이라는 속성에 question을 넣어줌. 즉, Quiz라는 객체에 question이라는 속성이 생김.
        self.choices = choices              # 이하동문.
        self.answer = answer
        self.explanation = explanation
        self.hint = hint                    # Quiz라는 객체에(문제, 선지, 답, 해설, 힌트)가 존재하게 되며 해설과 힌트는 없을 수 있다. =""

    def show(self):                         # Quiz 클래스 속에서 show를 정의함
        print()                             # 가독성을 위한 공백
        print(f"\033[1m{self.question}\033[0m")          # 문제 출력, \033[1m굵게, \033[0m 원래대로
        print()                             # 공백
        for i in range(len(self.choices)):  # for [꺼낸거] in [꺼낼 대상] 하나씩 꺼내서 반복, i 는 임의로 지정한 값, range 범위값 range없이 숫자만 적으면 4라는 하나의 항목만 나옴, len은 만들어진 Quiz객체(self)의 choice리스트 안의 항목의 개수를 세어줌 
            print(f"{i+1}. {self.choices[i]}")  # 

    # 추가내용: 정답 확인만 담당하는 메서드(출력/입력과 채점 분리). ask()에서 이 메서드를 사용
    def is_correct(self, user):
        return user == self.answer

    def ask(self):
        self.show()
        print()                        # 먼저 문제를 보여줘.

        used_hint = False  # 힌트 사용여부 기록

        if self.hint: # 힌트가 있을 경우에만
            while True:

                choice = input("힌트를 볼까요? (y/n): ").strip().lower()
                if choice == "y":
                    print(f"💡 힌트: {self.hint}")
                    used_hint = True  # 힌트 사용 확인
                    break
                
                elif choice == "n":
                    break
                else:
                    print("y / n 으로 입력해주세요!")
            print()
                    

        user = input_number("정답 번호: ", 1, 4)  # while 루프를 함수로 대체

        if self.is_correct(user):        # 추가내용: 기존 `user == self.answer` 비교를 is_correct 메서드로 교체. int는 정수. 문자를 숫자로 바꿔줌. 1도 문자 1과 숫자 1이 다름.
            print("정답이에요! 🎉")
            print()
            if self.explanation:       # 해설이 있는 문제일 경우
                print(f"💡 해설: {self.explanation}")  # 해설 출력!
            print()    
            return True, used_hint                  # return은 점수를 위해
    
        else:
            print(f"아쉬워요! 정답은 {self.answer}번! 😢")
            print(f"   → {self.choices[self.answer - 1]}")  # 추가내용: 정답 번호뿐 아니라 정답 선택지 내용도 함께 보여줌
            print()
            if self.explanation:
                print(f"💡 해설: {self.explanation}")
            print()    
            return False, used_hint


        

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
                "파일에 저장하면 프로그램을 껐다 켜도 데이터가 유지된다(데이터 영속성).",
                "메모리(RAM)와 파일(디스크)의 차이가 무엇인지 생각해보세요."
                ),
            Quiz(
                "파일이 없거나 손상되었을 때 프로그램이 멈추지 않게 하는 방법으로 가장 적절한 것은?",
                ["try/except로 예외를 잡아 기본 데이터로 복구한다.",
                 "오류가 나면 프로그램을 즉시 강제 종료한다.",
                 "예외 처리 없이 그대로 실행한다.",
                 "파일이 생길 때까지 무한 반복한다."],
                1,
                "try/except로 예외를 잡으면 파일 오류에도 멈추지 않고 복구할 수 있다.",
                "프로그램이 예상치 못한 상황을 만났을 때 쓰는 문법이 무엇이었는지 떠올려보세요."
                ),
        ]
        self.custom_quizzes = []  # 추가문제를 위한 비어있는 리스트
        self.history = []        # 👈 기록을 담을 리스트!
        self.load_data()

    def save_data(self):
        data = {
            "best_score": self.best_score,          # 최고 점수
            "history": self.history,
            "quizzes": [                            # list로 퀴즈의 구성요소들을 묶는다. [대괄호]로 감싼다.
                {                                   # 구성요소들을 dict딕셔너리로! {중괄호}로 감싼다.
                    "question": q.question,         # dict는 키와 값으로 구성된다. 여기서 key는 "question", value는 q.question
                    "choices": q.choices,
                    "answer": q.answer,
                    "explanation": q.explanation,
                    "hint": q.hint
                }
                for q in self.custom_quizzes
            ]             
        }   

        try:  # 추가내용: 쓰기 오류(권한 없음, 디스크 문제 등)가 나도 프로그램이 죽지 않도록 try/except로 감쌈
            with open(STATE_FILE, "w", encoding="utf-8") as f:   # 추가내용: "state.json" → STATE_FILE(프로젝트 루트 고정 경로)
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("저장 완료!")
        except PermissionError:  # 추가내용: 파일 쓰기 권한이 없을 때 (OSError의 하위 클래스라 OSError보다 먼저 써야 함)
            print("⚠️ 파일 쓰기 권한이 없어서 저장하지 못했어요. 이번 변경 내용은 파일에 남지 않을 수 있어요.")
        except OSError as e:     # 추가내용: 그 외 파일 쓰기 오류
            print(f"⚠️ 저장 중 오류가 발생했어요({e}). 이번 변경 내용은 파일에 남지 않을 수 있어요.")

    def load_data(self):  
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:   # 추가내용: "state.json" → STATE_FILE(프로젝트 루트 고정 경로)
                data = json.load(f)                  # 파일 읽기
            # 추가내용: 끝까지 성공했을 때만 반영하려고 임시 변수에 먼저 담음 (일부만 불러온 상태 방지)
            best_score = data.get("best_score", 0)     # 점수는 그대로
            history = data.get("history", [])   # 👈 기록 불러오기(없으면 빈 리스트)
            custom_quizzes = [                         # 👇 여기에서 추가문제 조립!
                Quiz(d["question"], d["choices"], d["answer"], d.get("explanation", ""), d.get("hint", ""))
                for d in data["quizzes"]             # 딕셔너리 하나씩
            ]
            

        except FileNotFoundError: # 파일이 없을 경우
            print("저장된 데이터가 없어요! 새로 시작합니다 😊")
            return  # 추가내용: 실패했으니 기본 데이터 그대로 두고 종료
        except PermissionError:  # 추가내용: 파일 읽기 권한이 없을 경우 (OSError보다 먼저 써야 함)
            print("⚠️ 파일 읽기 권한이 없어요. 기본 데이터로 실행합니다.")
            return
        except OSError as e:     # 추가내용: 그 외 파일 읽기 오류
            print(f"⚠️ 파일을 읽는 중 오류가 발생했어요({e}). 기본 데이터로 실행합니다.")
            return
        except (json.JSONDecodeError, UnicodeDecodeError, KeyError, TypeError, AttributeError): # 파일이 손상 되었을 경우 (추가내용: UnicodeDecodeError, TypeError, AttributeError 추가)
            print("⚠️ 데이터 파일이 손상되어 기본 데이터로 복구합니다.")
            self.backup_corrupted_file()  # 추가내용: 덮어쓰기 전에 손상 파일을 .bak으로 보관
            return

        # 추가내용: 여기까지 왔다면 파일 읽기/조립이 모두 성공 → 그때서야 실제 값에 반영
        self.best_score = best_score
        self.history = history
        self.custom_quizzes = custom_quizzes

    # 추가내용: 손상된 state.json을 다음 저장 때 덮어쓰기 전에 state.json.bak으로 보관 (실패해도 프로그램은 계속 실행)
    def backup_corrupted_file(self):
        try:
            os.replace(STATE_FILE, STATE_FILE + ".bak")
            print("📦 손상된 파일은 state.json.bak으로 보관했어요.")
        except OSError:
            pass

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
        print("  5. 🏆 점수 기록")
        print("  6. 🚪 종료")
        print("=" * 30)

    def show_list(self):
        quizzes = self.all_quizzes()   # 추가내용
        if not quizzes:                # 추가내용: 퀴즈가 하나도 없는 경우 처리 (미션 요구사항)
            print("아직 등록된 퀴즈가 없어요! 먼저 추가해주세요 😊")
            return
        print("===== 📋 퀴즈 목록 =====")
        print(f"총 {len(quizzes)}개")   # 추가내용: 전체 퀴즈 개수 표시
        for quiz in quizzes:           # 추가내용: self.all_quizzes() → 위에서 만든 quizzes 변수 사용
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
            correct, used_hint = quiz.ask()
            if correct:
                if used_hint:
                    score += 0.5
                else:
                    score += 1

        print(f"총 {count}문제 중 {score}점이에요! 🎯")
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total": count,          # 👈 푼 문제 수는?
            "score": score           # 👈 점수는?
            }
        self.history.append(record)    # 리스트에 기록 추가!

        if score > self.best_score:          # 👈 새 점수가 더 높으면?
            self.best_score = score          # 👈 최고 점수 갱신!
            print(f"🏆 신기록! 최고 점수: {self.best_score}점")
        else:
            print(f"현재 최고 점수는 {self.best_score}점이에요! 다음엔 더 잘할 수 있어요! 💪")
        self.save_data() # 기록 항상 저장


    # 추가내용: run() 안에 길게 들어 있던 퀴즈 추가 입력 로직을 메서드로 분리 (기능별 메서드 분리 요구사항)
    def add_quiz(self):
        print()
        print("새로운 문제를 만들어요!")
        print()
        q = input_text("문제입력: ")              # 추가내용: clean(input()) → 빈 입력을 막는 input_text로 교체
        c1 = input_text("선택지 1: ")
        c2 = input_text("선택지 2: ")
        c3 = input_text("선택지 3: ")
        c4 = input_text("선택지 4: ")
        a = input_number("정답 번호(1~4): ", 1, 4)   # 👈 숫자는 그대로 둬요!
        e = clean(input("해설(없으면 Enter): ").strip())    # 추가내용: 해설/힌트는 선택 사항이라 빈 입력 허용, 공백만 제거
        h = clean(input("힌트(없으면 Enter): ").strip())
        new_quiz = Quiz(q, [c1, c2, c3, c4], a, e, h)     # 새 custom_quiz 만들기!
        self.custom_quizzes.append(new_quiz)               # 목록에 추가!
        self.save_data()                          # json 파일에 저장
        print("퀴즈가 추가됐어요! ✨")


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
        
    def show_history(self): # 점수 기록 기능        
        print()
        print("===== 🏆 점수 기록 =====")

        if not self.history:                        # 기록이 하나도 없을 때
            print("아직 게임 기록이 없어요! 😊")
            return

        best = max(self.history, key=lambda h: h["score"])   # score 기준
        print(f"🏆 최고 점수: [{best['date']}] {best['total']}문제 중 {best['score']}점")
        print("-" * 24)
        for h in reversed(self.history):                      # 기록 하나씩 출력, 리버스는 최근기록이 위에 오도록.
            print(f"[{h['date']}] {h['total']}문제 중 {h['score']}점")


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
                    self.add_quiz()                 # 추가내용: 기존 인라인 입력 코드를 add_quiz() 메서드 호출로 교체

                elif choice == "3":
                    self.show_list()                # 목록 보기!

                elif choice == "4":
                    self.delete_quiz()          # 👈 삭제 기능 연결!

                elif choice == "5":
                    self.show_history()  # 점수 기록 출력

                elif choice == "6":
                    print("게임을 종료해요! 👋")
                    break                           # 반복 끝!
                else:
                    print("1~6 중에서 골라주세요! 😊")

            except (KeyboardInterrupt, EOFError):   # Ctrl+C, 입력 종료
                print("\n안전하게 저장 후 종료할게요! 👋")
                self.save_data()                       # 저장 후 종료
                break    




        
# 추가내용: 이 파일을 직접 실행했을 때만 게임이 시작되도록 main 가드 추가 (다른 파일에서 import해도 자동 실행되지 않음)
if __name__ == "__main__":
    game = QuizGame()      # 👈 인스턴스 만들기! (__init__ 실행됨)
    game.run()           # 👈 game.play_quiz() 대신 이걸로!
