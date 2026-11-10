print("수수께끼 게임에 오신 걸 환영합니다!")
quizzes = [{"question":"아침에는 네 발, 점심에는 두 발, 저녁에는 세 발인 것은?",
     "answers": ["사람", "인간"]},
    {"question": "구멍이 많을수록 물을 더 잘 담는 것은? ",
     "answers": ["스펀지", "스폰지"]},
    {"question": "불을 먹고 사는 것은? ",      
     "answers": ["촛불", "초"]} ]
for quiz in quizzes:
    answer = input(quiz["question"])
    if answer in quiz["answers"]:
        print("정답입니다! 🎉")
    else:
        print("틀렸어요.")