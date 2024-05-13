from typing import Generator
import api
import datetime

class AiBot:
    def __init__(self, name: str, role_profile: str):
        self.name = name
        self.role_profile = role_profile

        personality = ""
        for n in api.generate_role_appearance(name, role_profile):
            print(str(n), end='')
            personality += n
        print()

        self.message = []
        self.character_meta = {
            "user_name": "",
            "bot_name": name, 
            "user_info": "",
            "bot_info": personality, 
        }
        self.personality = personality

    def talk_to(self, bot) -> None:
        self.character_meta['user_info'] = bot.character_meta['bot_info']
        self.character_meta['user_name'] = bot.character_meta['bot_name']

    def talk(self) -> Generator[str, None, None]:
        for chunk in api.get_characterglm_response(self.message, self.character_meta):
            yield chunk

    def listen(self, message: str) -> str:
        self.message.append({"role": "assistant", "content": message})

    def save(self) -> None: 
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"{self.name}_{current_time}.txt"
        
        with(open(filename, 'w')) as f:
            f.write(self.personality) 
            for msg in self.message:
                f.write(f"\n{msg['role']}：{msg['content']}")
                # f.write(msg['content'])