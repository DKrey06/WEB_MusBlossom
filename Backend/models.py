from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import json

db = SQLAlchemy()

post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    website = db.Column(db.String(200), nullable=True)
    genres = db.Column(db.String(1000), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    hashed_password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    last_login = db.Column(db.DateTime, nullable=True)
    

    posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    playlists = db.relationship('Playlist', backref='creator', lazy=True, cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='author', lazy=True, cascade='all, delete-orphan')
    post_likes = db.relationship('PostLike', backref='user', lazy=True, cascade='all, delete-orphan')
    

    followers = db.relationship('Follow',
                               foreign_keys='Follow.followed_id',
                               backref='followed',
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    following = db.relationship('Follow',
                               foreign_keys='Follow.follower_id',
                               backref='follower',
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    

    course_enrollments = db.relationship('CourseEnrollment', backref='user', lazy=True, cascade='all, delete-orphan')
    

    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)
    

    notifications = db.relationship('Notification', backref='user', lazy=True, cascade='all, delete-orphan')
    
    saved_posts = db.relationship('SavedPost', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def change_password(self, current_password, new_password):
        if not self.check_password(current_password):
            return False
        self.set_password(new_password)
        return True
    
    def to_dict(self):
        genres_list = []
        if self.genres:
            try:
                genres_list = json.loads(self.genres)
            except:
                genres_list = []
        
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'location': self.location,
            'website': self.website,
            'genres': genres_list,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'stats': {
                'posts_count': len(self.posts),
                'followers_count': self.followers.count(),
                'following_count': self.following.count(),
                'playlists_count': len(self.playlists),
                'reviews_count': len(self.reviews),
            }
        }
    
    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).first() is not None
    
    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None
    
    def follow(self, user):
        if not self.is_following(user) and self.id != user.id:
            follow = Follow(follower_id=self.id, followed_id=user.id)
            db.session.add(follow)
            return True
        return False
    
    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            return True
        return False

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_type = db.Column(db.String(50), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    track_id = db.Column(db.String(100), nullable=True) 
    artist_name = db.Column(db.String(100), nullable=True)
    track_name = db.Column(db.String(200), nullable=True)
    album_art_url = db.Column(db.String(500), nullable=True)
    media_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('PostLike', backref='post', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy=True))
    saved_by = db.relationship('SavedPost', backref='post', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'post_type': self.post_type,
            'author': self.author.to_dict(),
            'track_id': self.track_id,
            'track_name': self.track_name,
            'artist_name': self.artist_name,
            'album_art_url': self.album_art_url,
            'media_url': self.media_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'views_count': self.views_count,
            'tags': [tag.name for tag in self.tags],
            'comments': [comment.to_dict() for comment in self.comments[:10]],
        }

class PostLike(db.Model):
    __tablename__ = 'post_likes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),
    )

class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    parent_comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'author': self.author.to_dict(),
            'post_id': self.post_id,
            'parent_comment_id': self.parent_comment_id,
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat(),
            'replies_count': len(self.replies),
        }

class Playlist(db.Model):
    __tablename__ = 'playlists'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    cover_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    plays_count = db.Column(db.Integer, default=0)
    
    tracks = db.relationship('PlaylistTrack', backref='playlist', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'creator': self.creator.to_dict(),
            'is_public': self.is_public,
            'cover_url': self.cover_url,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'plays_count': self.plays_count,
            'tracks_count': len(self.tracks),
            'tracks': [track.to_dict() for track in self.tracks[:20]],
        }

class PlaylistTrack(db.Model):
    __tablename__ = 'playlist_tracks'
    
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    track_id = db.Column(db.String(100), nullable=False)
    track_name = db.Column(db.String(200), nullable=False)
    artist_name = db.Column(db.String(100), nullable=False)
    album_name = db.Column(db.String(200), nullable=True)
    album_art_url = db.Column(db.String(500), nullable=True)
    duration_ms = db.Column(db.Integer, nullable=True)
    added_at = db.Column(db.DateTime, default=datetime.now)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    added_by_user = db.relationship('User', foreign_keys=[added_by])
    
    def to_dict(self):
        return {
            'id': self.id,
            'track_id': self.track_id,
            'track_name': self.track_name,
            'artist_name': self.artist_name,
            'album_name': self.album_name,
            'album_art_url': self.album_art_url,
            'duration_ms': self.duration_ms,
            'added_at': self.added_at.isoformat(),
            'added_by': self.added_by_user.to_dict() if self.added_by_user else None,
        }

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    track_id = db.Column(db.String(100), nullable=False)
    track_name = db.Column(db.String(200), nullable=False)
    artist_name = db.Column(db.String(100), nullable=False)
    album_art_url = db.Column(db.String(500), nullable=True)
    likes_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'content': self.content,
            'author': self.author.to_dict(),
            'track_id': self.track_id,
            'track_name': self.track_name,
            'artist_name': self.artist_name,
            'album_art_url': self.album_art_url,
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat(),
        }

class Concert(db.Model):
    __tablename__ = 'concerts'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(100), nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    ticket_url = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    price_range = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'artist_name': self.artist_name,
            'venue': self.venue,
            'city': self.city,
            'country': self.country,
            'date': self.date.isoformat(),
            'ticket_url': self.ticket_url,
            'image_url': self.image_url,
            'description': self.description,
            'price_range': self.price_range,
            'created_at': self.created_at.isoformat(),
        }

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    tag_type = db.Column(db.String(50), nullable=False)
    popularity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tag_type': self.tag_type,
            'popularity': self.popularity,
        }

class Follow(db.Model):
    __tablename__ = 'follows'
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    __table_args__ = (
        db.UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'follower': self.follower.to_dict(),
            'followed': self.followed.to_dict(),
            'created_at': self.created_at.isoformat(),
        }

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    instrument = db.Column(db.String(50), nullable=False) 
    level = db.Column(db.String(20), nullable=False) 
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    video_url = db.Column(db.String(500), nullable=True)
    thumbnail_url = db.Column(db.String(500), nullable=True)
    students_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'instructor': self.instructor,
            'instrument': self.instrument,
            'level': self.level,
            'price': self.price,
            'duration': self.duration,
            'video_url': self.video_url,
            'thumbnail_url': self.thumbnail_url,
            'students_count': self.students_count,
            'rating': self.rating,
            'created_at': self.created_at.isoformat(),
        }

class CourseEnrollment(db.Model):
    __tablename__ = 'course_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.now)
    completed_at = db.Column(db.DateTime, nullable=True)
    progress = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float, nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'course_id', name='unique_enrollment'),
    )
    
    course = db.relationship('Course', backref='enrollments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'course': self.course.to_dict(),
            'enrolled_at': self.enrolled_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'progress': self.progress,
            'rating': self.rating,
        }

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False)  
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    reference_id = db.Column(db.Integer, nullable=True)  
    reference_type = db.Column(db.String(50), nullable=True) 
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'reference_id': self.reference_id,
            'reference_type': self.reference_type,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
        }

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'sender': self.sender.to_dict(),
            'receiver': self.receiver.to_dict(),
            'content': self.content,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
        }

class SavedPost(db.Model):
    __tablename__ = 'saved_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.now)
    folder = db.Column(db.String(100), nullable=True) 
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_saved_post'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post': self.post.to_dict(),
            'saved_at': self.saved_at.isoformat(),
            'folder': self.folder,
        }


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
        if Tag.query.count() == 0:
            default_tags = [
                ('Rock', 'genre'),
                ('Pop', 'genre'),
                ('Hip-Hop', 'genre'),
                ('Jazz', 'genre'),
                ('Classical', 'genre'),
                ('Electronic', 'genre'),
                ('Indie', 'genre'),
                ('Metal', 'genre'),
                ('Folk', 'genre'),
                ('R&B', 'genre'),
                ('Soul', 'genre'),
                ('Reggae', 'genre'),
                ('Country', 'genre'),
                ('Blues', 'genre'),
                ('Funk', 'genre'),
                ('Happy', 'mood'),
                ('Sad', 'mood'),
                ('Energetic', 'mood'),
                ('Relaxing', 'mood'),
                ('Romantic', 'mood'),
                ('Guitar', 'instrument'),
                ('Piano', 'instrument'),
                ('Drums', 'instrument'),
                ('Bass', 'instrument'),
                ('Violin', 'instrument'),
                ('Saxophone', 'instrument'),
                ('80s', 'era'),
                ('90s', 'era'),
                ('2000s', 'era'),
                ('2020s', 'era'),
            ]
            
            for name, tag_type in default_tags:
                tag = Tag(name=name, tag_type=tag_type)
                db.session.add(tag)

        if User.query.filter_by(username='admin').count() == 0:
            admin = User(
                username='admin',
                email='admin@musblossom.com',
                bio='Основатель MusBlossom',
                is_verified=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
        
        db.session.commit()