from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime
from eralchemy2 import render_er

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user", cascade="all, delete")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="user", cascade="all, delete")

    followers: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.user_id]",
        back_populates="user",
        cascade="all, delete"
    )

    following: Mapped[list["Follower"]] = relationship(
        "Follower",
        foreign_keys="[Follower.follower_id]",
        back_populates="follower",
        cascade="all, delete"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    image_url: Mapped[str] = mapped_column(String(250), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship("Comment", back_populates="post", cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "caption": self.caption,
            "created_at": self.created_at.isoformat(),
        }

class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=datetime.datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="comments")
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
        }

class Follower(db.Model):
    __tablename__ = 'follower'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)      # being followed
    follower_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)  # the one who follows

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id], back_populates="followers")
    follower: Mapped["User"] = relationship("User", foreign_keys=[follower_id], back_populates="following")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "follower_id": self.follower_id,
        }



try:
    render_er(db.Model, 'diagram.png')
    print("diagram.png generated successfully!")
except Exception as e:
    print("Error generating diagram:", e)