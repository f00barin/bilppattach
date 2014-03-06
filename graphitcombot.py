#!/usr/bin/python

from __future__ import print_function, unicode_literals, division
from collections import defaultdict as dd
import glob
import os
import re
import shutil
import numpy as np
import sys

bestlc = {}
taudevacc = dd(list)
taulcdict = dd(list)
taunormdict = dd(list)
direc = sys.argv[1]
inp = sys.argv[2]
maxobj = float(sys.argv[3])
os.chdir(direc)

for files in glob.glob("comdevaccl2pnn*with*.txt"):
    try:
        base = re.findall("comdevacc|l2pl1|l2pl2p|l2pnn|\d{3,5}|cl[e0-9\-\.]+|cb[e0-9-\.]+|lc[e0-9\.-]+|with", files)
        print(base)
        sample = int(base[2])
        ppt = str(base[6])
        regtype = str(base[1])
        cl = str(re.findall(r'[e0-9-\.]+', base[3])[0])
        cb = str(re.findall(r'[e0-9-\.]+',base[4])[0])
        lc = str(re.findall(r'[e0-9-\.]+',base[5])[0])
        scores = np.loadtxt(files)
        iteration = scores.argmax() + 1
        objective = np.loadtxt('comlog'+base[1]+base[2]+base[3]+base[4]+base[5]+base[6]+'.txt')
        cnorm = np.loadtxt('combonorm'+base[1]+base[2]+base[3]+base[4]+'eta'+lc+base[6]+'.txt')
        bnorm = np.loadtxt('bilnorm'+base[1]+base[2]+base[3]+base[4]+'eta'+lc+base[6]+'.txt')
        lnorm = np.loadtxt('linnorm'+base[1]+base[2]+base[3]+base[4]+'eta'+lc+base[6]+'.txt')
        tracc = np.loadtxt('comtracc'+base[1]+base[2]+base[3]+base[4]+base[5]+base[6]+'.txt')

    #    iteration = scores.argmax() + 1
        indicator = np.sort(objective)[-1]
        if indicator < maxobj:
            objcordlist = []

            for ind, val in enumerate(objective):
                objcordlist.append((ind+1, val))

            taulcdict[(float(cl),float(cb))].append((float(lc), objcordlist))
            taudevacc[(float(cl),float(cb))].append((float(lc), scores))
            taunormdict[(float(cl),float(cb))].append((float(lc), cnorm))

    except:
        continue

def printdict(inp):
    if inp == 'taulc':
        sortedtau = np.sort(taulcdict.keys()).tolist()
        for tau in sortedtau:
            printtop(tau)
            lcdict = dict(taulcdict[tau])
            sortedlc = np.sort(lcdict.keys()).tolist()
            for lc in sortedlc:
                bestobj = 1
                print ("\\addplot")
                print ("    coordinates{")
                print ("    ", ''.join(str(it) for it in lcdict[lc]))
                print ("    };")
                print ("   \\addlegendentry{lc=",lc,"}")
                try:
                    tempobj = ((lcdict[lc])[99])[1]
                    if bestobj > tempobj:
                        bestobj = tempobj
                        bestlc[tau] = (lc, bestobj)
                except:
                    bestlc[tau] = (lc, objective[-1])
                    continue

            bestset = [tau, bestlc[tau]]

            printbottom(bestset)


def printtop(val):
#    print ('\\begin{figure}')
    print ('\\begin{tikzpicture}')
    print ('\\begin{axis}[')
    print ('    title={Tau = ', val, '},')
    print ('    height=\\textwidth,')
    print ('    width=\\textwidth,')
    print ('    xlabel={Iterations},')
    print ('    ylabel={Objective},')
    print ('    legend style={at={(0.5, -0.5)}, anchor=west},')
    print ('    ymajorgrids=true,')
    print ('    xmajorgrids=true,')
    print ('    grid style=dashed,]')

def printbottom(bestset):
    print ('\\end{axis}')
    print ('\\end{tikzpicture}')
#    print('\\caption{For Tau = ',bestset[0], 'best LC = ', bestset[1][0], 'that obtains objective at iteration 99 = ', bestset[1][1], '}')
#    print ('\\end{figure}')
    print ('')
    print ('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print ('')

def printbest():
    print ('\\begin{itemize}')
    sortedtau = np.sort(bestlc.keys())
    for t in sortedtau:
        print ('\\item Tau = ', t, 'best lipschitz constant = ', bestlc[t][0])

    print ('\\end{itemize}')

def printdevacc(bestlc):
    bestscorelist = []
    bestiterlist = []
    bestnormlist = []
    for tau in np.sort(bestlc.keys()):
        lc = bestlc[tau][0]
        scoredict = dict(taudevacc[tau])
        normdict = dict(taunormdict[tau])
        best = (scoredict[lc]).max()
        itr = (scoredict[lc]).argmax()
        optnorm = (normdict[lc])[itr]
        bestscorelist.append((tau, best))
        bestiterlist.append(((tau,best), itr))
        bestnormlist.append((optnorm, best))

    printtop(0.1)
    print ("\\addplot")
    print ("    coordinates{")
    print ("    ", ''.join(str(it) for it in bestscorelist))
    print ("    };")
    best = dict(bestscorelist)[0]
    print ("\\addplot [red, no markers] coordinates {(-0.1,"+str(best)+") (1,"+str(best)+")};");
#    for it in bestiterlist:
#        coordinate = it[0]
#        itr = it[1]
#        print ("\\node[label={180:{(it="+str(itr+1)+","+str(coordinate[1])+")}},circle,fill,inner sep=2pt] at (axis cs:"+str(coordinate[0])+","+str(coordinate[1])+ ") {};")
    print ("   \\addlegendentry{Best score list for BiLinear Model}")
    printbottom((0, (0,0)))

    printtop(0.1)
    print ("\\addplot")
    print ("    coordinates{")
    print ("    ", ''.join(str(it) for it in bestnormlist))
    print ("    };")
    print ("   \\addlegendentry{Best score list for Linear Model}")
    printbottom((0, (0,0)))

print ("\\documentclass[]{article}")
print ("\\usepackage{pgfplots}")
print ("\\begin{document}")

printdict(inp)
printbest()
printdevacc(bestlc)

print ("\\end{document}")
