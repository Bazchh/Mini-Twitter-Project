"""
This module defines the PostService for handling post-related business logic.
"""
from core.repositories.post_repository import PostRepository
from core.shared.custom_api_exception import CustomAPIException
from core.models.post_model import Post
from django.core.exceptions import ObjectDoesNotExist


class PostService:
    """
    Service class for managing Post objects and their associated business logic.
    """

    @staticmethod
    def create_post(user, title, text, image=None):
        """
        Creates a new post through the PostRepository.
        Raises CustomAPIException if post creation fails.
        """
        try:
            # S.O.L.I.D. - S (Responsabilidade Única): O serviço delega a persistência
            # para o repositório, focando apenas na orquestração da lógica de negócio.
            # S.O.L.I.D. - D (Inversão de Dependência): O serviço depende de uma abstração (PostRepository)
            # e não diretamente do ORM ou detalhes de banco de dados.
            return PostRepository.create_post(user=user, title=title, text=text, image=image)
        except CustomAPIException as exc:
            # S.O.L.I.D. - O (Aberto/Fechado) & D (Inversão de Dependência): O serviço pode propagar
            # CustomAPIException de forma genérica, sem precisar saber os detalhes específicos
            # da validação que o repositório fez (e.g., se faltou título).
            raise exc
        except Exception as e:
            # Tratamento de exceção robusto com 'from e' para preservar o traceback.
            raise CustomAPIException(detail=f"Failed to create post: {e}", status_code=400) from e

    @staticmethod
    def update_post(post_id, user_id, title=None, text=None, image=None):
        """
        Updates an existing post.
        Requires the user to be the owner of the post to update.
        Raises CustomAPIException if post not found, permission denied, or update fails.
        """
        try:
            # S.O.L.I.D. - S (Responsabilidade Única): O serviço lida com a regra de negócio
            # da permissão de atualização, que é uma lógica de negócio e não de persistência.
            post = Post.objects.get(id=post_id)

            if post.user_id != user_id:
                raise CustomAPIException(detail="You do not have permission to edit this post.", status_code=403)

            # Atualiza os campos apenas se um novo valor for fornecido
            if title is not None:
                post.title = title
            if text is not None:
                post.text = text
            if image is not None:
                post.image = image

            post.save()
            return post

        except ObjectDoesNotExist as exc:
            # S.O.L.I.D. - D (Inversão de Dependência): O serviço lida com a exceção de "não encontrado"
            # do ORM e a converte para uma CustomAPIException, mantendo a camada de serviço
            # dependente de uma abstração de erro (CustomAPIException).
            raise CustomAPIException(detail="Post not found.", status_code=404) from exc
        except CustomAPIException as exc:
            # Propaga exceções de permissão ou outras exceções CustomAPIException
            raise exc
        except Exception as e:
            raise CustomAPIException(detail=f"Error updating post: {e}", status_code=400) from e

    @staticmethod
    def retrieve_post(post_id):
        """
        Retrieves a single post by its ID using the PostRepository.
        Raises CustomAPIException if the post is not found or retrieval fails.
        """
        try:
            # S.O.L.I.D. - S (Responsabilidade Única) & D (Inversão de Dependência):
            # Delega a recuperação do dado ao repositório.
            return PostRepository.get_post_by_id(post_id)
        except CustomAPIException as exc:
            raise exc
        except Exception as e:
            raise CustomAPIException(detail=f"Failed to retrieve post: {e}", status_code=404) from e

    @staticmethod
    def delete_post(user_id, post_id):
        """
        Deletes a post using the PostRepository.
        Requires the user to be the owner of the post to delete.
        Raises CustomAPIException if deletion fails.
        """
        try:
            # S.O.L.I.D. - S (Responsabilidade Única) & D (Inversão de Dependência):
            # Delega a exclusão ao repositório.
            PostRepository.delete_post(user_id=user_id, post_id=post_id)
            return {"detail": "Post deleted successfully."}
        except CustomAPIException as exc:
            raise exc
        except Exception as e:
            raise CustomAPIException(detail=f"Failed to delete post: {e}", status_code=400) from e

    @staticmethod
    def like_post(post_id, user_id):
        """
        Handles the liking of a post by a user using the PostRepository.
        Raises CustomAPIException if liking fails (e.g., post not found, already liked).
        """
        try:
            # S.O.L.I.D. - S (Responsabilidade Única) & D (Inversão de Dependência):
            # Delega a lógica de "curtir" ao repositório (ou modelo, se add_like estiver lá).
            return PostRepository.like_post(post_id=post_id, user_id=user_id)
        except CustomAPIException as exc:
            raise exc
        except Exception as e:
            raise CustomAPIException(detail=f"Failed to like post: {e}", status_code=400) from e

    @staticmethod
    def get_post_likes(post_id):
        """
        Retrieves the number of likes for a specific post using the PostRepository.
        Raises CustomAPIException if retrieval fails.
        """
        try:
            # S.O.L.I.D. - S (Responsabilidade Única) & D (Inversão de Dependência):
            # Delega a recuperação do contador de curtidas ao repositório.
            return PostRepository.get_likes(post_id)
        except CustomAPIException as exc:
            raise exc
        except Exception as e:
            raise CustomAPIException(detail=f"Failed to retrieve likes: {e}", status_code=400) from e