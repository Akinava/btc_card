#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import sys
import os
from getpass import getpass
from datetime import datetime
import random

PATH = sys.path[0]
sys.path.append('%s/lib/python-qrcode-master' % PATH)
import qrcode
sys.path.append('%s/lib' % PATH)
import ecdsa
import utilit

############ settings
font = '%s/lib/DejaVuSansCondensed.ttf'
secret = '9EoV26vC9pxcaJQG3p4QJquowD7h3DPufYGqiZoX4yfZ'

# размеры в пикселях
# размер листа A4, ориентация альбомная A4 для печати переворачивается как
# книжная
paper_size = (2480, 3508)
sides = 2
# цвет фона листа белый
paper_color = (255, 255, 255)

#templat = False
templat = ('%s/templates/t_1_1.png', '%s/templates/t_1_2.png')

# отступ от верхнего левого угла листа
sketch_indent = (10, 10)
# отступ между картами
card_indent = (20, 20)
# колличество карт в ширину и длину на листе
card_number = (2, 5)
#card_number = (1, 1)
# размер карты
card_size = (1016, 638)
# границу карты отмечать по пикселям принадлежащим карте
card_border_inside = True
card_botder_type = 'line'  # point, line
card_border_color = (0, 0, 0)
# размер скретч слоя
scratch_size = (267, 267)
# отступ скретч слоя от верхнего левого угла карты
scratch_indent = (374, 126)
# границу слоя отмечать пикселями принадлежащими слою
scratch_border_inside = True
# как обозначить границу точки/линии
scratch_border_type = 'line'  # point, line
# цвет краницы скретч слоя
scratch_border_color = (0, 0, 0)
# сторона скретч слоя
scratch_side = 2
# скретч текстового ключа
scratch_key_size = (873, 67)
scratch_key_indent = (71, 474)
scratch_key_border_inside = True
scratch_key_border_type = 'line'
scratch_key_border_color = (0, 0, 0)
scratch_key_side = 2
# отступ текста приватного ключа от верхнего левого угла карты
key_indent = (105, 490)
key_fontsize = 26
key_text_color = (0, 0, 0)
key_side = 2

# отступ текста адреса от верхнего левого угла карты
address_indent = (82, 408)
address_fontsize = 42
address_text_color = (0, 0, 0)
address_side = 1
# key_qr
key_qr_indent = (391, 143)
key_qr_box_size = 8
key_qr_side = 2
# address_qr
address_qr_indent = (696, 82)
address_qr_box_size = 8
address_qr_side = 1
############ settings


# ширина, высота / Magic number
width, height = 0, 1

TIME_FORMAT = '%Y.%m.%d_%H.%M.%S'

# secp256k1, http://www.oid-info.com/get/1.3.132.0.10
_p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2FL
_r = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141L
_b = 0x0000000000000000000000000000000000000000000000000000000000000007L
_a = 0x0000000000000000000000000000000000000000000000000000000000000000L
_Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798L
_Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8L
curve_secp256k1 = ecdsa.ellipticcurve.CurveFp(_p, _a, _b)
generator_secp256k1 = ecdsa.ellipticcurve.Point(curve_secp256k1, _Gx, _Gy, _r)
oid_secp256k1 = (1, 3, 132, 0, 10)
SECP256k1 = ecdsa.curves.Curve("SECP256k1", curve_secp256k1, generator_secp256k1, oid_secp256k1)


def _draw_card_botder(coordinates, pages):
    for page in pages:
        card_border_coordinate = _border_coordinate(coordinates[pages.index(page)],
                                                    (0, 0),
                                                    card_size,
                                                    card_border_inside)
        _add_bordur(page, card_border_coordinate, card_botder_type, card_border_color)


def _draw_scratch_border(coordinates, pages):
    scratch_border_coordinate = _border_coordinate(coordinates[scratch_side - 1],
                                                   scratch_indent,
                                                   scratch_size,
                                                   scratch_border_inside)
    _add_bordur(pages[scratch_side - 1], scratch_border_coordinate, scratch_border_type, scratch_border_color)


def _draw_scratch_key_border(coordinates, pages):
    scratch_border_coordinate = _border_coordinate(coordinates[scratch_key_side - 1],
                                                   scratch_key_indent,
                                                   scratch_key_size,
                                                   scratch_key_border_inside)
    _add_bordur(pages[scratch_key_side - 1], scratch_border_coordinate, scratch_key_border_type, scratch_key_border_color)


def _border_coordinate(coordinate, indent, size, border_inside):
    border_coordinate = []
    if border_inside:
        diff = 0
    else:
        diff = 1
    for x, y in ((-diff, -diff), (size[width] + diff, -diff), (size[width] + diff, size[height] + diff), (-diff, size[height] + diff)):
        border_coordinate.append((coordinate[width] + indent[width] + x, coordinate[height] + indent[height] + y))
    return border_coordinate


def _add_bordur(img, border_coordinate, botder_type, border_color):
    imgDrawer = ImageDraw.Draw(img)
    if botder_type == 'line':
        _draw_line_border(imgDrawer, border_coordinate, border_color)
    if botder_type == 'point':
        _draw_point_border(imgDrawer, border_coordinate, border_color)
    del imgDrawer


def _draw_line_border(imgDrawer, border_coordinate, border_color):
    for n in xrange(4):
        imgDrawer.line((border_coordinate[n], border_coordinate[n + 1 if n + 1 < 4 else 0]), fill=border_color)


def _draw_point_border(imgDrawer, border_coordinate, border_color):
    for n in border_coordinate:
        imgDrawer.point(n, fill=border_color)


def _draw_pr_key(pr_key, coordinates, pages):
    _add_text(pr_key,
              key_indent,
              key_fontsize,
              key_text_color,
              coordinates[key_side - 1],
              pages[key_side - 1])


def _draw_address(address, coordinates, pages):
    _add_text(address,
              address_indent,
              address_fontsize,
              address_text_color,
              coordinates[address_side - 1],
              pages[address_side - 1])


def _add_text(text, indent, fontsize, text_color, coordinate, img):
    imgDrawer = ImageDraw.Draw(img)
    ttf = ImageFont.truetype(font % PATH, fontsize)
    imgDrawer.text(_get_coordinate(indent, coordinate), text, text_color, font=ttf)


def _draw_qr_pr_key(pr_key, coordinates, pages):
    _add_qr(pr_key,
            key_qr_indent,
            key_qr_box_size,
            coordinates[key_qr_side - 1],
            pages[key_qr_side - 1])


def _draw_qr_address(address, coordinates, pages):
    _add_qr(address,
            address_qr_indent,
            address_qr_box_size,
            coordinates[address_qr_side - 1],
            pages[address_qr_side - 1])


def _add_qr(text, indent, box_size, coordinate, img):
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=box_size, border=0)
    qr.add_data(text)
    img.paste(qr.make_image(), _get_coordinate(indent, coordinate))


def _get_coordinate(indent, coordinate):
    x = coordinate[width] + indent[width]
    y = coordinate[height] + indent[height]
    return x, y


def _draw_card(coordinates, pages, pwd):
    pr_key, address = _generate_data(pwd)
    _draw_card_botder(coordinates, pages)
    if templat:
        _draw_templat(coordinates, pages)
    _draw_scratch_border(coordinates, pages)
    _draw_scratch_key_border(coordinates, pages)
    _draw_pr_key(pr_key, coordinates, pages)
    _draw_address(address, coordinates, pages)
    _draw_qr_pr_key(pr_key, coordinates, pages)
    _draw_qr_address(address, coordinates, pages)


def _draw_templat(coordinates, pages):
    for x in xrange(len(pages)):
        if len(templat) < x:
            return
        tpl = Image.open(templat[x] % PATH)
        pages[x].paste(tpl, coordinates[x])


def _generate_data(pwd):
    secret = rnd(1, generator_secp256k1.order())
    pk = ecdsa.util.number_to_string(secret, generator_secp256k1.order())
    pub_ecdsa = ecdsa.ecdsa.Public_key(generator_secp256k1, generator_secp256k1 * secret)
    #priv_string = ('%064x' % secret).decode('hex')
    pub_string = ('04' + '%064x' % pub_ecdsa.point.x() + '%064x' % pub_ecdsa.point.y()).decode('hex')
    priv_b56 = utilit.key_dump_electrum_format(pk)
    address = utilit.str_to_base58(utilit.hesh160_to_addr_v0(utilit.open_key_to_hesh160(pub_string)))
    write_log(priv_b56, address, pwd)
    return priv_b56, address


def write_log(priv_key, address, pwd):
    if DEBUG:
        return

    log_path = "%s/log" % PATH
    _check_dir(log_path)

    encrypted_key = utilit.encrypted(pwd, priv_key)

    f = open("%s/%s.log" % (log_path, time_now().split("_")[0]), "a")
    f.write("%s %s %s %s\n" % (time_now(), encrypted_key, address, utilit.str_to_base58(utilit.dhash(utilit.dhash(pwd)))))
    f.close()


def time_now():
    return datetime.now().strftime(TIME_FORMAT)


def rnd(start, finish):
    randrange = random.SystemRandom().randrange
    return randrange(start, finish)


def _coordinates_card(x, y, pages):
    cc_xn = [sketch_indent[width] + x * (card_size[width] + card_indent[width])]
    cc_xn.append(paper_size[width] - sketch_indent[width] - ((x + 1) * card_size[width] + x * card_indent[width]))

    cc_list = []
    cc_y = sketch_indent[height] + y * (card_size[height] + card_indent[height])
    for i in pages:
        cc_list.append((cc_xn[pages.index(i)], cc_y))
    return cc_list


def _check_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


if __name__ == "__main__":
    DEBUG = False
    if '-d' in sys.argv:
        DEBUG = True
    print "start"
    if DEBUG:
        print "debug mode"
    pwd = ""
    if not DEBUG:
        while secret != utilit.str_to_base58(utilit.dhash(utilit.dhash(pwd))):
            pwd = getpass("secret: ")
    # создать листы
    pages = []

    if 1 > sides > 2:
        print "Error: wrong number pages"
        exit(1)

    pages = []
    for x in xrange(sides):
        pages.append(Image.new("RGB", paper_size, paper_color))

    # номер карточки
    for y in xrange(card_number[height]):
        for x in xrange(card_number[width]):
            _draw_card(_coordinates_card(x, y, pages), pages, pwd)

    pfx = rnd(0, 100)
    for page in pages:
        if DEBUG:
            page.show()
        else:
            # save
            count_s = "" if sides == 1 else "_%d" % pages.index(page)
            img_path = "%s/img" % PATH
            _check_dir(img_path)

            page.save("%s/img/%s%s_%d.tiff" % (PATH, time_now(), count_s, pfx), "TIFF")
