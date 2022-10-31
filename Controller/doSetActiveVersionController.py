from flask import request, render_template, redirect, url_for

from DAO import Seq2SeqDAO
from Model.Seq2Seq import Seq2Seq

def setActive():
    if request.method == 'POST':
        version = request.form['input']
        Seq2SeqDAO.setActiveModelSeq2Seq(version)
        return redirect(url_for('versionManagement'))
    seq2SeqList = Seq2SeqDAO.getSeq2SeqList()
    return render_template("/server/versionManagement.html", data=seq2SeqList)
