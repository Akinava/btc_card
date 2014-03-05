import hashlib
import aes

b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def open_key_to_hesh160(open_key):
    return rhash(open_key)


def rhash(s):
    h160 = hashlib.new('ripemd160')
    h160.update(hashlib.sha256(s).digest())
    return h160.digest()


def dhash(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()


def hesh160_to_addr_v0(hesh160):
    return '\x00' + hesh160 + dhash('\x00' + hesh160)[0: 4]


def addr_v0_to_hesh160(addr_v0):
    return addr_v0[1: -4]


def str_to_base58(string):
    base58 = ''
    int_data = int(string.encode('hex'), 16)  # TODO
    while int_data >= len(b58chars):
        base58 = b58chars[int_data % len(b58chars)] + base58
        int_data = int_data / len(b58chars)
    base58 = b58chars[int_data % len(b58chars)] + base58
    for i in xrange(len(string)):
        if string[i] == '\x00':
            base58 = '1' + base58
        else:
            break
    return base58


def base58_to_str(base58):
    int_data = 0
    for i in xrange(-1, -len(base58) - 1, -1):
        int_data += (b58chars.index(base58[i])) * 58 ** (-i - 1)
    string = ('%048x' % int_data).decode('hex')  # TODO
    for i in xrange(len(base58)):
        if base58[i] == '1':
            string = '\x00' + string
        else:
            break
    return string


def encrypted(pwd, s):
    return str_to_base58(aes.encryptData(dhash(pwd), s))


def decrypted(pwd, s):
    return aes.decryptData(dhash(pwd), base58_to_str(s))


def key_dump_electrum_format(pk):
    pk = '\x80' + pk
    return str_to_base58(pk + dhash(pk)[0:4])
