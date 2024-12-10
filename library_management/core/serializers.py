from rest_framework import serializers # type: ignore
from .models import User, Book, Membership, Transaction, OverdueReport


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class OverdueReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverdueReport
        fields = '__all__'
