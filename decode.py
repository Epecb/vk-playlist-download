# -*- coding: utf-8 -*-
"""
Decode vk url for download mp3
"""
# TODO:  [ ] add comment for all function in module
# FIXME: [ ] invalid variable name

__vkstr__ = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/="


def check(url):
    """
    Check url
    """
    try:
        if len(url.split("audio_api_unavailable.mp3")) != 2:
            return False
        else:
            if len(url.split("?extra=")[1].split("#")) == 2:
                return True
            else:
                return False
    except IndexError:
        return False


# function o(t)
def decode(vstr, vk_id):
    """
    Extract direct link to mp3 from vk playlist url
    """

    vals = vstr.split("?extra=")[1].split("#")
    tstr = vk_o(vals[0])
    ops = vk_o(vals[1])
    ops_arr = ops.split(chr(9))
    vlen = len(ops_arr)
    for i in list(reversed(range(vlen))):
        args_arr = ops_arr[i].split(chr(11))
        op_ind = args_arr.pop(0)
        if op_ind == "v":
            tstr = vk_v(tstr)  # l.v
        elif op_ind == "r":  # l.r
            tstr = vk_r(tstr, int(args_arr[0]))
        elif op_ind == "x":  # l.x
            tstr = vk_x(tstr, args_arr[0])
        elif op_ind == "s":  # l.s
            tstr = vk_s(tstr, args_arr[0])
        elif op_ind == "i":  # l.i
            tstr = vk_i(tstr, args_arr[0], vk_id)
    return tstr


def vk_o(vstr):
    """
    function a(t) {
    """
    result = ""
    index2 = 0
    i = 0
    for j in range(len(vstr)):
        sym_index = __vkstr__.find(vstr[j])
        if sym_index != -1:
            # i = ((index2 % 4) != 0) ? ((i << 6) + sym_index) : sym_index
            i = ((i << 6) + sym_index) if ((index2 % 4) != 0) else sym_index
            if(index2 % 4) != 0:
                index2 += 1
                shift = -2 * index2 & 6
                result += chr(0xFF & (i >> shift))
            else:
                index2 += 1
    return result


# function s(t, e)
def vk_ss(v_t, v_e):
    """
    method s
    """
    i = len(v_t)
    v_o = []
    if i:
        v_a = i
        v_e = int(v_e)
        v_e = abs(v_e)
        while v_a:
            v_a = v_a - 1
            v_e = (i * (v_a + 1) ^ v_e + v_a) % i
            # v_e = (v_e + v_e * (v_a + i) / v_e)
            # v_o.append(v_e % i)
            v_o.append(v_e)
    return list(reversed(v_o))


# ----------------l{v,r,s,x}
# l.v
def vk_v(vstr):
    """
    Reverse vstr
    """
    if type(vstr) is str:
        return vstr[::-1]
    else:
        return False


# l.r
def vk_r(vstr, i):
    """
    method r
    """
    vk_str2 = __vkstr__ + __vkstr__
    vk_str2_len = len(vk_str2)
    vlen = len(vstr)
    result = ""
    for j in range(vlen):
        index = vk_str2.find(vstr[j])
        if index != -1:
            offset = (index - i)
            if offset < 0:
                offset += vk_str2_len
            result += vk_str2[offset]
        else:
            result += vstr[j]
    return result


# l.s
def vk_s(v_t, v_e):
    """
    method s
    """
    i = len(v_t)
    if i:
        v_o = vk_ss(v_t, v_e)
        v_a = 0
        v_t = list(v_t)
        v_a = 1
        while v_a < i:
            tmp = v_t[int(v_o[i - 1 - v_a])]
            v_t[int(v_o[i - 1 - v_a])] = v_t[v_a]
            v_t[v_a] = tmp
            v_a += 1
        return ''.join(v_t)


# i: function (t, e) {
# return l.s(t, e ^ vk.id)
# l.i
def vk_i(tstr, arg_arr, vk_id):
    """
    method i. too short for
    """
    # pass
    return vk_s(tstr, str(int(arg_arr) ^ int(vk_id)))


# l.x
def vk_x(vstr, vnum):
    """
    Xor byte in vstr with vnum
    """
    assert type(vstr) is str, "incorrect type"
    assert type(vnum) is str, "incorrect type"
    result = ""
    xor_val = ord(vnum[0])
    for i in vstr:
        result += chr(ord(i) ^ xor_val)
    return result
