# -*- coding: utf-8 -*-
########## Builder Auxiliar ################
############################################

## NEW TAB

tab_str = '''
TabbedPanelItem:
    # border: (0, -20,0, -20)
    id:tab_%s
    text:'%s'
    background_normal:'./Images/tab_N.png'
    background_down:'./Images/tab_P.png'
    markup: True
    # font_size:30
    # on_release: app.check_active_tab()
    BoxLayout:
        ScrollView:
            # scroll_distance:100
            scroll_distance:100000000
            # scroll_timeout: 55
            scroll_timeout: 0.1
            do_scroll_y:True
            do_scroll_x:True
            # scroll_type: ['bars']
            GridLayout:
                id:grid_%s
                cols:1
                orientation: 'vertical'
                spacing:5
                size_hint_y:None
                height: self.minimum_height
                '''
