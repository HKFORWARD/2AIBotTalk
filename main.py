import ai_bot

REFERENCE: str = "任小粟初识周迎雪.md"
# REFERENCE: str = "第一序列.md"
PLAYER1: str = "周迎雪"
PLAYER2: str = "任小粟"
START_WORD: str = "（仔细打量着任小粟，慢慢的坐到他对面）任小粟，你是超凡者吧？"
MAX_ROUND: int = 20

def main():
    text = ""
    with open(REFERENCE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            _line = line.strip()
            if _line == "":
                continue
            text += _line

    print("")
    print("===================================================")
    print("这篇文章总行数为： " + str(len(text)))
    print("")

    bot1 = ai_bot.AiBot(PLAYER1, text)
    bot2 = ai_bot.AiBot(PLAYER2, text)

    bot1.talk_to(bot2)
    bot2.talk_to(bot1)

    start_word = START_WORD

    bot1.message.append({"role": "assistant", "content": start_word})
    print(f"{bot1.name}：{start_word}")
    bot2.listen(start_word)

    # 交替对话
    round = 0
    while round < MAX_ROUND:
        # print(f"\n第{round}轮对话")

        # 
        speaker = bot2 if round % 2 == 0 else bot1 
        listener = bot1 if round % 2 == 0 else bot2

        contents = ""
        print(f"{speaker.name}：", end='')

        for chunk in speaker.talk():
            print(chunk, end='')
            contents += chunk

        listener.listen(contents)
        speaker.message.append({"role": "assistant", "content": contents})

        round += 1
        
        print()
        # print(f"\n")

    bot1.save()
    bot2.save()

if __name__ == '__main__':
    main()