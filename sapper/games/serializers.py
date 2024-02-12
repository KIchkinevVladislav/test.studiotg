from rest_framework import serializers

from .models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

        read_only_fields = ('completed', 'field', 'game_id')

    def create(self, validated_data):
            # Проверка, чтобы количество мин не превышало (width * height - 1)
            width = validated_data.get('width', 0)
            height = validated_data.get('height', 0)
            mines_count = validated_data.get('mines_count', 0)

            if mines_count > (width * height - 1):
                raise serializers.ValidationError("Количество мин должно быть меньше или равно (width * height - 1)")

            instance = super().create(validated_data)
            instance.initialize_game()
            return instance