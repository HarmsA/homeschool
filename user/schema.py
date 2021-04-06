from django.contrib.auth import get_user_model
from graphql import GraphQLError

from graphene_django import DjangoObjectType, DjangoListField
from graphene import Mutation, Field, String, ObjectType, List, Int


class UserType(DjangoObjectType):
	class Meta:
		model = get_user_model()


class Query(ObjectType):
	user = Field(UserType, id=Int(required=True))
	users = List(UserType)
	me = Field(UserType)

	def resolve_user(self, info, id):
		return get_user_model().objects.get(id=id)

	def resolve_users(self, info):
		return get_user_model().objects.all()

	def resolve_me(self, info):
		user = info.context.user
		if user.is_anonymous:
			raise GraphQLError("Not logged in!")
		return user


class CreateUser(Mutation):
	user = Field(UserType)

	class Arguments:
		username = String(required=True)
		email = String(required=True)
		password = String(required=True)
		# firstName = String()
		# lastName = String()

	def mutate(self, info, username, email, password):
		user = get_user_model()(
			username=username,
			email=email,
			# firstName=firstName,
			# lastName=lastName
		)

		user.set_password(password)
		user.save()
		return CreateUser(user=user)


class UpdateUser(Mutation):
	user = Field(UserType)

	class Arguments:
		username = String()
		email = String()
		password = String()
		# firstName = String()
		# lastName = String()

	def mutate(self, info, username, email, password):
		user = get_user_model()(
			username=username,
			email=email,
			# firstName=firstName,
			# lastName=lastName
		)

		user.set_password(password)
		user.save()
		return CreateUser(user=user)


class Mutation(ObjectType):
	create_user = CreateUser.Field()
