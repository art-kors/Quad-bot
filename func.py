# Import the gTTS module for text
# to speech conversion
from gtts import gTTS
from playsound import playsound

russian_morze = {'а': '.-',
                 '': '',
                 'б': '-...',
                 'в': '.--',
                 'г': '--.',
                 'д': '-..',
                 'е': '.',
                 'ж': '...-',
                 'з': '--..',
                 'и': '..',
                 'й': '.---',
                 'к': '-.-',
                 'л': '.-..',
                 'м': '--',
                 'н': '-.',
                 'о': '---',
                 'п': '.--.',
                 'р': '.-.',
                 'с': '...',
                 'т': '-',
                 'у': '..-',
                 'ф': '..-.',
                 'х': '....',
                 'ц': '-.-.',
                 'ч': '---.',
                 'ш': '----',
                 'щ': '--.-',
                 'ы': '-.--',
                 'э': '..-..',
                 'ю': '..--',
                 'я': '.-.-',
                 '1': '.----',
                 '2': '..---',
                 '3': '...--',
                 '4': '....-',
                 '5': '.....',
                 '6': '-....',
                 '7': '--...',
                 '8': '---..',
                 '9': '----.',
                 '0': '-----',
                 ',': '.-.-.-',
                 '.': '......',
                 '?': '..--..',
                 '/': '-..-.',
                 '-': '-....-',
                 '(': '-.--.',
                 ')': '-.--.-',
                 '!': '--..--',
                 '\n': '\n',
                 'ъ': '.--.-.',
                 'ь': '-..-',
                 '': '',
                 '"': '.-..-.'
                 }
russian_demorze = {'-': 'т',
                   '--': 'м',
                   '---': 'о',
                   '----': 'ш',
                   '---.': 'ч',
                   '--.': 'г',
                   '--.-': 'щ',
                   '--..': 'з',
                   '-.': 'н',
                   '-.-': 'к',
                   '-.--': 'ы',
                   '-.-.': 'ц',
                   '-..': 'д',
                   '-...': 'б',
                   '.': 'е',
                   '.-': 'а',
                   '.--': 'в',
                   '.---': 'й',
                   '.--.': 'п',
                   '.-.': 'р',
                   '.-.-': 'я',
                   '.-..': 'л',
                   '..': 'и',
                   '..-': 'у',
                   '..--': 'ю',
                   '..-.': 'ф',
                   '..-..': 'э',
                   '...': 'с',
                   '...-': 'ж',
                   '....': 'х',
                   '-----': '0',
                   '----.': '9',
                   '---..': '8',
                   '--..--': '!',
                   '--...': '7',
                   '-.--.': '(',
                   '-.--.-': ')',
                   '-..-.': '/',
                   '-....': '6',
                   '-....-': '-',
                   '.----': '1',
                   '.-.-.-': '.',
                   '..---': '2',
                   '..--..': '?',
                   '...--': '3',
                   '....-': '4',
                   '.....': '5',
                   '\n': '\n',
                   '.--.-.': 'ъ',
                   '.-.-.-': ',',
                   '......': '.',
                   '.-..-.': '"',
                   }
morze = {'a': '.-',
         'b': '-...',
         'c': '-.-.',
         '\n': '\n',
         'd': '-..',
         'e': '.',
         'f': '..-.',
         'g': '--.',
         'h': '....',
         'i': '..',
         'j': '.---',
         'k': '-.-',
         'l': '.-..',
         'm': '--',
         'n': '-.',
         'o': '---',
         'p': '.--.',
         'q': '--.-',
         'r': '.-.',
         's': '...',
         't': '-',
         'u': '..-',
         'v': '...-',
         'w': '.--',
         'x': '-..-',
         'y': '-.--',
         'z': '--..',
         '1': '.----',
         '2': '..---',
         '3': '...--',
         '4': '....-',
         '5': '.....',
         '6': '-....',
         '7': '--...',
         '8': '---..',
         '9': '----.',
         '0': '-----',
         ',': '.-.-.-',
         '.': '......',
         '?': '..--..',
         '/': '-..-.',
         '-': '-....-',
         '(': '-.--.',
         ')': '-.--.-',
         '!': '--..--',
         '\n': '\n',
         '': '',
         '"': '.-..-.'
         }
demorze = {'-': 't',
           '--': 'm',
           '---': 'o',
           '-----': '0',
           '\n': '\n',
           '': '',
           '----.': '9',
           '---..': '8',
           '--.': 'g',
           '--.-': 'q',
           '--..': 'z',
           '--..--': '!',
           '--...': '7',
           '-.': 'n',
           '-.-': 'k',
           '-.--': 'y',
           '-.--.': '(',
           '-.--.-': ')',
           '-.-.': 'c',
           '-..': 'd',
           '-..-': 'x',
           '-..-.': '/',
           '-...': 'b',
           '-....': '6',
           '-....-': '-',
           '.': 'e',
           '.-': 'a',
           '.--': 'w',
           '.---': 'j',
           '.----': '1',
           '.--.': 'p',
           '.-.': 'r',
           '.-.-.-': '.',
           '.-..': 'l',
           '..': 'i',
           '..-': 'u',
           '..---': '2',
           '..--..': '?',
           '..-.': 'f',
           '...': 's',
           '...-': 'v',
           '...--': '3',
           '....': 'h',
           '....-': '4',
           '.....': '5',
           '\n': '\n',
           '.-.-.-': ',',
           '......': '.',
           '.-..-.': '"'
           }
japan_name_letters = {
    'А': 'ка',
    'И': 'ки',
    'Р': 'ши',
    'Ш': 'ли',
    'Б': 'зу',
    'Й': 'фу',
    'С': 'ари',
    'Щ': 'ни',
    'В': 'ру',
    'К': 'ме',
    'Т': 'чи',
    'Ъ': 'д',
    'Г': 'джи',
    'Л': 'та',
    'У': 'мей',
    'Ы': 'хе',
    'Д': 'те',
    'М': 'рин',
    'Ф': 'лу',
    'Ь': 'ксе',
    'Е': 'ку',
    'Ё': 'ку',
    'Н': 'то',
    'Х': 'ри',
    'Э': 'га',
    'Ж': 'зу',
    'О': 'мо',
    'Ц': 'ми',
    'Ю': 'до',
    'З': 'з',
    'П': 'но',
    'Ч': 'зи',
    'Я': 'ма',
    '': '',
    ' ': ' '}


def japan_name(name):
    res = ''
    for i in name.upper():
        res += japan_name_letters[i]
    res = res.capitalize()
    return res


def encode_to_morse(message):
    # декодер
    cipher = ''
    message = message.lower()
    for letter in message:
        if letter != ' ':
            try:
                cipher += morze[letter] + ' '
            except KeyError:
                cipher += 'Неопределенный символ'
        else:
            cipher += ' '
    return cipher


def decode_to_morse(message):
    message += ' '

    decipher = ''
    citext = ''
    i = 0
    for letter in message:

        # checks for space
        if (letter != ' '):

            # counter to keep track of space
            i = 0

            # storing morse code of a single character
            citext += letter

        # in case of space
        else:
            # if i = 1 that indicates a new character
            i += 1

            # if i = 2 that indicates a new word
            if i == 2:

                # adding space to separate words
                decipher += ' '
            else:

                # accessing the keys using their values (reverse of encryption)
                try:
                    decipher += list(morze.keys()
                                     )[list(morze.values()).index(citext)]
                    citext = ''
                except Exception:
                    pass

    return decipher


def rus_to_morze(message):
    cipher = ''
    message = message.lower()
    for letter in message:
        if letter != ' ':
            try:
                cipher += russian_morze[letter] + ' '
            except KeyError:
                cipher += 'Неопределенный символ'
        else:
            cipher += ' '
    return cipher


def morze_to_rus(message):
    # extra space added at the end to access the
    # last morse code
    message += ' '

    decipher = ''
    citext = ''
    i = 0
    for letter in message:

        # checks for space
        if (letter != ' '):

            # counter to keep track of space
            i = 0

            # storing morse code of a single character
            citext += letter

        # in case of space
        else:
            # if i = 1 that indicates a new character
            i += 1

            # if i = 2 that indicates a new word
            if i == 2:

                # adding space to separate words
                decipher += ' '
            else:

                # accessing the keys using their values (reverse of encryption)
                try:
                    decipher += list(russian_morze.keys()
                                     )[list(russian_morze.values()).index(citext)]
                    citext = ''
                except Exception:
                    pass
    return decipher