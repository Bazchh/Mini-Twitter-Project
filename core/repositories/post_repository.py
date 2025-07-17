"""
This module defines the PostRepository for handling post-related data operations.
"""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException
from core.models.post_model import Post
from core.models.user_model import User
from core.shared.custom_api_exception import CustomAPIException


class PostRepository:
    """
    Repository class for managing Post objects and their interactions.
    """

    @staticmethod
    def create_post(user, title, text, image=None):
        """
        Creates a new post.
        Raises APIException if title or text are missing.
        """
        if not title or not text:
            # A APIException do DRF geralmente não aceita 'status_code' no construtor
            raise APIException(detail="Title and text are required.")

        try:
            post = Post.objects.create(user=user, title=title, text=text, image=image)
            return post
        except Exception as e:
            # Para CustomAPIException, 'status_code' é esperado
            raise CustomAPIException(detail=f"Failed to create post: {e}", status_code=500) from e

    @staticmethod
    def update_post(post_id, user_id, title=None, text=None, image=None):
        """
        Updates an existing post.
        Requires user permission to edit.
        """
        try:
            post = Post.objects.get(id=post_id)

            if post.user_id != user_id:
                raise CustomAPIException(
                    detail="You do not have permission to edit this post.", status_code=403
                )

            if title:
                post.title = title
            if text:
                post.text = text
            if image:
                post.image = image

            post.save()
            return post

        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="Post not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(detail=f"Error updating post: {e}", status_code=400) from e

    @staticmethod
    def delete_post(post_id, user_id):
        """
        Deletes a post.
        Requires user permission to delete.
        """
        try:
            post = Post.objects.get(id=post_id)

            if post.user_id != user_id:
                raise CustomAPIException(
                    detail="You do not have permission to delete this post.", status_code=403
                )

            post.delete()
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="Post not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(detail=f"Error deleting post: {e}", status_code=400) from e

    @staticmethod
    def get_likes(post_id):
        """
        Retrieves the number of likes for a specific post.
        """
        try:
            post = Post.objects.get(id=post_id)
            return post.likes
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="Post not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(detail=f"Error retrieving likes: {e}", status_code=400) from e

    @staticmethod
    def like_post(post_id, user_id):
        """
        Adds a like from a user to a post.
        Handles cases where the post or user is not found, or post already liked.
        """
        try:
            post = Post.objects.get(id=post_id)
            user = User.objects.get(id=user_id)

            post.add_like(user)
            return post.likes
        except Post.DoesNotExist as exc: # Específico para Post
            raise CustomAPIException(detail="Post not found.", status_code=404) from exc
        except User.DoesNotExist as exc: # Específico para User
            raise CustomAPIException(detail="User not found.", status_code=404) from exc
        except ValueError as exc: # Erro lançado se o usuário já curtiu
            raise CustomAPIException(detail=str(exc), status_code=400) from exc
        except Exception as e:
            raise CustomAPIException(detail=f"Error liking post: {e}", status_code=400) from e

    @staticmethod
    def get_post_by_id(post_id):
        """
        Retrieves a post by its ID.
        """
        try:
            return Post.objects.get(id=post_id)
        except ObjectDoesNotExist as exc:
            raise CustomAPIException(detail="Post not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(detail=f"Error retrieving post: {e}", status_code=400) from e
