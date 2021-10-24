function p(t, e) {
    var n = (65535 & t) + (65535 & e);
    return (t >> 16) + (e >> 16) + (n >> 16) << 16 | 65535 & n
}

function a(t, e, n, r, o, i) {
    return p((s = p(p(e, t), p(r, i))) << (a = o) | s >>> 32 - a, n);
    var s, a
}

function l(t, e, n, r, o, i, s) {
    return a(e & n | ~e & r, t, e, o, i, s)
}

function f(t, e, n, r, o, i, s) {
    return a(e & r | n & ~r, t, e, o, i, s)
}

function m(t, e, n, r, o, i, s) {
    return a(e ^ n ^ r, t, e, o, i, s)
}

function h(t, e, n, r, o, i, s) {
    return a(n ^ (e | ~r), t, e, o, i, s)
}

function c(t, e) {
    t[e >> 5] |= 128 << e % 32,
        t[14 + (e + 64 >>> 9 << 4)] = e;
    var n, r, o, i, s, a = 1732584193,
        c = -271733879,
        u = -1732584194,
        d = 271733878;
    for (n = 0; n < t.length; n += 16)
        a = l(r = a, o = c, i = u, s = d, t[n], 7, -680876936),
        d = l(d, a, c, u, t[n + 1], 12, -389564586),
        u = l(u, d, a, c, t[n + 2], 17, 606105819),
        c = l(c, u, d, a, t[n + 3], 22, -1044525330),
        a = l(a, c, u, d, t[n + 4], 7, -176418897),
        d = l(d, a, c, u, t[n + 5], 12, 1200080426),
        u = l(u, d, a, c, t[n + 6], 17, -1473231341),
        c = l(c, u, d, a, t[n + 7], 22, -45705983),
        a = l(a, c, u, d, t[n + 8], 7, 1770035416),
        d = l(d, a, c, u, t[n + 9], 12, -1958414417),
        u = l(u, d, a, c, t[n + 10], 17, -42063),
        c = l(c, u, d, a, t[n + 11], 22, -1990404162),
        a = l(a, c, u, d, t[n + 12], 7, 1804603682),
        d = l(d, a, c, u, t[n + 13], 12, -40341101),
        u = l(u, d, a, c, t[n + 14], 17, -1502002290),
        a = f(a, c = l(c, u, d, a, t[n + 15], 22, 1236535329), u, d, t[n + 1], 5, -165796510),
        d = f(d, a, c, u, t[n + 6], 9, -1069501632),
        u = f(u, d, a, c, t[n + 11], 14, 643717713),
        c = f(c, u, d, a, t[n], 20, -373897302),
        a = f(a, c, u, d, t[n + 5], 5, -701558691),
        d = f(d, a, c, u, t[n + 10], 9, 38016083),
        u = f(u, d, a, c, t[n + 15], 14, -660478335),
        c = f(c, u, d, a, t[n + 4], 20, -405537848),
        a = f(a, c, u, d, t[n + 9], 5, 568446438),
        d = f(d, a, c, u, t[n + 14], 9, -1019803690),
        u = f(u, d, a, c, t[n + 3], 14, -187363961),
        c = f(c, u, d, a, t[n + 8], 20, 1163531501),
        a = f(a, c, u, d, t[n + 13], 5, -1444681467),
        d = f(d, a, c, u, t[n + 2], 9, -51403784),
        u = f(u, d, a, c, t[n + 7], 14, 1735328473),
        a = m(a, c = f(c, u, d, a, t[n + 12], 20, -1926607734), u, d, t[n + 5], 4, -378558),
        d = m(d, a, c, u, t[n + 8], 11, -2022574463),
        u = m(u, d, a, c, t[n + 11], 16, 1839030562),
        c = m(c, u, d, a, t[n + 14], 23, -35309556),
        a = m(a, c, u, d, t[n + 1], 4, -1530992060),
        d = m(d, a, c, u, t[n + 4], 11, 1272893353),
        u = m(u, d, a, c, t[n + 7], 16, -155497632),
        c = m(c, u, d, a, t[n + 10], 23, -1094730640),
        a = m(a, c, u, d, t[n + 13], 4, 681279174),
        d = m(d, a, c, u, t[n], 11, -358537222),
        u = m(u, d, a, c, t[n + 3], 16, -722521979),
        c = m(c, u, d, a, t[n + 6], 23, 76029189),
        a = m(a, c, u, d, t[n + 9], 4, -640364487),
        d = m(d, a, c, u, t[n + 12], 11, -421815835),
        u = m(u, d, a, c, t[n + 15], 16, 530742520),
        a = h(a, c = m(c, u, d, a, t[n + 2], 23, -995338651), u, d, t[n], 6, -198630844),
        d = h(d, a, c, u, t[n + 7], 10, 1126891415),
        u = h(u, d, a, c, t[n + 14], 15, -1416354905),
        c = h(c, u, d, a, t[n + 5], 21, -57434055),
        a = h(a, c, u, d, t[n + 12], 6, 1700485571),
        d = h(d, a, c, u, t[n + 3], 10, -1894986606),
        u = h(u, d, a, c, t[n + 10], 15, -1051523),
        c = h(c, u, d, a, t[n + 1], 21, -2054922799),
        a = h(a, c, u, d, t[n + 8], 6, 1873313359),
        d = h(d, a, c, u, t[n + 15], 10, -30611744),
        u = h(u, d, a, c, t[n + 6], 15, -1560198380),
        c = h(c, u, d, a, t[n + 13], 21, 1309151649),
        a = h(a, c, u, d, t[n + 4], 6, -145523070),
        d = h(d, a, c, u, t[n + 11], 10, -1120210379),
        u = h(u, d, a, c, t[n + 2], 15, 718787259),
        c = h(c, u, d, a, t[n + 9], 21, -343485551),
        a = p(a, r),
        c = p(c, o),
        u = p(u, i),
        d = p(d, s);
    return [a, c, u, d]
}

function u(t) {
    var e, n = "";
    for (e = 0; e < 32 * t.length; e += 8)
        n += String.fromCharCode(t[e >> 5] >>> e % 32 & 255);
    return n
}

function d(t) {
    var e, n = [];
    for (n[(t.length >> 2) - 1] = void 0,
        e = 0; e < n.length; e += 1)
        n[e] = 0;
    for (e = 0; e < 8 * t.length; e += 8)
        n[e >> 5] |= (255 & t.charCodeAt(e / 8)) << e % 32;
    return n
}

function r(t) {
    var e, n, r = "0123456789abcdef",
        o = "";
    for (n = 0; n < t.length; n += 1)
        e = t.charCodeAt(n),
        o += r.charAt(e >>> 4 & 15) + r.charAt(15 & e);
    return o
}

function o(t) {
    return unescape(encodeURIComponent(t))
}

function i(t) {
    return u(c(d(e = o(t)), 8 * e.length));
    var e
}

function s(t, e) {
    return function (t, e) {
        var n, r, o = d(t),
            i = [],
            s = [];
        for (i[15] = s[15] = void 0,
            16 < o.length && (o = c(o, 8 * t.length)),
            n = 0; n < 16; n += 1)
            i[n] = 909522486 ^ o[n],
            s[n] = 1549556828 ^ o[n];
        return r = c(i.concat(d(e)), 512 + 8 * e.length),
            u(c(s.concat(r), 640))
    }(o(t), o(e))
}
function getPwd (t, e, n) {
    return e ? n ? s(e, t) : r(s(e, t)) : n ? i(t) : r(i(t))
}

a = getPwd("1026581494@pjq", undefined, undefined);
console.log(a);