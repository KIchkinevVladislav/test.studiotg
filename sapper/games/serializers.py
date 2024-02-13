from rest_framework import serializers

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = 'game_id', 'width', 'height', 'mines_count', 'field', 'completed'

        read_only_fields = ('game_id', 'field', 'completed', 'mine_field')
   
    def create(self, validated_data):
            instance = super().create(validated_data)
            # заполняем полец field и mine_field
            instance.initialize_game()
            return instance