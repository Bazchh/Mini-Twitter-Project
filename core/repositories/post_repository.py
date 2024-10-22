from core.models.post_model import Post
from core.shared.customAPIException import CustomAPIException
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import APIException

class PostRepository:
    
    @staticmethod
    def create_post(user, title, text, image=None):
        if not title or not text:
            raise APIException(detail="Title and text are required.", status_code=400)

        try:
            post = Post.objects.create(user=user, title=title, text=text, image=image)
            return post
        except Exception as e:
            raise APIException(detail="Failed to create post: " + str(e), status_code=400)

    @staticmethod
    def update_post(post_id, user_id, title=None, text=None, image=None):
        try:
            post = Post.objects.get(id=post_id)

            if post.user_id != user_id:
                raise CustomAPIException(detail="You do not have permission to edit this post.", status_code=403)
            
            if title:
                post.title = title
            if text:
                post.text = text
            if image:
                post.image = image
            
            post.save()
            return post
        
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Post not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating post: " + str(e), status_code=400)

    @staticmethod
    def delete_post(post_id, user_id):
        try:
            post = Post.objects.get(id=post_id)

            if post.user_id != user_id:
                raise CustomAPIException(detail="You do not have permission to delete this post.", status_code=403)

            post.delete()
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Post not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error deleting post: " + str(e), status_code=400)
        
    @staticmethod
    def get_likes(post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post.likes
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Post not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving likes: " + str(e), status_code=400)

    @staticmethod
    def like_post(post_id):
        try:
            post = Post.objects.get(id=post_id)
            post.add_like()
            return post.likes  
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Post not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error liking post: " + str(e), status_code=400)
        
    @staticmethod
    def get_post_by_id(post_id):
        try:
            return Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Post not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving post: " + str(e), status_code=400)
