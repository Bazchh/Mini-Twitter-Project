"""
This module defines the UserFollowingService for handling business logic related to user followings.
"""
from uuid import UUID
from django.core.exceptions import ObjectDoesNotExist
from core.models.user_following_model import UserFollowing
from core.models.user_model import User
from core.shared.custom_api_exception import CustomAPIException


class UserFollowingService:
    """
    Service class for managing user following relationships (who follows whom).
    """

    @staticmethod
    def list_followings_for_user(user_id):
        """
        Retrieves all users that a specified user is following.
        Raises CustomAPIException on error.
        """
        try:
            # Obtém todos os usuários que o user_id (quem segue) está seguindo (o seguido)
            user_followings = UserFollowing.objects.filter(following_id=user_id)
            return user_followings
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error retrieving user followings: {e}", status_code=400
            ) from e

    @staticmethod
    def list_followers_for_user(user_id):
        """
        Retrieves all followers of a specified user.
        Raises CustomAPIException on error.
        """
        try:
            # Obtém todos os seguidores do user_id (quem é seguido)
            # Ou seja, busca relacionamentos onde user_id é o 'followed'
            return UserFollowing.objects.filter(followed_id=user_id)
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error retrieving user followers: {e}", status_code=500
            ) from e

    @staticmethod
    def create_user_following(validated_data):
        """
        Creates a new following relationship.
        Raises CustomAPIException on creation error.
        """
        try:
            user_following = UserFollowing.objects.create(**validated_data)
            return user_following
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error creating user following: {e}", status_code=400
            ) from e

    @staticmethod
    def update_following_relationship(requester_id, requested_id):
        """
        Ensures a following relationship exists between two users.
        If the relationship doesn't exist, it creates one.
        Raises CustomAPIException on error.
        """
        try:
            # Recupera as instâncias de usuário com base nos IDs
            requester = User.objects.get(id=requester_id)
            requested = User.objects.get(id=requested_id)

            # Verifica se o relacionamento já existe
            existing_relationship = UserFollowing.objects.filter(
                following=requester,
                followed=requested
            ).first()

            if not existing_relationship:
                # Cria um novo relacionamento de seguimento se não existir
                UserFollowing.objects.create(following=requester, followed=requested)
                return {"detail": "Following relationship created."}
            # else:
            # Se já existe, não faz nada ou retorna uma mensagem de que já existe
            return {"detail": "Following relationship already exists."}

        except ObjectDoesNotExist as exc:
            # Captura se requester ou requested não forem encontrados
            raise CustomAPIException(detail="User not found.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error updating following relationship: {e}", status_code=400
            ) from e

    @staticmethod
    def remove_follower(user_id, follower_id):
        """
        Removes a follower from a user's follower list.
        The user (user_id) must be the one being followed (followed_id) by the follower (follower_id).
        Raises CustomAPIException if the relationship is not found or on error.
        """
        try:
            # Garante que os IDs são UUIDs antes de usar na query
            # Não é estritamente necessário converter se o ORM já lida com isso,
            # mas garante consistência se os IDs vierem de fontes variadas.
            # No entanto, User.objects.get(id=...) já lida com string UUID.
            # user_uuid = UUID(str(user_id)) if not isinstance(user_id, UUID) else user_id
            # follower_uuid = UUID(str(follower_id)) if not isinstance(follower_id, UUID) else follower_id

            # Busca a relação de seguimento onde 'follower_id' segue 'user_id'
            following_relationship = UserFollowing.objects.get(
                following_id=follower_id, # Quem está seguindo (o seguidor)
                followed_id=user_id # Quem é seguido (o usuário atual)
            )

            # Remove a relação
            following_relationship.delete()
            return {"detail": "Seguidor removido com sucesso."}

        except UserFollowing.DoesNotExist as exc:
            raise CustomAPIException(detail="Relação de seguimento não encontrada.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Erro ao remover seguidor: {e}", status_code=500
            ) from e

    @staticmethod
    def list_non_friends(user_id):
        """
        Lists users who are neither followed by, nor followers of, the specified user.
        """
        try:
            # Obtém todos os usuários, exceto o próprio usuário
            all_users = User.objects.exclude(id=user_id)

            # Obtém os IDs dos usuários que o usuário logado está seguindo
            following_ids = UserFollowing.objects.filter(following_id=user_id).values_list('followed_id', flat=True)

            # Obtém os IDs dos usuários que seguem o usuário logado
            followers_ids = UserFollowing.objects.filter(followed_id=user_id).values_list('following_id', flat=True)

            # Combine todos os IDs relacionados (seguindo e seguidores)
            related_ids = set(following_ids).union(set(followers_ids))

            # Filtre os usuários que não estão relacionados (não seguem ou não são seguidos)
            non_friends = all_users.exclude(id__in=related_ids)

            return non_friends
        except Exception as e:
            raise CustomAPIException(
                detail=f"Error listing non-friends: {e}", status_code=500
            ) from e

    @staticmethod
    def unfollow_user(user_id, followed_id):
        """
        Removes a following relationship, meaning the user (user_id) stops following another user (followed_id).
        Raises CustomAPIException if the relationship is not found or on error.
        """
        try:
            # Tenta encontrar a relação de seguimento
            following_relationship = UserFollowing.objects.get(
                following_id=user_id,
                followed_id=followed_id
            )
            following_relationship.delete()
            return {"detail": "Unfollowed successfully."}
        except UserFollowing.DoesNotExist as exc:
            raise CustomAPIException(detail="Relação de seguimento não encontrada.", status_code=404) from exc
        except Exception as e:
            raise CustomAPIException(
                detail=f"Erro ao deixar de seguir: {e}", status_code=500
            ) from e

    @staticmethod
    def is_following(requester_id, requested_id):
        """
        Checks if a requester is following a requested user.
        Returns True if following, False otherwise.
        """
        # Não precisa de try-except aqui, pois .exists() não levanta DoesNotExist
        return UserFollowing.objects.filter(following_id=requester_id, followed_id=requested_id).exists()
