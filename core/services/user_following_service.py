from core.models.user_following_model import UserFollowing
from core.shared.customAPIException import CustomAPIException
from core.models.user_model import User
from uuid import UUID

class UserFollowingService:
    @staticmethod
    def list_followings_for_user(user_id):
        try:
            # Obtém todos os usuários que o usuário logado está seguindo (seguido pelo usuário logado)
            user_followings = UserFollowing.objects.filter(following_id=user_id)
            return user_followings
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving user followings: " + str(e), status_code=400)

    @staticmethod
    def list_followers_for_user(user_id):
        """Lista todos os seguidores do usuário especificado."""
        try:
            return UserFollowing.objects.filter(followed=user_id)
        except Exception as e:
            raise CustomAPIException(detail="Error retrieving user followers: " + str(e), status_code=500)

    @staticmethod
    def create_user_following(validated_data):
        """Cria um novo relacionamento de seguimento."""
        try:
            user_following = UserFollowing.objects.create(**validated_data)
            return user_following
        except Exception as e:
            raise CustomAPIException(detail="Error creating user following: " + str(e), status_code=400)

    @staticmethod
    def update_following_relationship(requester_id, requested_id):
        """Atualiza o relacionamento de seguimento entre dois usuários."""
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
                # Cria um novo relacionamento de seguimento
                UserFollowing.objects.create(following=requester, followed=requested)
            else:
                # Se já existe, você pode optar por atualizar se necessário
                pass  # Remova ou adicione a lógica necessária aqui

        except Exception as e:
            raise CustomAPIException(detail="Error updating following relationship: " + str(e), status_code=400)

        
        
    @staticmethod
    def remove_follower(user_id, follower_id):
        """
        Remove um seguidor. 
        O usuário (user_id) deve ter o follower_id como seguidor para que a remoção seja bem-sucedida.
        """
        try:
            # Converte os IDs para UUID, caso ainda não sejam
            user_uuid = UUID(user_id) if isinstance(user_id, str) else user_id
            follower_uuid = UUID(follower_id) if isinstance(follower_id, str) else follower_id

            # Busca a relação de seguimento
            following_relationship = UserFollowing.objects.get(following=follower_uuid, followed=user_uuid)
            
            # Remove a relação
            following_relationship.delete()
            return {"detail": "Seguidor removido com sucesso."}
        
        except UserFollowing.DoesNotExist:
            raise CustomAPIException(detail="Relação de seguimento não encontrada.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Erro ao remover seguidor: " + str(e), status_code=500)
        
    @staticmethod
    def list_non_friends(user_id):
        # Obtenha todos os usuários, exceto o próprio usuário
        all_users = User.objects.exclude(id=user_id)  # Exclui o próprio usuário logado

        # Obtenha os IDs dos usuários que o usuário logado está seguindo
        following_ids = UserFollowing.objects.filter(following=user_id).values_list('followed_id', flat=True)

        # Obtenha os IDs dos usuários que seguem o usuário logado
        followers_ids = UserFollowing.objects.filter(followed=user_id).values_list('following_id', flat=True)

        # Combine todos os IDs relacionados
        related_ids = set(following_ids).union(set(followers_ids))

        # Filtre os usuários que não estão relacionados (não seguem ou não são seguidos)
        non_friends = all_users.exclude(id__in=related_ids)

        return non_friends
    
    @staticmethod
    def unfollow_user(user_id, followed_id):
        """
        Remove a relação de seguimento, ou seja, o usuário logado deixa de seguir outro usuário.
        """
        try:
            # Tenta encontrar a relação de seguimento
            following_relationship = UserFollowing.objects.get(following=user_id, followed=followed_id)
            following_relationship.delete()
            return {"detail": "Unfollowed successfully."}
        except UserFollowing.DoesNotExist:
            raise CustomAPIException(detail="Relação de seguimento não encontrada.", status_code=404)
        except Exception as e:
            raise CustomAPIException(detail="Erro ao deixar de seguir: " + str(e), status_code=500)
    @staticmethod    
    def is_following(requester_id, requested_id):
        return UserFollowing.objects.filter(following=requester_id, followed=requested_id).exists()