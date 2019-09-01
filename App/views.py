# url+视图函数
import random
from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session

from App.exts import cache
from .models import *

blog = Blueprint('blog', __name__)
admin = Blueprint('admin', __name__)


@blog.route('/')
def demo():
    return redirect(url_for('blog.index', page=1))


# 首页
@blog.route('/index/<string:page>')
def index(page):
    # 关于我
    s_user = User.query.filter_by(is_super=1).first()
    s_name = s_user.name
    s_content = s_user.content
    s_icon = s_user.icon
    # 我的相册
    s_photos = Photo.query.filter_by(user_id=s_user.id).all()

    page = int(page)
    per_page = 8
    # 文章列表
    articles = Article.query.paginate(page=page, per_page=per_page, error_out=False)

    data = {
        'name': s_name,
        'icon': s_icon,
        'content': s_content,
        'photos': s_photos,
        'articles': articles,
        'page': page,
    }

    data.update(get_column())
    return render_template('blog/index.html', **data)


# 文章列表
@blog.route('/articlelist/<string:id>/')
def article_list(id):
    # 关于我
    s_user = User.query.filter_by(is_super=1).first()
    s_name = s_user.name
    s_content = s_user.content
    s_icon = s_user.icon
    # 我的相册
    s_photos = Photo.query.filter_by(user_id=s_user.id).all()

    # 文章分类
    columns = Column.query.get(id)
    s_articles = columns.articles

    data = {
        'name': s_name,
        'icon': s_icon,
        'content': s_content,
        'photos': s_photos,
        's_articles': s_articles,
    }
    data.update(get_column())

    return render_template('blog/index.html', **data)


# 文章搜索
@blog.route('/search/')
def search():
    # 关于我
    s_user = User.query.filter_by(is_super=1).first()
    s_name = s_user.name
    s_content = s_user.content
    s_icon = s_user.icon
    # 我的相册
    s_photos = Photo.query.filter_by(user_id=s_user.id).all()

    kw = request.args.get('keyboard').strip()
    if kw != "":
        s_articles = Article.query.filter(Article.article_name.contains(kw))
    else:
        s_articles = Article.query.all()

    data = {
        'name': s_name,
        'icon': s_icon,
        'content': s_content,
        'photos': s_photos,
        's_articles': s_articles,
    }
    data.update(get_column())
    print(data)
    return render_template('blog/index.html', **data)


# 文章页
@blog.route('/info/<string:id>')
def info(id, per_page=1):
    # 文章部分
    page = Article.query.filter(Article.id.__le__(id)).count()
    article = Article.query.paginate(page, per_page, error_out=False)
    captcha = captchas()

    user_ip = request.remote_addr
    cache_ip = cache.get(user_ip)
    cache_aid = cache.get(int(id))
    if not cache_ip and not cache_aid:
        article.items[0].readersum += 1
        cache.set(user_ip, user_ip, timeout=10)
        cache.set(cache_aid, cache_aid, timeout=10)
        db.session.commit()

    data = {
        "article": article,
        'captcha': captcha,
    }
    data.update(get_column())
    data.update(get_type())

    return render_template('blog/info.html', **data)


# 留言
@blog.route('/command/')
def command():
    articleid = request.args.get('id')
    name = request.args.get('name')
    commands = request.args.get('command')

    article = Article.query.get(articleid)

    if article:
        usera = User.query.filter_by(name=name).first()
        if not usera:
            user = User()
            user.name = name
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
                error = "用户插入失败"
                data = {
                    'error': error,
                }
                return jsonify(data)
            userb = User.query.filter_by(name=name).first()
            command = Command()
            command.command = commands
            command.user_id = userb.id
            command.article_id = articleid
            try:
                db.session.add(command)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
                error = "评论插入失败"
                data = {
                    'error': error,
                }
                return jsonify(data)
        else:
            command = Command()
            command.command = commands
            command.user_id = usera.id
            command.article_id = articleid
            try:
                db.session.add(command)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
                error = "评论插入失败"
                data = {
                    'error': error,
                }
                return jsonify(data)
    else:
        data = {
            'error': '文章不存在',
        }
        return jsonify(data)

    userid = User.query.filter_by(name=name).first().id
    command_time = Command.query.filter(Command.user_id == userid, Command.article_id == articleid).first().time
    print(userid, command_time)
    data = {
        'name': name,
        'commands': commands,
        'time': command_time,
    }

    return jsonify(data)


# 验证码接口
@blog.route('/api/captcha')
def captcha():
    capt = captchas()
    data = {
        'captcha': capt,
    }
    return jsonify(data)


# 生成验证码
def captchas():
    capt = random.randint(1000, 9999)
    return capt


# ajax更换验证码
@blog.route('/api/change_captcha/', methods=['POST'])
def change_captcha():
    return jsonify({
        'captchas': captchas(),
    })


# 关于我
@blog.route('/about/')
def about():
    s_user = User.query.filter_by(is_super=1).first()
    s_name = s_user.name
    s_content = s_user.content
    s_icon = s_user.icon
    # 我的相册
    s_photos = Photo.query.filter_by(user_id=s_user.id).all()

    data = {
        'name': s_name,
        'icon': s_icon,
        'content': s_content,
        'photos': s_photos,
    }
    data.update(get_column())
    return render_template('blog/about.html', **data)


# 我的相册
@blog.route('/share/')
def share():
    # 文章列表
    data = {

    }
    data.update(get_column())
    return render_template('blog/share.html', **data)


# 我的日记
@blog.route('/list/<string:page>/')
def list(page):
    s_user = User.query.filter_by(is_super=1).first()
    s_name = s_user.name
    s_content = s_user.content
    s_icon = s_user.icon
    # 我的相册
    s_photos = Photo.query.filter_by(user_id=s_user.id).all()
    page = int(page)
    per_page = 8
    # 文章列表
    articles = Article.query.paginate(page=page, per_page=per_page, error_out=False)
    data = {
        'name': s_name,
        'icon': s_icon,
        'content': s_content,
        'photos': s_photos,
        'articles': articles,
    }
    data.update(get_column())
    return render_template('blog/list.html', **data)


# 标题留言
@blog.route('/gbook/')
def gbook():
    s_user = User.query.filter_by(is_super=1).first()
    s_name = s_user.name
    s_content = s_user.content
    s_icon = s_user.icon
    # 我的相册
    s_photos = Photo.query.filter_by(user_id=s_user.id).all()
    data = {
        'name': s_name,
        'icon': s_icon,
        'content': s_content,
        'photos': s_photos,
    }
    data.update(get_column())
    return render_template('blog/gbook.html', **data)


# 相册内容页
@blog.route('/infopic/')
def infopic():
    return render_template('blog/infopic.html')


# 管理登录
@admin.route('/adminlogin/', methods=['GET', 'POST'])
def admin_login():
    if request.method == "GET":
        return render_template('admin/login.html')
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("userpwd")

        user = User.query.filter_by(is_super=True).filter_by(name=username).first()
        if user:
            if password == user.password:

                session['user'] = username

                userlogin = UserLogin()
                userlogin.logindate = datetime.datetime.now()
                userlogin.s_id = user.id
                userlogin.is_success = True
                userlogin.IP = request.remote_addr

                try:
                    db.session.add(userlogin)
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return "操作失败"

                user = User.query.filter_by(is_super=True).filter_by(name=username).first()
                sum = user.userlogins.filter_by(is_success=True).all()
                print(sum)
                if sum:
                    sum = sum[-2].loginsum
                    print(sum)
                    userlogin.loginsum = sum + 1
                else:
                    userlogin.loginsum = 0

                try:
                    db.session.add(userlogin)
                    db.session.commit()
                    return redirect(url_for('admin.admin_index'))
                except:
                    db.session.rollback()
                    db.session.flush()
                    return "操作失败"
            else:
                userlogin = UserLogin()
                userlogin.logindate = datetime.datetime.now()
                userlogin.s_id = user.id
                userlogin.is_success = False
                userlogin.IP = request.remote_addr
                try:
                    db.session.add(userlogin)
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return "操作失败"
                data = {
                    'code': 1,
                    'msg': '密码错误',
                }
                return render_template('admin/login.html', **data)
        else:
            data = {
                'code': 2,
                'msg': '没有这个用户',
            }
            return render_template('admin/login.html', **data)


# 管理首页
@admin.route('/admin/', methods=['POST', 'GET'])
def admin_index():
    user = session.get('user')
    if user:
        user = User.query.filter_by(is_super=True).filter_by(name=user).first()
        username = user.name
        article_sum = Article.query.filter().count()
        command_sum = Command.query.filter().count()
        reader_list = Article.query.filter(Article.readersum.__gt__(0)).all()
        reader_sum = 0
        for i in reader_list:
            reader_sum += i.readersum

        # 获取登陆次数与登陆时间
        first_login = user.userlogins.all()
        if len(first_login) >= 2:
            ip = first_login[-2].IP
            logindate = first_login[-2].logindate
            loginsum = first_login[-1].loginsum
        else:
            ip = first_login[-1].IP
            logindate = first_login[-1].logindate
            loginsum = first_login[-1].loginsum

        # 管理员信息
        super_name = user.name
        super_idname = user.idname
        super_phone = user.phone
        super_oldpwd = user.password

        # 保存最新一次登陆ip与时间
        user.IP = request.remote_addr
        user.logindate = datetime.datetime.now()
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
            return "操作失败"

        # 获取管理员所有登陆次数与登陆时间
        super_logins = user.userlogins.all()[-5:]

        data = {
            'username': username,
            'article_sum': article_sum,
            'command_sum': command_sum,
            'reader_sum': reader_sum,
            'loginsum': loginsum,
            'ip': ip,
            'logindate': logindate,
            "super_name": super_name,
            "super_idname": super_idname,
            "super_phone": super_phone,
            "super_oldpwd": super_oldpwd,
            'super_logins': super_logins,
        }

        return render_template('admin/index.html', **data)
    else:
        return redirect(url_for('admin.admin_login'))


# 修改管理员信息
@admin.route('/updateadmin/', methods=['POST', 'GET'])
def admin_update():
    user = session.get('user')
    if not user:
        return redirect(url_for('admin.admin_login)'))

    name = request.form.get('username')
    idname = request.form.get('truename')
    phone = request.form.get('usertel')
    old_password = request.form.get('old_password')
    password = request.form.get('password')
    new_password = request.form.get('new_password')

    user = User.query.filter_by(is_super=True).filter_by(name=user).first()
    print(user)
    user.name = name
    user.idname = idname
    user.phone = phone
    user.old_password = old_password
    user.password = password
    user.new_password = new_password
    try:
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.admin_index'))
    except:
        db.session.rollback()
        db.session.flush()
        return "操作失败"


# 文章管理
@admin.route('/admin/article/<string:page>')
def admin_article(page):
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        user = User.query.filter_by(is_super=True).filter_by(name=user).first()

        # 管理员信息
        super_name = user.name
        super_idname = user.idname
        super_phone = user.phone
        super_oldpwd = user.password

        # 获取管理员所有登陆次数与登陆时间
        super_logins = user.userlogins.all()[-5:]

        # 获取用户名
        username = user.name

        # 获取所有文章
        articles = Article.query.all()
        article_sum = len(Article.query.all())
        articles = Article.query.paginate(page=int(page), per_page=8, error_out=False)

        data = {
            'username': username,
            'articles': articles,
            'article_sum': article_sum,
            "super_name": super_name,
            "super_idname": super_idname,
            "super_phone": super_phone,
            "super_oldpwd": super_oldpwd,
            'super_logins': super_logins,
        }

    return render_template('admin/article.html', **data)


# 添加文章首页
@admin.route('/admin/article/add-article-index/')
def admin_add_article_index():
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index', page=1))
    else:
        user = User.query.filter_by(is_super=True).filter_by(name=user).first()

        # 管理员信息
        super_name = user.name
        super_idname = user.idname
        super_phone = user.phone
        super_oldpwd = user.password

        # 获取管理员所有登陆次数与登陆时间
        super_logins = user.userlogins.all()[-5:]

        # 获取用户名
        username = user.name

        data = {
            'username': username,
            "super_name": super_name,
            "super_idname": super_idname,
            "super_phone": super_phone,
            "super_oldpwd": super_oldpwd,
            'super_logins': super_logins,
        }
        data.update(get_column())
        return render_template('admin/add-article.html', **data)


# 添加文章
@admin.route('/admin/article/add-article/', methods=['POST', 'GET'])
def admin_add_article():
    if request.method != 'POST':
        return redirect(url_for('admin.admin_article'))
    # 添加新文章
    title = request.form.get('title')
    content = request.form.get('content')
    keywords = request.form.get('keywords')
    describe = request.form.get('describe')
    category_id = request.form.get('category')
    titlepic = request.form.get('titlepic')

    article = Article()
    article.article_name = title
    article.article_content = content
    article.article_time = datetime.datetime.now()
    article.intro = describe
    article.pict = titlepic

    try:
        db.session.add(article)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
        return '添加文章失败'

    # 给文章添加标签
    types_list = keywords.split(',')
    for types in types_list:
        type = Type.query.filter_by(type_name=types).first()
        if type:
            pass
        else:
            type = Type()
            type.type_name = types
            try:
                db.session.add(type)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
                return "添加标签操作失败"
        type = Type.query.filter_by(type_name=type.type_name).first()
        article = Article.query.filter_by(article_name=title).first()
        article.types.append(type)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
            return "文章添加标签操作失败"

    # 栏目
    category_id = Column.query.get(category_id)
    article.columns.append(category_id)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
        return "文章添加栏目操作失败"

    return redirect(url_for('admin.admin_article', page=1))


# 修改文章主页
@admin.route('/admin/article/update-article-index/<string:id>/')
def admin_update_article_index(id):
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        # 是否存在文章
        uid = int(id)
        update_article = Article.query.filter_by(id=uid).first()

        if update_article:
            user = User.query.filter_by(is_super=True).filter_by(name=user).first()

            # 管理员信息
            super_name = user.name
            super_idname = user.idname
            super_phone = user.phone
            super_oldpwd = user.password

            # 获取管理员所有登陆次数与登陆时间
            super_logins = user.userlogins.all()[-5:]

            # 获取用户名
            username = user.name

            data = {
                'username': username,
                "super_name": super_name,
                "super_idname": super_idname,
                "super_phone": super_phone,
                "super_oldpwd": super_oldpwd,
                'super_logins': super_logins,
                'update_article': update_article,
            }
            data.update(get_column())
            return render_template('admin/update-article.html', **data)

        else:
            return redirect(url_for('admin.admin_article', page=1))


# 修改文章
@admin.route('/admin/article/update-article/<string:id>/', methods=['POST', 'GET'])
def admin_update_article(id):
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        if request.method != 'POST':
            return redirect(url_for('admin.admin_article', page=1))
        # 修改文章
        article = Article.query.filter_by(id=id).first()
        if article:
            title = request.form.get('title')
            content = request.form.get('content')
            keywords = request.form.get('keywords')
            describe = request.form.get('describe')
            category_id = request.form.get('category')
            titlepic = request.form.get('titlepic')

            article.article_name = title
            article.article_content = content
            article.article_time = datetime.datetime.now()
            article.intro = describe
            article.pict = titlepic

            try:
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
                return '添加文章失败'

            # 文章修改标签
            types_list = keywords.split(',')
            print(types_list)

            # 删除中间表 文章原有的标签
            article = Article.query.filter_by(id=id).first()
            for i in article.types.all():
                obj_type = Type.query.get(i.id)
                article.types.remove(obj_type)
                db.session.commit()

            # 添加标签
            for types in types_list:
                type = Type.query.filter_by(type_name=types).first()
                if type:
                    pass
                else:
                    type = Type()
                    type.type_name = types
                    try:
                        db.session.add(type)
                        db.session.commit()
                    except:
                        db.session.rollback()
                        db.session.flush()
                        return "添加标签操作失败"

                type = Type.query.filter_by(type_name=type.type_name).first()
                article = Article.query.filter_by(id=id).first()
                article.types.append(type)
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return "文章添加标签操作失败"
            # 栏目

            # 删除文章对应的栏目
            article = Article.query.filter_by(id=id).first()
            for i in article.columns.all():
                c_column = Column.query.get(i.id)
                article.columns.remove(c_column)
                db.session.commit()

            column = Column.query.filter_by(id=category_id).first()
            article = Article.query.filter_by(id=id).first()
            article.columns.append(column)
            # 添加文章对应的栏目
            try:
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
                return "文章添加栏目操作失败"
            return redirect(url_for('admin.admin_article', page=1))
        else:
            return redirect(url_for('admin.admin_update_article_index', id=id))


# 删除一篇文章
@admin.route('/admin/article/delete-article-single/<string:id>/')
def admin_delete_article_single(id):
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        article = Article.query.filter_by(id=id).first()
        if article:

            # 删除中间表 文章原有的标签
            for i in article.types.all():
                obj_type = Type.query.get(i.id)
                article.types.remove(obj_type)

            # 删除中间表 文章对应的栏目
            for i in article.columns.all():
                c_column = Column.query.get(i.id)
                article.columns.remove(c_column)

            # 删除文章对应的点赞信息
            for i in article.commands.all():
                db.session.delete(i)

            # 删除文章
            db.session.delete(article)
            try:
                db.session.commit()
            except:
                return '删除文章出错'
            return redirect(url_for('admin.admin_article', page=1))
        else:
            return redirect(url_for('admin.admin_update_article_index', id=id))


# 删除多篇文章
@admin.route('/admin/article/delete-article-muti/', methods=['POST', 'GET'])
def admin_delete_article_muti():
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        if request.method != 'POST':
            return redirect(url_for('admin.admin_article', page=1))

        article_id_list = request.form.getlist("checkbox[]")

        for article_id in article_id_list:
            article = Article.query.get(article_id)
            # 删除中间表 文章原有的标签
            for i in article.types.all():
                obj_type = Type.query.get(i.id)
                article.types.remove(obj_type)

            # 删除中间表 文章对应的栏目
            for i in article.columns.all():
                c_column = Column.query.get(i.id)
                article.columns.remove(c_column)

            # 删除文章对应的点赞信息
            for i in article.commands.all():
                db.session.delete(i)

            # 删除文章
            db.session.delete(article)
            try:
                db.session.commit()
            except:
                return '删除文章出错'
        return redirect(url_for('admin.admin_article', page=1))


# 评论管理
@admin.route('/admin/command/<string:page>/')
def admin_command(page):
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        user = User.query.filter_by(is_super=True).filter_by(name=user).first()

        # 管理员信息
        super_name = user.name
        super_idname = user.idname
        super_phone = user.phone
        super_oldpwd = user.password

        # 获取管理员所有登陆次数与登陆时间
        super_logins = user.userlogins.all()[-5:]

        # 获取用户名
        username = user.name

        # 获取所有文章
        article_sum = len(Command.query.all())
        commands = Command.query.paginate(page=int(page), per_page=8, error_out=False)
        data = {
            'username': username,
            'article_sum': article_sum,
            "super_name": super_name,
            "super_idname": super_idname,
            "super_phone": super_phone,
            "super_oldpwd": super_oldpwd,
            'super_logins': super_logins,
            'commands': commands,
        }
    return render_template('admin/comment.html', **data)


# 获取评论信息
@admin.route('/admin/get_command/', methods=['GET', 'POST'])
def admin_get_command():
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        if request.method != "POST":
            return redirect(url_for('/admin/command/1/'))
        c_id = request.form.get('c_id')
        # 获取所有文章
        command = Command.query.filter_by(id=c_id).first()
        command_id = command.id
        command_article = command.articles.article_name
        command_content = command.command
        data = {
            'command_id': command_id,
            'command_article': command_article,
            'command_content': command_content,
        }
    return jsonify(data)


# 删除一条评论信息
@admin.route('/admin/del_command/', methods=['GET', 'POST'])
def admin_del_command():
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        command_id = request.form.get('c_id')
        command = Command.query.get(command_id)
        if command:
            # 删除评论
            db.session.delete(command)
            try:
                db.session.commit()
            except:
                return jsonify({
                    'code': 2,
                    'msg': '删除失败',
                })
            return jsonify({
                'code': 1,
                'msg': '删除成功',
            })
        else:
            return redirect(url_for('admin.admin_update_article_index', id=id))


# 删除多条评论
@admin.route('/admin/del_muti_command/', methods=['GET', 'POST'])
def admin_del_muti_command():
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        command_list = request.form.getlist('checkbox[]')
        for command_id in command_list:
            command = Command.query.get(command_id)
            if command:
                # 删除评论
                db.session.delete(command)
                try:
                    db.session.commit()
                except:
                    return '删除失败'

        return redirect(url_for('admin.admin_command', page=1))


# 栏目管理
@admin.route('/admin/category/')
def admin_category():
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        user = User.query.filter_by(is_super=True).filter_by(name=user).first()

        # 管理员信息
        super_name = user.name
        super_idname = user.idname
        super_phone = user.phone
        super_oldpwd = user.password

        # 获取管理员所有登陆次数与登陆时间
        super_logins = user.userlogins.all()[-5:]

        # 获取用户名
        username = user.name

        # 获取父节点
        Father_columns = Column.query.filter_by(c_column=None).all()
        # 获取所有节点
        columns = Column.query.all()

        data = {
            'username': username,
            "super_name": super_name,
            "super_idname": super_idname,
            "super_phone": super_phone,
            "super_oldpwd": super_oldpwd,
            'super_logins': super_logins,
            'father_columns': Father_columns,
            'columns': columns,
        }
    return render_template('admin/category.html', **data)


# 添加栏目
@admin.route('/admin/add_category/', methods=['GET', 'POST'])
def admin_add_category():
    print(request.method)
    if request.method != 'POST':
        return redirect(url_for('admin.admin_category'))
    # 添加新栏目
    name = request.form.get('name')
    alias = request.form.get('alias')
    fid = request.form.get('fid')

    column = Column()
    column.column_name = name
    column.column_nickname = alias

    # 判断是否有父栏目
    if int(fid) == 0:
        pass
    else:
        column.c_column = fid

    try:
        db.session.add(column)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
        return '添加栏目失败'

    return redirect(url_for('admin.admin_category'))


# 修改栏目首页
@admin.route('/admin/article/update_column_index/<string:id>/')
def admin_update_column_index(id):
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        # 是否存在栏目
        cid = int(id)
        update_column = Column.query.get(cid)

        if update_column:
            user = User.query.filter_by(is_super=True).filter_by(name=user).first()

            # 管理员信息
            super_name = user.name
            super_idname = user.idname
            super_phone = user.phone
            super_oldpwd = user.password

            # 获取管理员所有登陆次数与登陆时间
            super_logins = user.userlogins.all()[-5:]

            # 获取父节点
            Father_columns = Column.query.filter_by(c_column=None).all()

            # 获取用户名
            username = user.name

            data = {
                'username': username,
                "super_name": super_name,
                "super_idname": super_idname,
                "super_phone": super_phone,
                "super_oldpwd": super_oldpwd,
                'super_logins': super_logins,
                'update_column': update_column,
                'father_columns': Father_columns,
            }
            data.update(get_column())
            return render_template('admin/update-category.html', **data)

        else:
            return redirect(url_for('admin.admin_article', page=1))


# 修改栏目
@admin.route('/admin/update_category/<string:id>/', methods=['POST', 'GET'])
def admin_update_category(id):
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:

        if request.method != 'POST':
            return redirect(url_for('admin.admin_update_category', id=id))
        # 修改文章
        column_id = int(id)
        column = Column.query.get(column_id)
        if column:
            # 添加新栏目
            name = request.form.get('name')
            alias = request.form.get('alias')
            fid = request.form.get('fid')

            # 判断名字是否相同
            columns_all = Column.query.all()
            for column in columns_all:
                if column.column_name == name:
                    return "修改失败,栏目名称不能相同"

            # 判断是否有父栏目
            if int(fid) == 0:
                column.column_name = name
                column.column_nickname = alias
                try:
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return '修改栏目失败'
            else:
                column = Column()
                column.column_name = name
                column.column_nickname = alias
                column.c_column = fid
                try:
                    db.session.add(column)
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return '修改栏目失败'

            return redirect(url_for('admin.admin_category'))
        else:
            return redirect(url_for('admin.admin_update_category', id=column_id))

# 删除栏目
@admin.route('/admin/del_category/',methods=['POST','GET'])
def admin_del_category():
    user = session.get('user', default=None)
    if not user:
        return redirect(url_for('admin.admin_index'))
    else:
        id = request.form.get('id')
        column = Column.query.filter_by(id=id).first()
        if column:
            # 栏目下的所有文章
            articles = column.articles


            for article in articles:
                # 删除中间表 文章原有的标签
                for i in article.types.all():
                    obj_type = Type.query.get(i.id)
                    article.types.remove(obj_type)

                # 删除中间表 文章对应的栏目
                for i in article.columns.all():
                    c_column = Column.query.get(i.id)
                    article.columns.remove(c_column)

                # 删除文章对应的点赞信息
                for i in article.commands.all():
                    db.session.delete(i)

                # 删除文章
                db.session.delete(article)

            # 删除栏目
            db.session.delete(column)
            try:
                db.session.commit()
            except:
                return jsonify({
                    'code': 2,
                    'msg': '删除失败',
                })
            return jsonify({
                'code': 1,
                'msg': '删除成功',
            })
        else:
            return redirect(url_for('admin.admin_update_column_index', id=id))


# 用户管理
# @admin.route('/admin/manage_user/')
# def admin_manage_user():
#     user = session.get('user', default=None)
#     if not user:
#         return redirect(url_for('admin.admin_index'))
#     else:
#         user = User.query.filter_by(is_super=True).filter_by(name=user).first()
#
#         # 管理员信息
#         super_name = user.name
#         super_idname = user.idname
#         super_phone = user.phone
#         super_oldpwd = user.password
#
#         # 获取管理员所有登陆次数与登陆时间
#         super_logins = user.userlogins.all()[-5:]
#
#         # 获取用户名
#         username = user.name
#
#
#         data = {
#             'username': username,
#             "super_name": super_name,
#             "super_idname": super_idname,
#             "super_phone": super_phone,
#             "super_oldpwd": super_oldpwd,
#             'super_logins': super_logins,
#         }
#
#     return render_template('admin/manage-user.html', **data)




# 用户登出
@admin.route('/admin/logout/')
def admin_logout():
    session.clear()
    return redirect(url_for('admin.admin_index'))


# 分类
def get_type():
    types = Type.query.all()
    data = {
        "types": types
    }
    return data


# 栏目
def get_column():
    columns = Column.query.all()
    data = {
        "columns": columns,
    }
    return data
