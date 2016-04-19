#!/usr/bin/python 

import pexpect

# patch slowPrint delay
f = open('poc.exe','r+b')
f.seek(0x76e) # offset of the delay in ms
f.write('\x00')
f.close()

p = pexpect.spawn('wine poc.exe')

while True:
    i = p.expect([' > ',':D'])

    if not i:
        for line in p.before.splitlines():
            if 'Question' in line:
                question = line.split()
                qnum = int(question[1])
                o = question[8].replace('modulus','%').replace('sum','+').replace('product','*').replace('difference','-')
                r = question[10]
                s = question[12].strip('?')

                # do base conversions
                if r.startswith('0x'):
                    r = int(r,16)   # hex
                elif r.startswith('0'):
                    r = int(r,8)   # oct
                else:
                    r = int(r,10)  # decimal

                if s.startswith('0x'):
                    s = int(s,16)   # hex
                elif s.startswith('0'):
                    s = int(s,8)
                else:
                    s = int(s,10) # decimal

                result = eval(str(r) + o + str(s)) # most problems solve here
                if '-' in o and s>r: # except difference when s>r
                    result = s - r

                print "[*] Question " + str(qnum) + " solution: "+ str(result)
        
                p.sendline(str(result))
    else:
        print '[+] Flag: ' + p.before.splitlines()[1] + ':D'
        quit()

