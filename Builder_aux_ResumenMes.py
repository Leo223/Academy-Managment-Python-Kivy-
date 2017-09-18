#!/usr/bin/env python
# -*- coding: utf-8 -*-
########## Builder Auxiliar ################
############################################

# Importar en el main.py
#   from Builder_aux_ResumenMes import*
#   Builder.load_string(ResMes)
#

## Pupil Widget

ResMes = '''
<ResumenMes>
    BoxLayout:
        orientation: 'vertical'
        GridLayout:
            cols:2
            orientation: 'horizontal'
            size_hint_y: 0.2
            Label:
                text: 'Mes'
            Label:
                text: 'Año'

        ScrollView:
'''
###########################################