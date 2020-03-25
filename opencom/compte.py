from flask import (Blueprint, flash, g, redirect, url_for, render_template, request, session)

from werkzeug.exceptions import abort

from opencom.auth import login_required
from opencom.db import get_db

bp = Blueprint('compte', __name__, url_prefix='/compte')

@bp.route('listAll')
@login_required
def listAllAccount():
    return render_template('compte/listAll.html')


@bp.route('addAccount', methods=('GET','POST'))
def addAccount():
    if request.method=='POST':
        toto = dict()
        toto['toto']='robert'
        toto['tata']='roberta'
        return toto

    return render_template('compte/addAccount.html'
