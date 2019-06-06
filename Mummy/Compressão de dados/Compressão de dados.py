import base64

txt = open('menu_comprimido.txt', 'w')

with open('menu.png', 'rb') as imageFile:
    string = base64.b64encode(bytes(imageFile.read()))
    print(string)
    print(len(string))
    txt.write(str(string))

    with open('menu_cópia.png', 'wb') as imageFile2:
        str2 = base64.b64decode(bytes(string))
        imageFile2.write(str2)
        imageFile2.close()

txt.close()
