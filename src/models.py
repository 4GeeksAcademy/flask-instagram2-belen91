from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

#ORM: OBJECT-RELATIONAL MAPPER

class User(db.Model):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    
    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")
    likes: Mapped[list["Like"]] = relationship(back_populates="users", cascade="all, delete-orphan")

# followers = usuarios que ME siguen
    followers: Mapped[list["Follow"]] = relationship(back_populates="followed", foreign_keys="Follow.followed_id", cascade="all, delete-orphan")

# following = usuarios a los que YO sigo
    following: Mapped[list["Follow"]] = relationship(back_populates="follower", foreign_keys="Follow.follower_id", cascade="all, delete-orphan")
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    media_type: Mapped[str] = mapped_column(String(120), nullable=False)
    caption: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(String(120), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    author: Mapped["User"] = relationship(back_populates="posts")
    likes: Mapped[list["Like"]] = relationship(back_populates="post", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "media_type": self.media_type,
            "caption": self.caption,
            "url": self.url,
            "user_id":self.user_id
        }

class Follow(db.Model):

    __tablename__ = "follow"

    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    followed_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    date: Mapped [str] = mapped_column(String(10), nullable=False)

    follower: Mapped["User"] = relationship(back_populates="following", foreign_keys=[follower_id])
    followed: Mapped["User"] = relationship(back_populates="followers", foreign_keys=[followed_id])

    __table_args__ = (UniqueConstraint("follower_id", "followed_id", name="uq_follow_pair"),)

    def serialize(self):
        return {
            "follower_id": self.follower_id,
            "followed_id": self.followed_id,
            "date": self.date,
        }
    
class Like(db.Model):
    
    __tablename__ = "like"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)
    date: Mapped[str] = mapped_column(String(10), nullable=False)

    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")
    
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="uq_like_user_post"),)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "post_id": self.post_id,
            "date": self.date,
        }