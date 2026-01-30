from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_login import LoginManager
from datetime import datetime, timedelta
import re
import os

from models import db, User, Post, Comment, Playlist, Review, Concert, Tag, Follow, Course
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173", "http://127.0.0.1:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "Authorization"]
    }
}, supports_credentials=True)

db.init_app(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)

@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin and origin in ["http://localhost:5173", "http://127.0.0.1:5173"]:
        response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

#БДшка
def init_db():
    with app.app_context():
        db.create_all()
        
        # Тестовый пользователь
        if User.query.count() == 0:
            admin = User(
                username='admin',
                email='admin@musblossom.com',
                bio='Основатель MusBlossom'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Тестовый пользователь
            test_user = User(
                username='testuser',
                email='test@musblossom.com',
                bio='Тестовый пользователь'
            )
            test_user.set_password('test123')
            db.session.add(test_user)
            
            db.session.commit()
            print("База данных инициализирована. Созданы пользователи admin и testuser")

# БД
with app.app_context():
    init_db()

#Аутентификация 
@app.route('/api/auth/register', methods=['POST'])
def api_register():
    """Регистрация нового пользователя"""
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Нет данных'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    bio = data.get('bio', '').strip()
    
    errors = {}
    
    #Валидация
    if not username:
        errors['username'] = 'Имя пользователя обязательно'
    elif len(username) < 3:
        errors['username'] = 'Имя должно содержать минимум 3 символа'
    elif User.query.filter_by(username=username).first():
        errors['username'] = 'Это имя пользователя уже занято'
    
    if not email:
        errors['email'] = 'Email обязателен'
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        errors['email'] = 'Некорректный email'
    elif User.query.filter_by(email=email).first():
        errors['email'] = 'Этот email уже зарегистрирован'
    
    if not password:
        errors['password'] = 'Пароль обязателен'
    elif len(password) < 6:
        errors['password'] = 'Пароль должен содержать минимум 6 символов'
    
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    
    try:
        user = User(
            username=username,
            email=email,
            bio=bio
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'message': 'Регистрация успешна!',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Нет данных'}), 400
    
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not email or not password:
        return jsonify({'success': False, 'error': 'Email и пароль обязательны'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        user.last_login = datetime.now()
        db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'success': True,
            'message': 'Вход выполнен',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
    else:
        return jsonify({'success': False, 'error': 'Неверный email или пароль'}), 401

@app.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def api_refresh():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
    
    new_access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'success': True,
        'access_token': new_access_token,
        'user': user.to_dict()
    }), 200

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def api_get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    }), 200

# Пользователи
@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id):
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    }), 200

@app.route('/api/users/<int:user_id>/posts', methods=['GET'])
def api_get_user_posts(user_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = Post.query.filter_by(user_id=user_id)\
        .order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    posts_data = [{
        'id': post.id,
        'title': post.title,
        'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
        'author': post.author.to_dict(),
        'post_type': post.post_type,
        'track_name': post.track_name,
        'artist_name': post.artist_name,
        'created_at': post.created_at.isoformat(),
        'likes_count': post.likes_count,
        'comments_count': post.comments_count
    } for post in posts.items]
    
    return jsonify({
        'success': True,
        'posts': posts_data,
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page
    }), 200

# Посты
@app.route('/api/posts', methods=['GET'])
def api_get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    post_type = request.args.get('type', None)
    
    query = Post.query
    
    if post_type:
        query = query.filter_by(post_type=post_type)
    
    posts = query.order_by(Post.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    posts_data = [{
        'id': post.id,
        'title': post.title,
        'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
        'author': post.author.to_dict(),
        'post_type': post.post_type,
        'track_name': post.track_name,
        'artist_name': post.artist_name,
        'created_at': post.created_at.isoformat(),
        'likes_count': post.likes_count,
        'comments_count': post.comments_count
    } for post in posts.items]
    
    return jsonify({
        'success': True,
        'posts': posts_data,
        'total': posts.total,
        'pages': posts.pages,
        'current_page': page
    }), 200
# Создание поста
@app.route('/api/posts', methods=['POST'])
@jwt_required()
def api_create_post():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Нет данных'}), 400
    
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    post_type = data.get('post_type', 'thought')
    track_id = data.get('track_id', '')
    track_name = data.get('track_name', '')
    artist_name = data.get('artist_name', '')
    
    errors = {}
    
    if not title:
        errors['title'] = 'Заголовок обязателен'
    if not content:
        errors['content'] = 'Содержание обязательно'
    
    if errors:
        return jsonify({'success': False, 'errors': errors}), 400
    
    try:
        post = Post(
            title=title,
            content=content,
            post_type=post_type,
            user_id=current_user_id,
            track_id=track_id,
            track_name=track_name,
            artist_name=artist_name
        )
        
        db.session.add(post)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Пост создан',
            'post': {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'post_type': post.post_type,
                'track_name': post.track_name,
                'artist_name': post.artist_name,
                'created_at': post.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def api_get_post(post_id):
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'success': False, 'error': 'Пост не найден'}), 404
    
    comments = Comment.query.filter_by(post_id=post_id)\
        .order_by(Comment.created_at.desc())\
        .all()
    
    return jsonify({
        'success': True,
        'post': {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'author': post.author.to_dict(),
            'post_type': post.post_type,
            'track_name': post.track_name,
            'artist_name': post.artist_name,
            'created_at': post.created_at.isoformat(),
            'likes_count': post.likes_count,
            'comments_count': post.comments_count
        },
        'comments': [comment.to_dict() for comment in comments]
    }), 200

#Коменты к постам
@app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def api_create_comment(post_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Нет данных'}), 400
    
    content = data.get('content', '').strip()
    
    if not content:
        return jsonify({'success': False, 'error': 'Комментарий не может быть пустым'}), 400
    
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'success': False, 'error': 'Пост не найден'}), 404
    
    try:
        comment = Comment(
            content=content,
            user_id=current_user_id,
            post_id=post_id
        )
        
        post.comments_count += 1
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Комментарий добавлен',
            'comment': comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

#Плейлисты
@app.route('/api/playlists', methods=['GET'])
def api_get_playlists():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    user_id = request.args.get('user_id', None, type=int)
    
    query = Playlist.query.filter_by(is_public=True)
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    playlists = query.order_by(Playlist.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    playlists_data = [{
        'id': playlist.id,
        'name': playlist.name,
        'description': playlist.description,
        'creator': playlist.creator.to_dict(),
        'is_public': playlist.is_public,
        'created_at': playlist.created_at.isoformat(),
        'tracks_count': len(playlist.tracks)
    } for playlist in playlists.items]
    
    return jsonify({
        'success': True,
        'playlists': playlists_data,
        'total': playlists.total,
        'pages': playlists.pages,
        'current_page': page
    }), 200

#Создание плейлиста 
@app.route('/api/playlists', methods=['POST'])
@jwt_required()
def api_create_playlist():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Нет данных'}), 400
    
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    is_public = data.get('is_public', True)
    
    if not name:
        return jsonify({'success': False, 'error': 'Название обязательно'}), 400
    
    try:
        playlist = Playlist(
            name=name,
            description=description,
            user_id=current_user_id,
            is_public=is_public
        )
        
        db.session.add(playlist)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Плейлист создан',
            'playlist': {
                'id': playlist.id,
                'name': playlist.name,
                'description': playlist.description,
                'is_public': playlist.is_public,
                'created_at': playlist.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

#Концерты
@app.route('/api/concerts', methods=['GET'])
def api_get_concerts():
    city = request.args.get('city', None)
    country = request.args.get('country', None)
    artist = request.args.get('artist', None)
    
    query = Concert.query
    
    if city:
        query = query.filter_by(city=city)
    if country:
        query = query.filter_by(country=country)
    if artist:
        query = query.filter(Concert.artist_name.ilike(f'%{artist}%'))
    
    query = query.filter(Concert.date >= datetime.now())
    
    concerts = query.order_by(Concert.date.asc()).all()
    
    concerts_data = [{
        'id': concert.id,
        'artist_name': concert.artist_name,
        'venue': concert.venue,
        'city': concert.city,
        'country': concert.country,
        'date': concert.date.isoformat(),
        'ticket_url': concert.ticket_url,
        'image_url': concert.image_url
    } for concert in concerts]
    
    return jsonify({
        'success': True,
        'concerts': concerts_data,
        'total': len(concerts_data)
    }), 200

#Курсы
@app.route('/api/courses', methods=['GET'])
def api_get_courses():
    instrument = request.args.get('instrument', None)
    level = request.args.get('level', None)
    
    query = Course.query
    
    if instrument:
        query = query.filter_by(instrument=instrument)
    if level:
        query = query.filter_by(level=level)
    
    courses = query.order_by(Course.created_at.desc()).all()
    
    courses_data = [{
        'id': course.id,
        'title': course.title,
        'description': course.description,
        'instructor': course.instructor,
        'instrument': course.instrument,
        'level': course.level,
        'price': course.price,
        'duration': course.duration,
        'created_at': course.created_at.isoformat()
    } for course in courses]
    
    return jsonify({
        'success': True,
        'courses': courses_data,
        'total': len(courses_data)
    }), 200

#Поиск
@app.route('/api/search', methods=['GET'])
def api_search():
    query = request.args.get('q', '').strip()
    
    if not query or len(query) < 2:
        return jsonify({'success': False, 'error': 'Запрос должен содержать минимум 2 символа'}), 400
    
    results = {
        'users': [],
        'posts': [],
        'playlists': []
    }
    
    users = User.query.filter(
        db.or_(
            User.username.ilike(f'%{query}%'),
            User.bio.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    results['users'] = [user.to_dict() for user in users]
    
    posts = Post.query.filter(
        db.or_(
            Post.title.ilike(f'%{query}%'),
            Post.content.ilike(f'%{query}%'),
            Post.track_name.ilike(f'%{query}%'),
            Post.artist_name.ilike(f'%{query}%')
        )
    ).limit(20).all()
    
    results['posts'] = [{
        'id': post.id,
        'title': post.title,
        'content': post.content[:100] + '...' if len(post.content) > 100 else post.content,
        'author': post.author.to_dict(),
        'post_type': post.post_type,
        'created_at': post.created_at.isoformat()
    } for post in posts]
    
    playlists = Playlist.query.filter(
        db.or_(
            Playlist.name.ilike(f'%{query}%'),
            Playlist.description.ilike(f'%{query}%')
        )
    ).filter_by(is_public=True).limit(10).all()
    
    results['playlists'] = [{
        'id': playlist.id,
        'name': playlist.name,
        'description': playlist.description,
        'creator': playlist.creator.to_dict(),
        'created_at': playlist.created_at.isoformat()
    } for playlist in playlists]
    
    return jsonify({
        'success': True,
        'query': query,
        'results': results
    }), 200

#Статы
@app.route('/api/stats', methods=['GET'])
def api_get_stats():
    total_users = User.query.count()
    total_posts = Post.query.count()
    total_playlists = Playlist.query.filter_by(is_public=True).count()
    total_comments = Comment.query.count()

    popular_posts = Post.query\
        .order_by(Post.likes_count.desc())\
        .limit(5).all()
    
    popular_posts_data = [{
        'id': post.id,
        'title': post.title,
        'author': post.author.username,
        'likes_count': post.likes_count,
        'comments_count': post.comments_count
    } for post in popular_posts]
    
    return jsonify({
        'success': True,
        'stats': {
            'total_users': total_users,
            'total_posts': total_posts,
            'total_playlists': total_playlists,
            'total_comments': total_comments
        },
        'popular_posts': popular_posts_data
    }), 200

# Лайки
@app.route('/api/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def api_toggle_like(post_id):
    current_user_id = get_jwt_identity()
    
    try:
        post = Post.query.get(post_id)
        if not post:
            return jsonify({'success': False, 'error': 'Пост не найден'}), 404
        from models import PostLike
        existing_like = PostLike.query.filter_by(
            post_id=post_id,
            user_id=current_user_id
        ).first()
        
        if existing_like:
            db.session.delete(existing_like)
            post.likes_count -= 1
            is_liked = False
        else:
            like = PostLike(post_id=post_id, user_id=current_user_id)
            db.session.add(like)
            post.likes_count += 1
            is_liked = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Лайк обновлен',
            'likes_count': post.likes_count,
            'is_liked': is_liked
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

#Обновление профиля
@app.route('/api/profile/update', methods=['PUT'])
@jwt_required()
def api_update_profile():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Нет данных'}), 400
    
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
    
    try:
        allowed_fields = ['bio', 'avatar_url', 'location', 'genres']
        
        for field in allowed_fields:
            if field in data:
                if field == 'genres' and isinstance(data[field], list):
                    import json
                    setattr(user, field, json.dumps(data[field]))
                else:
                    setattr(user, field, data[field].strip() if data[field] else None)
        
        user.updated_at = datetime.now()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Профиль обновлен',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

#Список друзей
@app.route('/api/friends', methods=['GET'])
@jwt_required()
def api_get_friends():
    current_user_id = get_jwt_identity()
    
    from models import Follow
    
    following = Follow.query.filter_by(follower_id=current_user_id).all()
    followers = Follow.query.filter_by(followed_id=current_user_id).all()
    
    following_ids = [f.followed_id for f in following]
    follower_ids = [f.follower_id for f in followers]
    friend_ids = set(following_ids) & set(follower_ids)
    friends = User.query.filter(User.id.in_(friend_ids)).all()
    
    return jsonify({
        'success': True,
        'friends': [friend.to_dict() for friend in friends],
        'stats': {
            'friends_count': len(friends),
            'following_count': len(following),
            'followers_count': len(followers)
        }
    }), 200

#Запрос в друзья 
@app.route('/api/friends/requests', methods=['GET'])
@jwt_required()
def api_get_friend_requests():
    current_user_id = get_jwt_identity()
    
    from models import Follow
    
    followers = Follow.query.filter_by(followed_id=current_user_id).all()
    following_ids = [f.followed_id for f in Follow.query.filter_by(follower_id=current_user_id).all()]
    
    requests = []
    for follower in followers:
        if follower.follower_id not in following_ids:
            user = User.query.get(follower.follower_id)
            if user:
                requests.append({
                    'user': user.to_dict(),
                    'requested_at': follower.created_at.isoformat()
                })
    
    return jsonify({
        'success': True,
        'requests': requests
    }), 200

#Подписка
@app.route('/api/friends/<int:user_id>/follow', methods=['POST'])
@jwt_required()
def api_follow_user(user_id):
    current_user_id = get_jwt_identity()
    
    if current_user_id == user_id:
        return jsonify({'success': False, 'error': 'Нельзя подписаться на себя'}), 400
    
    user_to_follow = User.query.get(user_id)
    if not user_to_follow:
        return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
    
    try:
        from models import Follow
        
        existing_follow = Follow.query.filter_by(
            follower_id=current_user_id,
            followed_id=user_id
        ).first()
        
        if existing_follow:
            db.session.delete(existing_follow)
            action = 'unfollowed'
        else:
            follow = Follow(follower_id=current_user_id, followed_id=user_id)
            db.session.add(follow)
            action = 'followed'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'action': action,
            'message': f'Вы {action} пользователя {user_to_follow.username}'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Смена пароля

@app.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def api_change_password():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Нет данных'}), 400
    
    current_password = data.get('current_password', '').strip()
    new_password = data.get('new_password', '').strip()
    
    if not current_password or not new_password:
        return jsonify({'success': False, 'error': 'Все поля обязательны'}), 400
    
    if len(new_password) < 6:
        return jsonify({'success': False, 'error': 'Новый пароль должен содержать минимум 6 символов'}), 400
    
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
    
    try:
        if user.change_password(current_password, new_password):
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'Пароль успешно изменен'
            }), 200
        else:
            return jsonify({'success': False, 'error': 'Неверный текущий пароль'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Удаление аккаунта

@app.route('/api/auth/delete-account', methods=['DELETE'])
@jwt_required()
def api_delete_account():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'error': 'Нет данных'}), 400
    
    password = data.get('password', '').strip()
    
    if not password:
        return jsonify({'success': False, 'error': 'Введите пароль для подтверждения'}), 400
    
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'success': False, 'error': 'Пользователь не найден'}), 404
    
    if not user.check_password(password):
        return jsonify({'success': False, 'error': 'Неверный пароль'}), 400
    
    try:
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Аккаунт успешно удален'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)