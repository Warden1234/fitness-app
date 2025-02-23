import google.generativeai as genai
import os

genai.configure(api_key=os.environ["API_KEY"])

model = genai.GenerativeModel('gemini-1.5-flash')

def training_plan():
    global model
    response1 = model.generate_content("Мои параметры: Рост 193 см, Вес 80 кг.Составь мне план тренировок на сегодняшний день, используя только упражнения бег, подтягивания и отжимания. Выведи только название упражнения,кол-во повторений. Не делай комментариев. На каждом упражнении определенное количество повторений.Выведи в формате в каждой новой строчке: время суток- упражнение - количество")
    return response1.text.split("\n")[:-1]


def eating_plan():
    global model
    response2 = model.generate_content("Мои параметры: Рост 193 см, Вес 80 кг.Составь мне план питания на сегодняшний день и выведи в конце суммарное количество калорий. Выведи только название блюда и его калорийность. Не делай комментариев. Выведи в формате в каждой новой строчке: Время суток- блюдо - калорийность")
    return response2.text.split("\n")[:-1]


def evaluate_calories(dish):
    global model
    response3 = model.generate_content(f"Я хочу съесть {dish}. Выведи количество калорий в этом блюде. Выведи только количество калорий. Выведи 1 приблизительное число.")
    return int(response3.text)


def evaluate_calories_photo():
    global model
    file=genai.upload_file('./captured_food.png')
    response4 = model.generate_content([file, f"Сделал фото еды. Выведи количество калорий в этом изображении. Выведи только количество калорий. Выведи 1 приблизительное число."])
    return int(response4.text)
