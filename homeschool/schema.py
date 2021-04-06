import graphene
from graphene import Schema, ObjectType

from classes.schema import Query as ClassesQuery
from classes.schema import Mutation as ClassesMutation
from user.schema import Mutation as UserMutation


class Query(ClassesQuery, ObjectType):
	pass


class Mutation(ClassesMutation, UserMutation, ObjectType):
	pass


schema = Schema(query=Query, mutation=Mutation)
