from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()

class RouteRequestSerializer(serializers.Serializer):
    # distance_matrix = serializers.ListField(
    #     child=serializers.ListField(
    #         child=serializers.FloatField()
    #     )
    # )
    locations = LocationSerializer(many=True) 
    start = serializers.IntegerField(default=0)
    algorithm = serializers.ChoiceField(
    choices=["greedy", "aco"],
    default="greedy",
)


class RouteResponseSerializer(serializers.Serializer):
    route = serializers.ListField(
        child=serializers.IntegerField()
    )
    total_distance_km = serializers.FloatField()
    duration_minutes = serializers.FloatField()
    geometry = serializers.ListField(
        child=serializers.ListField(
            child=serializers.FloatField()
        )
    )
    optimization_time_ms = serializers.FloatField()
