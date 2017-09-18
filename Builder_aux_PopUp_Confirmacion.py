
########## Builder Auxiliar ################
############################################

## Pupil Widget

PopUp_Confirmacion = '''
<ContenidoPopup_Confirmacion>
    orientation:'vertical'
    Label:
        text:'Seguro que quieres BORRARLO ????'
    BoxLayout:
        id:_BoxOkCancel_conf
        orientation:'horizontal'
        Button:
            id:_OK_popup_conf
            text:'OK'
            on_release: root.ok_conf()
        Button:
            id:_Cancel_popup_conf
            text:'Cancel'
            on_release:root.cancel_conf()
'''
###########################################