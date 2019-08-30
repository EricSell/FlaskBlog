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


# ==================== 管理 ====================

@admin.route('/adminlogin/')


# 管理首页
@admin.route('/admin/', methods=['POST', 'GET'])
def admin_index():
    if request.method == "GET":
        return render_template('admin/login.html')
    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("userpwd")

        user = User.query.filter_by(is_super=True).filter_by(name=username).first()
        if user:
            if password == user.password:

                user.loginsum += 1
                try:
                    db.session.add(user)
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return "操作失败"

                session['user'] = username

                username = user.name
                article_sum = Article.query.filter().count()
                command_sum = Command.query.filter().count()
                reader_list = Article.query.filter(Article.readersum.__gt__(0)).all()
                reader_sum = 0
                for i in reader_list:
                    reader_sum += i.readersum
                loginsum = User.query.filter_by(name=username).first().loginsum

                ip = user.IP
                logindate = user.logindate
                data = {
                    'username': username,
                    'article_sum': article_sum,
                    'command_sum': command_sum,
                    'reader_sum': reader_sum,
                    'loginsum': loginsum,
                    'ip': ip,
                    'logindate': logindate,
                }
                user.IP = request.remote_addr
                user.logindate = datetime.datetime.now()
                try:
                    db.session.add(user)
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
                    return "操作失败"

                return render_template('admin/index.html', **data)
            else:
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
            print(data)
            return render_template('admin/login.html', **data)


# 文章管理
@admin.route('/admin/article/')
def admin_article():
    user = session.get('user', default=None)
    if not user:
        return render_template('admin/login.html')
    else:
        user = User.query.filter_by(name=user).first()
        username = user.name
        data = {
            'username': username
        }
    return render_template('admin/article.html', **data)


# 栏目管理
@admin.route('/admin/category/')
def admin_category():
    user = session.get('user', default=None)
    if not user:
        return render_template('admin/login.html')
    else:
        user = User.query.filter_by(name=user).first()
        username = user.name
        data = {
            'username': username
        }
    return render_template('admin/category.html', **data)


# 评论管理
@admin.route('/admin/command/')
def admin_command():
    user = session.get('user', default=None)
    if not user:
        return render_template('admin/login.html')
    else:
        user = User.query.filter_by(name=user).first()
        username = user.name
        data = {
            'username': username
        }
    return render_template('admin/comment.html', **data)


# 用户管理
@admin.route('/admin/manage_user/')
def admin_manage_user():
    user = session.get('user', default=None)
    if not user:
        return render_template('admin/login.html')
    else:
        user = User.query.filter_by(name=user).first()
        username = user.name
        data = {
            'username': username
        }
    return render_template('admin/manage-user.html', **data)



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
