from rest_framework import serializers

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

        read_only_fields = ('game_id', 'field', 'completed',)
   

    def create(self, validated_data):

            instance = super().create(validated_data)
            # заполняем поле field
            instance.initialize_game()
            return instance