import cv2
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView  # Import ScrollView for scrollable checkboxes
from kivy.uix.popup import Popup  # Import Popup for custom dialogs
from kivy.uix.textinput import TextInput
import gemine
import detection

# Global variables for styling
FONT_SIZE = '14sp'
BUTTON_COLOR = (0.043, 0.611, 0.192, 1)  # Green
TEXT_COLOR = (0.1, 0.1, 0.1, 1)  # Dark grey
BACKGROUND_COLOR = (0.92, 0.94, 0.95, 1)  # Light greyish-blue
TEXTURE=None


class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)
        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=BUTTON_COLOR)  # Green color for button
            RoundedRectangle(pos=self.pos, size=self.size, radius=[20])


class RectangleButton(Button):
    def __init__(self, **kwargs):
        super(RectangleButton, self).__init__(**kwargs)
        self.bind(pos=self.update_shape, size=self.update_shape)

    def update_shape(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=BUTTON_COLOR)
            Rectangle(pos=self.pos, size=self.size)


# Screen for the Home page
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Top half for checklists
        top_half = BoxLayout(orientation='horizontal', size_hint=(1, 0.5))

        # Daily Diet Checklist
        diet_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1), spacing=10)
        diet_label = Label(text="Рекомендованное питание", font_size='24sp', color=TEXT_COLOR)
        self.diet_checklist = GridLayout(cols=1, size_hint_y=None, spacing=20)  # Increased spacing
        self.diet_checklist.bind(minimum_height=self.diet_checklist.setter('height'))
        diet_scroll = ScrollView(size_hint=(1, 1))
        diet_scroll.add_widget(self.diet_checklist)
        diet_layout.add_widget(diet_label)
        diet_layout.add_widget(diet_scroll)
        top_half.add_widget(diet_layout)

        # Daily Exercise Checklist
        exercise_layout = BoxLayout(orientation='vertical', size_hint=(0.5, 1), spacing=10)
        exercise_label = Label(text="Рекомендованные упражнения", font_size='24sp', color=TEXT_COLOR)
        self.exercise_checklist = GridLayout(cols=1, size_hint_y=None, spacing=20)  # Increased spacing
        self.exercise_checklist.bind(minimum_height=self.exercise_checklist.setter('height'))
        exercise_scroll = ScrollView(size_hint=(1, 1))
        exercise_scroll.add_widget(self.exercise_checklist)
        exercise_layout.add_widget(exercise_label)
        exercise_layout.add_widget(exercise_scroll)
        top_half.add_widget(exercise_layout)

        layout.add_widget(top_half)

        self.add_widget(layout)

        # Initialize the checkboxes with sample data
        self.update_checklists()

    def update_checklists(self):
        # Example static recommendations for Daily Diet
        recommended_dishes = gemine.eating_plan()

        self.diet_checklist.clear_widgets()
        for dishes in recommended_dishes:
            label_dishes = Label(text=dishes, font_size=FONT_SIZE, color=TEXT_COLOR, halign='left')
            row = BoxLayout(size_hint_y=None, height='40dp', spacing=10)
            row.add_widget(label_dishes)
            self.diet_checklist.add_widget(row)

        # Example items for Daily Exercise 
        exercise_items = gemine.training_plan()
        self.exercise_checklist.clear_widgets()
        for item in exercise_items:
            checkbox = CheckBox(color=BUTTON_COLOR)  # Use button color for checkbox
            label = Label(text=item, font_size=FONT_SIZE, color=TEXT_COLOR)
            row = BoxLayout(size_hint_y=None, height='40dp')
            row.add_widget(checkbox)
            row.add_widget(label)
            self.exercise_checklist.add_widget(row)


# Screen for the Diet page
class DietScreen(Screen):
    def __init__(self, **kwargs):
        super(DietScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Input options
        input_options_layout = BoxLayout(orientation='horizontal', spacing=20)
        self.text_input = TextInput(hint_text="Введите название блюда", size_hint=(0.6, 1))
        take_photo_button = RoundedButton(text='Сделайте фото блюда', size_hint=(0.4, 1))
        take_photo_button.bind(on_press=self.open_camera_popup)
        input_options_layout.add_widget(self.text_input)
        input_options_layout.add_widget(take_photo_button)
        layout.add_widget(input_options_layout)

        # Submit button
        submit_button = RoundedButton(text='Загрузить фото/название', size_hint=(1, 0.1))
        submit_button.bind(on_press=self.submit_diet)
        layout.add_widget(submit_button)

        # Add a label to show the calories
        self.calories_label = Label(text="Калории: ", font_size=FONT_SIZE, color=TEXT_COLOR)
        layout.add_widget(self.calories_label)

        self.add_widget(layout)

    def open_camera_popup(self, instance):
        global TEXTURE
        content = BoxLayout(orientation='vertical')
        self.image = Image()
        self.image.texture = TEXTURE
        content.add_widget(self.image)

        # Button to take a picture
        take_picture_button = RoundedButton(text='Сделать фото', size_hint=(1, 0.1))
        take_picture_button.bind(on_press=self.take_picture)
        content.add_widget(take_picture_button)

        self.camera_popup = Popup(title="Camera", content=content, size_hint=(0.8, 0.8))
        self.camera_popup.open()

    def take_picture(self, instance):
        # Capture the picture
        self.image.export_to_png('captured_food.png')
        self.camera_popup.dismiss()

    def submit_diet(self, instance):
        # Get the diet input from either text or image
        diet_input = self.text_input.text if self.text_input.text else 'captured_food.png'
        
        if diet_input != 'captured_food.png':
            # Call the evaluate_calories function to get the calories
            calories = gemine.evaluate_calories(diet_input)
            self.calories_label.text = f"{diet_input} calories: {calories} kcal"
            # Update the calories label with the result
        
        else:
            calories = gemine.evaluate_calories_photo()
            self.calories_label.text = f"Dish calories: {calories} kcal"


        # Clear the input field after submission
        self.text_input.text = ""




# Screen for the Train page (with the video feed)
class TrainScreen(Screen):
    def __init__(self, **kwargs):
        super(TrainScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Image widget to display the video feed
        self.image = Image()
        layout.add_widget(self.image)

        # Create a horizontal layout to hold the training buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), padding=10, spacing=10)

        # Button for starting/stopping pullups
        self.pullups_active = False
        self.pullups_button = RoundedButton(
            text='Начать подтягивания',
            size_hint=(0.5, 1),
            pos_hint={'center_x': 0.5},
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        self.pullups_button.bind(on_press=self.toggle_pullups)

        # Button for starting/stopping pushups
        self.pushups_active = False
        self.pushups_button = RoundedButton(
            text='Начать Отжимания',
            size_hint=(0.5, 1),
            pos_hint={'center_x': 0.5},
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1),
        )
        self.pushups_button.bind(on_press=self.toggle_pushups)

        # Add both buttons to the horizontal button layout
        button_layout.add_widget(self.pullups_button)
        button_layout.add_widget(self.pushups_button)

        # Add the button layout to the main layout
        layout.add_widget(button_layout)

        self.add_widget(layout)

        # Capture video
        self.capture = cv2.VideoCapture(0)

        # Schedule the video frame updates
        Clock.schedule_interval(self.load_video, 1 / 30)

    def load_video(self, *args):
        global TEXTURE
        ret, frame = self.capture.read()
        cv2.resize(frame, (1500,1000))
        if self.pullups_active:
            frame = detection.main(ret, frame)
        elif self.pushups_active:
            frame = detection.main(ret, frame)
        self.image_frame = frame
        buffer = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture
        TEXTURE= texture

    def toggle_pullups(self, *args):
        self.pullups_active = not self.pullups_active
        self.pushups_active = False  # Disable pushups if pullups are active
        self.pullups_button.text = 'Закончить подтягивания' if self.pullups_active else 'Начать подтягивания'
        self.pushups_button.text = 'Начать отжимания'  # Reset pushups button text

    def toggle_pushups(self, *args):
        self.pushups_active = not self.pushups_active
        self.pullups_active = False  # Disable pullups if pushups are active
        self.pushups_button.text = 'Закончить отжимания' if self.pushups_active else 'Начать отжимания'
        self.pullups_button.text = 'Начать подтягивание'  # Reset pullups button text


class MainApp(App):
    def build(self):
        # Set the window background color for a smooth modern look
        Window.clearcolor = BACKGROUND_COLOR

        # ScreenManager to handle the three pages
        self.sm = ScreenManager()

        # Add screens to the ScreenManager
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(DietScreen(name='diet'))
        self.sm.add_widget(TrainScreen(name='train'))

        # Create a header with buttons
        header = BoxLayout(size_hint=(1, 0.1), padding=2, spacing=2)

        # Header buttons
        diet_button = RectangleButton(
            text='Питание',
            size_hint=(1, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        diet_button.bind(on_press=self.switch_to_diet)

        home_button = RectangleButton(
            text='Главная',
            size_hint=(1, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        home_button.bind(on_press=self.switch_to_home)

        train_button = RectangleButton(
            text='Тренировка',
            size_hint=(1, 1),
            background_color=(0, 0, 0, 0),
            color=(1, 1, 1, 1)
        )
        train_button.bind(on_press=self.switch_to_train)

        # Add buttons to the header layout
        header.add_widget(diet_button)
        header.add_widget(home_button)
        header.add_widget(train_button)

        # Main layout to combine header and ScreenManager
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(header)
        main_layout.add_widget(self.sm)

        return main_layout

    def switch_to_diet(self, *args):
        self.sm.current = 'diet'

    def switch_to_home(self, *args):
        self.sm.current = 'home'

    def switch_to_train(self, *args):
        self.sm.current = 'train'


if __name__ == '__main__':
    MainApp().run()