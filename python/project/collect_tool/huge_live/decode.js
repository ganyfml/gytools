function decodeEnc(target)  {
    var n = new Uint8Array([65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 43, 47]),
        r = new Uint8Array([255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 62, 255, 255, 255, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 255, 255, 255, 0, 255, 255, 255, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 255, 255, 255, 255, 255, 255, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 255, 255, 255, 255]);

    var decodeWithJS = function(e, t) {
        if (!e || 0 == e.length)
            return new Uint8Array(0);
        var n = e.length % 4;
        if (1 === n)
            throw new Error("Invalid Base64 string: length % 4 == 1");
        2 === n ? e += "==" : 3 === n && (e += "="),
            t || (t = new Uint8Array(e.length));
        for (var i = 0, o = e.length, s = 0; s < o; s += 4) {
            var a = r[e.charCodeAt(s)] << 18 | r[e.charCodeAt(s + 1)] << 12 | r[e.charCodeAt(s + 2)] << 6 | r[e.charCodeAt(s + 3)];
            t[i++] = a >>> 16 & 255,
                t[i++] = a >>> 8 & 255,
                t[i++] = 255 & a
        }
        return 61 == e.charCodeAt(o - 1) && i--,
            61 == e.charCodeAt(o - 2) && i--,
            t.slice(0, i)
    }

    var res1 = decodeWithJS(target);

    var getCroppedBuffer = function(e, t, n, r) {
        void 0 === r && (r = 0);
        var i = new Uint8Array(n + r);
        var d = e.slice(t, t + n)
        for(let j = 0; j < d.length; ++j){
            i[j] = d[j];
        }
        return i
    }

    var doubleByteArrayCapacity = function(e) {
        var t = new Uint8Array(2 * e.length);
        for(let j = 0; j < e.length; ++j){
            i[j] = e[j];
        }
        return t;
    }

    var e = {};
    (function Decompressor(e) {
        var t = function() {
            function t() {
                this.MaximumMatchDistance = 32767,
                    this.outputPosition = 0
            }
            return t.prototype.decompressBlockToString = function(t) {
                    return t = e.BufferTools.convertToUint8ArrayIfNeeded(t),
                        e.decodeUTF8(this.decompressBlock(t))
                },
                t.prototype.decompressBlock = function(t) {
                    this.inputBufferRemainder && (t = e.ArrayTools.concatUint8Arrays([this.inputBufferRemainder, t]),
                        this.inputBufferRemainder = void 0);
                    for (var n = this.cropOutputBufferToWindowAndInitialize(Math.max(4 * t.length, 1024)), r = 0, i = t.length; r < i; r++) {
                        var o = t[r];
                        if (o >>> 6 == 3) {
                            var s = o >>> 5;
                            if (r == i - 1 || r == i - 2 && 7 == s) {
                                this.inputBufferRemainder = t.slice(r);
                                break
                            }
                            if (t[r + 1] >>> 7 === 1)
                                this.outputByte(o);
                            else {
                                var a = 31 & o,
                                    u = void 0;
                                6 == s ? (u = t[r + 1],
                                    r += 1) : (u = t[r + 1] << 8 | t[r + 2],
                                    r += 2);
                                for (var c = this.outputPosition - u, f = 0; f < a; f++)
                                    this.outputByte(this.outputBuffer[c + f])
                            }
                        } else
                            this.outputByte(o)
                    }
                    return this.rollBackIfOutputBufferEndsWithATruncatedMultibyteSequence(),
                        getCroppedBuffer(this.outputBuffer, n, this.outputPosition - n)
                },
                t.prototype.outputByte = function(t) {
                    this.outputPosition === this.outputBuffer.length && (this.outputBuffer = doubleByteArrayCapacity(this.outputBuffer)),
                        this.outputBuffer[this.outputPosition++] = t
                },
                t.prototype.cropOutputBufferToWindowAndInitialize = function(t) {
                    if (!this.outputBuffer)
                        return this.outputBuffer = new Uint8Array(t),
                            0;
                    var n = Math.min(this.outputPosition, this.MaximumMatchDistance);
                    if (this.outputBuffer = getCroppedBuffer(this.outputBuffer, this.outputPosition - n, n, t),
                        this.outputPosition = n,
                        this.outputBufferRemainder) {
                        for (var r = 0; r < this.outputBufferRemainder.length; r++)
                            this.outputByte(this.outputBufferRemainder[r]);
                        this.outputBufferRemainder = void 0
                    }
                    return n
                },
                t.prototype.rollBackIfOutputBufferEndsWithATruncatedMultibyteSequence = function() {
                    for (var e = 1; e <= 4 && this.outputPosition - e >= 0; e++) {
                        var t = this.outputBuffer[this.outputPosition - e];
                        if (e < 4 && t >>> 3 === 30 || e < 3 && t >>> 4 === 14 || e < 2 && t >>> 5 === 6)
                            return this.outputBufferRemainder = this.outputBuffer.slice(this.outputPosition - e, this.outputPosition),
                                void(this.outputPosition -= e)
                    }
                },
                t
        }();
        e.Decompressor = t
    })(e);

    var res2 = (new e.Decompressor()).decompressBlock(res1);

    var decodeWithJS2 = function(t, n, r) {
        if (void 0 === n && (n = 0),
            !t || 0 == t.length)
            return "";
        void 0 === r && (r = t.length);
        for (var i, o, s = [], a = n, u = r; a < u;) {
            if ((o = t[a]) >>> 7 === 0)
                i = o,
                a += 1;
            else if (o >>> 5 === 6) {
                if (a + 1 >= r)
                    throw new Error("Invalid UTF-8 stream: Truncated codepoint sequence encountered at position " + a);
                i = (31 & o) << 6 | 63 & t[a + 1],
                    a += 2
            } else if (o >>> 4 === 14) {
                if (a + 2 >= r)
                    throw new Error("Invalid UTF-8 stream: Truncated codepoint sequence encountered at position " + a);
                i = (15 & o) << 12 | (63 & t[a + 1]) << 6 | 63 & t[a + 2],
                    a += 3
            } else {
                if (o >>> 3 !== 30)
                    throw new Error("Invalid UTF-8 stream: An invalid lead byte value encountered at position " + a);
                if (a + 3 >= r)
                    throw new Error("Invalid UTF-8 stream: Truncated codepoint sequence encountered at position " + a);
                i = (7 & o) << 18 | (63 & t[a + 1]) << 12 | (63 & t[a + 2]) << 6 | 63 & t[a + 3],
                    a += 4
            }
            s.push(String.fromCharCode(i))
        }
        return s
    }

    return JSON.parse(decodeWithJS2(res2).join(''));
}