# standart libraries
import os, time, keyboard, requests, subprocess, random

# lownloaded libraries
from telebot import TeleBot, types
import speech_recognition as sr
from threading import Thread

# myCreated libraries
import file

'''
 ____________________________________________________________
|  ___      ____    _________________   ___________________  |
| |   |    /   /   /   /         \   \ |_______     _______| |
| |   |   /   /   /   /           \   \        |   |         |
| |   |  /   /   /   /             \   \       |   |         |
| |   | /   /   /   /               \   \      |   |         |
| |   |/   /   /   /                 \   \     |   |         |
| |   |   |   |   | Kотик ☾амуйловˆᵜˆ |   |    |   |         |
| |   |\   \   \   \                 /   /     |   |         |
| |   | \   \   \   \               /   /      |   |         |
| |   |  \   \   \   \             /   /       |   |         |
| |   |   \   \   \   \           /   /        |   |         |
| |___|    \___\   \___\_________/___/         |___|         |
|____________________________________________________________|
                                            Kотик ☾амуйловˆᵜˆ

сделать автообновление версии для конфигурационного файла base.json так же для xml файла
сделать файл, запускающий последнюю версию файла
ответ на голосовые команды
'''
# print(os.getenv('managebot'))

class TGBot:
    def __init__(self):
        self.path = os.path.dirname(__file__)
        self.jP = os.path.join
        self.nameBase = self.jP(self.path, 'bace.json')
        self.base = file.readJson(self.nameBase)
        self.bot = TeleBot(os.getenv('managebot'))
        self.isDefend = False
        self.cmd = False

    def editBase(self, key="", data=""):
        self.base[key] = data
        # file.debounce(file.writeJson, self.base, self.nameBase)
        file.writeJson(self.base, filename=self.nameBase)

    def btn(self, t, cd):
        return types.InlineKeyboardButton(text=t, callback_data=cd)

    def pr(self, key, timeOut=1):
        keyboard.press(key)
        time.sleep(timeOut)
        keyboard.release(key)

    def stop(self):
        keyboard.release("w")
        keyboard.release("s")
        keyboard.release("a")
        keyboard.release("d")

    def nevAnswer(self, m, btns, txt):
        self.bot.edit_message_text(text=txt, chat_id=m.chat.id, message_id=m.message_id, reply_markup=btns)

    def audio_to_text(self, dest_name: str):

        r = sr.Recognizer()
        message = sr.AudioFile(dest_name)

        with message as source:
            audio = r.record(source)
        result = r.recognize_google(audio_data=audio, language="ru_RU")

        return result

    def crossheir(self):
        import psutil

        time.sleep(10)
        loop = 5 * 60
        start = False

        while True:
            time.sleep(loop)
            why = True
            for i in psutil.process_iter():
                if "cs2.exe" == i.name():
                    if start:
                        why = False
                    start = True
                    os.system('taskkill /im "cs2.exe" /f')
                    g = random.randint(100, 1000)
                    os.system(r'''Shutdown /s /t 35 /c "Непредвиденная ошибка! Код ошибки: 0x0''' + str(g) + r'"')
                    time.sleep(30)
                    os.system(r'Shutdown /a')

            if start & why:
                break

    def run(self):
        for i in self.base["admins"].keys():
            try:
                if self.base["admins"][i]["notif"]:
                    self.bot.send_message(i, "я работаю")
            except Exception as e:
                if "Error code: 400" in str(e):
                    del self.base["admins"][i]
                    self.editBase()
                print(e)

        @self.bot.message_handler(commands=["start", "help", "id", "cr"])
        def start(message):
            match message.text:
                case "/start":
                    self.isDefend = True
                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("windows", "windows"), self.btn("computer", "comp"))
                    btns.row(self.btn("cs", "cs"), self.btn("opera", "opera"))
                    btns.row(self.btn("help", "help"), self.btn("input mode", "input"))
                    self.bot.send_message(message.chat.id, "select app", reply_markup=btns)
                case "/help":
                    self.bot.send_message(message.chat.id, self.base["help"])
                case "/id":
                    self.bot.send_message(message.chat.id, message.chat.id)
                case "/cr":
                    if not str(message.chat.id) in self.base["admins"].keys():
                        return
                    Thread(target=self.crossheir, args=(self,)).start()

        @self.bot.message_handler(content_types=['voice'])
        def get_audio_messages(message):
            try:
                path = self.bot.get_file(message.voice.file_id).file_path
                fname = os.path.basename(path)
                doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(self.base["bot"], path))

                with open(self.jP(self.path, fname), 'wb') as f:
                    f.write(doc.content)

                subprocess.run([self.jP(self.path, 'ffmpeg.exe'), '-i', self.jP(self.path, fname), self.jP(self.path, fname + '.wav')])

                result = self.audio_to_text(self.jP(self.path, fname + '.wav'))
                self.bot.send_message(message.from_user.id, result)

            except sr.UnknownValueError as e:
                self.bot.send_message(message.from_user.id, "Прошу прощения, но я не разобрал сообщение, или оно поустое...\n" + e)

            except Exception as e:
                self.bot.send_message(message.from_user.id, "Что-то пошло не так\n" + e)

            finally:
                os.remove(self.jP(self.path, fname + '.wav'))
                os.remove(self.jP(self.path, fname))

        @self.bot.callback_query_handler(func=lambda m: True)
        def echoOfComands(m):
            match m.data:
                case "help": self.bot.send_message(m.message.chat.id, self.base["help"])
                case "input": self.bot.send_message(m.message.chat.id, 'send me one symbol ("/", "#", "*") for use key press or click... /help')
                case "menu":
                    # global isDefend
                    # isDefend = False
                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("windows", "windows"), self.btn("computer", "comp"))
                    btns.row(self.btn("cs", "cs"), self.btn("opera", "opera"))
                    btns.row(self.btn("help", "help"), self.btn("input mode", "input"))
                    btns.row(self.btn("new panel", "panel"))
                    self.nevAnswer(m.message, btns, "select app")

                case "panel":
                    # global isDefend
                    # isDefend = False
                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("windows", "windows"), self.btn("computer", "comp"))
                    btns.row(self.btn("cs", "cs"), self.btn("opera", "opera"))
                    btns.row(self.btn("help", "help"), self.btn("input mode", "input"))
                    self.bot.send_message(m.message.chat.id, "select app", reply_markup=btns)
                    self.bot.delete_message(m.message.chat.id, m.message.message_id)

                case "windows":
                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("ctrl", "*ctrl"), self.btn("alt", "*alt"), self.btn("delite", "del"))
                    btns.row(self.btn("esc", "esc"), self.btn("tab", "tab"), self.btn("switch", "alt + tab"))
                    btns.row(self.btn("enter", "enter"), self.btn("space", "space"), self.btn("processes", "/process"))

                    btns.row(self.btn("menu", "menu"))
                    self.nevAnswer(m.message, btns, "windows")

                case "cs":
                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("pause", "esc"), self.btn("dump", "g"), self.btn("reload", "r"))
                    btns.row(self.btn("change", "q"), self.btn("↑", "*w"), self.btn("interaction", "e"))
                    btns.row(self.btn("←", "*a"), self.btn("↓", "*s"), self.btn("→", "*d"))
                    btns.row(self.btn("sit down", "*ctrl"), self.btn("stop", "/stop"), self.btn("jump", "space"))
                    btns.row(self.btn("Global chat", "y"), self.btn("Team chat", "u"), self.btn("enter", "enter"))
                    btns.row(self.btn("use mik", "c"), self.btn("check", "f"), self.btn("roll up", "сtrl + d"))
                    btns.row(self.btn("menu", "menu"))
                    self.nevAnswer(m.message, btns, "сs")

                case "opera":
                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("reload page", "F5"), self.btn("↑", "up"), self.btn("full screen", "f"))
                    btns.row(self.btn("←", "left"), self.btn("pause", "space"), self.btn("→", "right"))
                    btns.row(self.btn("clear", "backspace"), self.btn("↓", "down"), self.btn("enter", "enter"))
                    btns.row(self.btn("close page", "ctrl + w"), self.btn("open last page", "ctrl + t"))
                    btns.row(self.btn("menu", "menu"))
                    self.nevAnswer(m.message, btns, "Mannage")

                case "cmd":
                    self.cmd = True
                    self.isDefend = False

                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("windows", "windows"), self.btn("computer", "comp"))
                    btns.row(self.btn("cs", "cs"), self.btn("opera", "opera"))
                    btns.row(self.btn("help", "help"), self.btn("input mode", "input"))
                    btns.row(self.btn("new panel", "panel"))
                    self.nevAnswer(m.message, btns, "select app")

                case "notify":
                    if not str(m.from_user.id) in self.base["admins"].keys():
                        return
                    self.base["admins"][str(m.from_user.id)]["notif"] = not self.base["admins"][str(m.from_user.id)]["notif"]
                    self.editBase()

                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("off", "comp/off"), self.btn("sleep", "comp/sleep"), self.btn("not off", "comp/on"))
                    btns.row(self.btn("reload", "comp/rel"), self.btn("exit all app", "comp/offApp"), )
                    btns.row(self.btn("lock", "comp/lock"), self.btn("unlock", "comp/unlock"))
                    btns.row(self.btn("notify off" if self.base["admins"][str(m.from_user.id)]["notif"] else "notify on", "notify"))
                    btns.row(self.btn("menu", "menu"))
                    self.nevAnswer(m.message, btns, "computer")
                case "comp":
                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("off", "comp/off"), self.btn("sleep", "comp/sleep"), self.btn("not off", "comp/on"))
                    btns.row(self.btn("reload", "comp/rel"), self.btn("exit all app", "comp/offApp"), )
                    btns.row(self.btn("lock", "comp/lock"), self.btn("unlock", "comp/unlock"))
                    btns.row(self.btn("notify off" if self.base["admins"][str(m.from_user.id)]["notif"] else "notify on", "notify"))
                    btns.row(self.btn("menu", "menu"))
                    self.nevAnswer(m.message, btns, "computer")
                case _:
                    print(m.data)
                    if not str(m.from_user.id) in self.base["admins"].keys():
                        return
                    if m.data[0:5] == "comp/":
                        os.system(self.base["commandOs"][m.data[5:]])
                    elif m.data == "/stop":
                        self.stop()
                    elif m.data == "/process":
                        import psutil
                        text = "\n".join(list(set([i.info["name"].replace(".exe", "") for i in list(psutil.process_iter(['name']))[-15:]])))

                        self.bot.send_message(m.from_user.id, text)

                    elif m.data[0] == "*":
                        Thread(target=self.pr, args=(m.data[1:],)).start()
                    else:
                        keyboard.send(m.data)

        @self.bot.message_handler(func=lambda m: True)
        def keys(message):
            if self.cmd:
                try:
                    os.system(message.text)
                    self.bot.send_message(message.chat.id, "исполнено")

                except Exception as e:
                    btns = types.InlineKeyboardMarkup()
                    btns.row(self.btn("windows", "windows"), self.btn("computer", "comp"))
                    btns.row(self.btn("cs", "cs"), self.btn("opera", "opera"))
                    btns.row(self.btn("help", "help"), self.btn("input mode", "input"))
                    self.bot.send_message(message.chat.id, "ошибка\n" + e, reply_markup=btns)
                finally:
                    self.cmd = False
            elif False:
                pass
            elif message.text in ["/", "#", "*"]:
                btns = types.ReplyKeyboardMarkup()
                btns.row(types.KeyboardButton(f'{message.text}esc'), types.KeyboardButton(f'{message.text}tab'))
                btns.row(types.KeyboardButton(f'{message.text}ctrl'), types.KeyboardButton(f'{message.text}alt'))
                btns.row(types.KeyboardButton(f'{message.text}backspace'), types.KeyboardButton(f'{message.text}shift'))
                btns.row(types.KeyboardButton('/start'), types.KeyboardButton('/help'))
                self.bot.send_message(message.chat.id, "use text for mannage computer", reply_markup=btns)

            else:
                if not str(message.from_user.id) in self.base["admins"].keys():
                    return
                text = message.text
                if text[0] == "#":
                    keyboard.release(text[1:])
                elif text[0] == "*":
                    keyboard.press(text[1:])
                elif text[0] == "/":
                    keyboard.send(text[1:])
                else:
                    if len(text) == 1:
                        keyboard.send(text)
                    else:
                        keyboard.write(text)

        self.bot.polling(none_stop=True)


def main():
    bot = TGBot()
    while True:
        try:
            bot.run()
        except Exception as e:
            print(e)
            time.sleep(10)



if __name__ == "__main__":
    Thread(target=main).start()
