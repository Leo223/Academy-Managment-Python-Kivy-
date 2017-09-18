
########## Builder Auxiliar ################
############################################

## Pupil Widget

PopUp_str = '''
<ContenidoPopup>
    orientation:'vertical'
    input_nombre:_input.text
    TextInput:
        id:_input
        text:''
        multiline:False
        focus: root.FocusTexto
        on_text_validate: root.ok()
    BoxLayout:
        id:_BoxOkCancel
        orientation:'horizontal'
        Button:
            id:_OK_popup
            text:'OK'
            on_release: root.ok()
        Button:
            id:_Cancel_popup
            text:'Cancel'
            on_release:root.cancel()
'''
###########################################