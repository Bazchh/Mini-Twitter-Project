from core.repositories.post_repository import PostRepository
from core.shared.customAPIException import CustomAPIException
from core.models.post_model import Post
from django.core.exceptions import ObjectDoesNotExist

class PostService:
    @staticmethod
    def create_post(user, title, text, image=None):
        try:
            return PostRepository.create_post(user=user, title=title, text=text, image=image)
        except Exception as e:
            raise CustomAPIException(detail="Failed to create post: " + str(e), status_code=400)

    @staticmethod
    def update_post(post_id, user_id, title=None, text=None, image=None):
        try:
            post = Post.objects.get(id=post_id)

            if post.user_id != user_id:
                raise CustomAPIException(detail="You do not have permission to edit this post.", status_code=403)
            
            if title is not None:
                post.title = title
            if text is not None:
                post.text = text
            if image is not None:
                post.image = image
            
            post.save()
            return post
            
        except ObjectDoesNotExist:
            raise CustomAPIException(detail="Post not found.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Error updating post: " + str(e), status_code=400)

        
    @staticmethod
    def retrieve_post(post_id):
        try:
            return PostRepository.get_post_by_id(post_id) 
        except CustomAPIException as e:
            raise e
        except Exception as e:
            raise CustomAPIException(detail="Failed to retrieve post: " + str(e), status_code=404)

    @staticmethod
    def delete_post(user_id, post_id):
        try:
            PostRepository.delete_post(user_id=user_id, post_id=post_id)
        except CustomAPIException as e:
            raise e  
        except Exception as e:
            raise CustomAPIException(detail="Failed to delete post: " + str(e), status_code=400)

    @staticmethod
    def like_post(post_id):
        try:
            return PostRepository.like_post(post_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to like post: " + str(e), status_code=400)

    @staticmethod
    def get_post_likes(post_id):
        try:
            return PostRepository.get_likes(post_id)
        except Exception as e:
            raise CustomAPIException(detail="Failed to retrieve likes: " + str(e), status_code=400)