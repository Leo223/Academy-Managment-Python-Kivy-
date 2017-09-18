# -*- coding: utf-8 -*-
########## Builder Auxiliar ################
############################################

## Pupil Widget

### 3 importaciones de nombre

pupil_box_str_new = '''
BoxLayout:
    #id: pupil_%s
    height: '70sp'
    size_hint_y: None
    background_color: .8,.8,0,1
    padding: '5dp'
    # canvas:
    #     Color:
    #         rgb: .3, .3, .3
    #     Rectangle:
    #         pos: self.pos
    #         size: self.size
    # CheckBox:
    #     text: ''
    #     size_hint_x: None
    #     width: self.height

    # Image:
    #     source: 'cross.png'
    #     size_hint_x: None
    #     width: self.height

    ToggleButton:
        disabled:True
        font_size:50
        background_down:'./Images/check.png'
        background_normal:'./Images/cross.png'
        size_hint_x: None
        width: self.height

    BoxLayout:
        id:horas_%s
        size_hint_x: 0.01

    ToggleButton:
        id: Borrar_pupil_%s
        text: 'B'
        # font_size:20
        size_hint_x: None
        width: self.height
        on_press:app.Popup_Remove_pupil_Conf()

    Button:
        id: Button_pupil_%s
        # font_size:20
        text: '%s'
        on_press:app.Desplegable_pupil_options(Button_pupil_%s.text)

    Button:
        id: cal_%s
        # text: '>'
        background_normal:'./Images/Calendario_N.png'
        background_down:'./Images/Calendario_P.png'
        font_size:80
        image:'next.png'
        size_hint_x: None
        width: self.height
        on_release:app.Switch_to_Calendar_screen(Button_pupil_%s.text)
            '''
###########################################