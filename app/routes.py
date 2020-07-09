
from selenium import webdriver
from app import app,login
from flask import render_template,redirect,url_for,flash
from app.form import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User,Uid_friend
import logging
import time
from app import db
import threading

browser = None
logging.basicConfig(
    filename='log.txt',
    filemode='a'
)

@app.route ("/")
@login.user_loader
@app.route ("/index")
def index():
        return render_template ("index.html")

@app.route ("/login" ,methods = ["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect (url_for('index'))
    login = LoginForm()

    if login.validate_on_submit():
        global browser
        browser = webdriver.Chrome()
        browser.get("http://m.facebook.com")

        user_name = browser.find_element_by_css_selector('#m_login_email')
        user_name.send_keys (login.username.data)
        pass_word = browser.find_element_by_css_selector('#m_login_password')
        pass_word.send_keys (login.password.data)
        submit = browser.find_element_by_css_selector('#u_0_4 > button')
        submit.click()

        time.sleep(3)
        check = None
        try:
            check = browser.find_element_by_css_selector("#root > div._7om2 > div > div > h3")
        except:
            pass
        if check:
            user = User.query.filter_by(username = login.username.data).first()
            if user is None:
                user = User (username = login.username.data)
                user.set_password(login.password.data)
                db.session.add(user)
                db.session.commit()
            login_user (user, remember= login.remember_me.data)
            return redirect (url_for('index'))
        flash ("dang nhap lai ")
        return redirect (url_for("login"))
    return render_template ("login.html" , form = login)

@app.route ('/logout')
def logout():
    logout_user()
    return redirect (url_for('login'))

@app.route ('/addfriend')
def addfriend():
    if current_user.is_authenticated:
        url = 'https://www.facebook.com/groups/CNTT.VN.2019/'
        global browser
        browser.get(url)
        time.sleep (2)
        thanh_vien = browser.find_element_by_css_selector ("")
        thanh_vien.click()
        sleep (2)
        
        i = 1
        while (True):
            name_element = browser.find_element_by_css_selector("#mount_0_0 > div > div > div.rq0escxv.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div > div.d2edcug0.cbu4d94t.j83agx80.bp9cbjyn > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div:nth-child(16) > div > div:nth-child(2) > div > div:nth-child({}) > div > div > div.ow4ym5g4.auili1gw.rq0escxv.j83agx80.buofh1pr.g5gj957u.i1fnvgqd.oygrvhab.cxmmr5t8.hcukyx3x.kvgmc6g5.tgvbjcpo.hpfvmrgz.qt6c0cv9.rz4wbd8a.a8nywdso.jb3vyjys.du4w35lb.bp9cbjyn.btwxx1t3.l9j0dhe7 > div.gs1a9yip.ow4ym5g4.auili1gw.rq0escxv.j83agx80.cbu4d94t.buofh1pr.g5gj957u.i1fnvgqd.oygrvhab.cxmmr5t8.hcukyx3x.kvgmc6g5.tgvbjcpo.hpfvmrgz.rz4wbd8a.a8nywdso.l9j0dhe7.du4w35lb.rj1gh0hx.f10w8fjw.pybr56ya > div > div > div:nth-child(1) > span > span > div > a".format(i))
            if name_element:
                name_element.click()
                time.sleep(2)
                
                profile_element = browser.find_element_by_css_selector ("#mount_0_0 > div > div > div.rq0escxv.l9j0dhe7.du4w35lb > div:nth-child(4) > div > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div.iqfcb0g7.tojvnm2t.a6sixzi8.k5wvi7nf.q3lfd5jv.pk4s997a.bipmatt0.cebpdrjk.qowsmv63.owwhemhu.dp1hu0rb.dhp61c6y.l9j0dhe7.iyyx5f41.a8s20v7p > div > div > div > div > div.kr520xx4.pedkr2u6.ms05siws.pnx7fd3z.b7h9ocf4.pmk7jnqg.j9ispegn.k4urcfbm > div.dati1w0a.ihqw7lf3.hv4rvrfc.discj3wi.btwxx1t3.j83agx80.dwg5866k > div:nth-child(3) > a > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.taijpn5t.bp9cbjyn.owycx6da.btwxx1t3.c4xchbtz.by2jbhx6 > div:nth-child(2) > span")
                profile_element.click()
                time.sleep(2)
                id_url = browser.current_url
                browser.get ("https://id.atpsoftware.vn/")
                search_id = browser.find_element_by_css_selector("#top-content > div > div > div > div.main-slider.slick-initialized.slick-slider > div > div > div > div > div > div.row > div > div > form > div > div > div.input-items > input")
                search_id.send_keys (id_url )
                search_id = browser.find_element_by_css_selector ("#top-content > div > div > div > div.main-slider.slick-initialized.slick-slider > div > div > div > div > div > div.row > div > div > form > div > div > div.input-items > span > input")
                search_id.click()
                time.sleep(3)
                search_id = browser.find_element_by_css_selector ("#result > div > span")
                new_uid = Uid_friend (uid = search_id.text)
                db.session.add(new_uid)
                db.session.commit()
            i += 1
            if (i == 100 ):
                break
            else :
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


        # browsers = [webdriver.Chrome()]*5
        
        # def thead_add_friend (url,index):
        #     browsers[index].get ("http://m.facebook.com")
        #     user_name = browsers[index].find_element_by_css_selector('#m_login_email')
        #     user_name.send_keys (current_user.user_name.data)
        #     pass_word = browsers[index].find_element_by_css_selector('#m_login_password')
        #     pass_word.send_keys (current_user.password.data)
        #     submit = browsers[index].find_element_by_css_selector('#u_0_4 > button')
        #     submit.click()

        # if browser:
        #     url = 'https://www.facebook.com/groups/CNTT.VN.2019/'


        
    else :
        return redirect (url_for('login'))