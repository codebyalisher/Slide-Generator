from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.list import OneLineListItem

KV = '''
BoxLayout:
    orientation: 'vertical'
    
    MDRaisedButton:
        text: 'New Slide'
        on_release: app.add_slide()
    
    MDScreenManager:
        id: screen_manager
        MDScreen:
            name: 'slide1'
        MDScreen:
            name: 'slide2'
'''


class PresentationApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.slide_count = 2  # Initial slides
        self.slides = {}  # Store slide widgets
        self.current_slide = 1
        return Builder.load_string(KV)

    def add_slide(self):
        # Create a new slide
        self.slide_count += 1
        slide_name = f'slide{self.slide_count}'
        screen_manager = self.root.ids.screen_manager
        screen_manager.add_widget(MDScreen(name=slide_name))
        self.slides[slide_name] = MDScreen(name=slide_name)
        self.show_slide(slide_name)

    def show_slide(self, slide_name):
        # Show the selected slide
        screen_manager = self.root.ids.screen_manager
        screen_manager.current = slide_name
        self.current_slide = int(slide_name[5:])  # Extract slide number

    def on_text_change(self, instance_textfield):
        # Apply text to the current slide
        slide_name = f'slide{self.current_slide}'
        self.slides[slide_name].clear_widgets()
        content = instance_textfield.text
        formatted_text = content.split('\n')
        for line in formatted_text:
            if line.strip().startswith('* '):
                # Create a bullet point
                list_item = OneLineListItem(text=line.strip()[2:])
                self.slides[slide_name].add_widget(list_item)
            else:
                # Create a heading
                heading = MDLabel(text=line, halign='center', font_style='H4')
                self.slides[slide_name].add_widget(heading)

    def build_slide(self, instance_button):
        # Add text formatting elements
        slide_name = f'slide{self.current_slide}'
        card = MDCard(
            size_hint=(None, None),
            size=(self.root.width, self.root.height / 2),
            padding=20,
        )
        text_field = MDTextField()
        text_field.bind(text=self.on_text_change)
        card.add_widget(text_field)
        self.slides[slide_name].add_widget(card)

    def on_start(self):
        # Create initial slides
        for i in range(1, self.slide_count + 1):
            slide_name = f'slide{i}'
            self.slides[slide_name] = MDScreen(name=slide_name)


if __name__ == '__main__':
    PresentationApp().run()
