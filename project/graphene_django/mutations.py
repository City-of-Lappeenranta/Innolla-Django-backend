# -*- coding: utf-8 -*-
#
# Copyright Haltu Oy, info@haltu.fi
# All rights reserved.
#

import graphene
from graphene import relay
from graphql_relay import from_global_id
from django.db import models
from graphene_django.forms.mutation import DjangoModelDjangoFormMutationOptions
from project.graphene_django.exceptions import PermissionDenied


class PermissionClassesMutationMixin(object):
  @classmethod
  def mutate_and_get_payload(cls, root, info, **input):
    permissions = cls.permission_classes()

    for permission in permissions:
      if not permission.has_permission(info.context):
        raise PermissionDenied

    return super().mutate_and_get_payload(root, info, **input)

  @staticmethod
  def permission_classes():
    raise NotImplementedError


class DeleteMutation(relay.ClientIDMutation):
  class Meta:
    abstract = True

  @classmethod
  def __init_subclass_with_meta__(cls, model=None, return_node=None, return_field_name=None, _meta=None, **options):
    if not _meta:
      _meta = DjangoModelDjangoFormMutationOptions(cls)

    if not return_node:
      raise Exception(
        "return_node is required for DeleteMutation")

    if not model:
      raise Exception(
        "model is required for DeleteMutation")

    if not return_field_name:
      model_name = model.__name__
      return_field_name = model_name[:1].lower() + model_name[1:]

    _meta = DjangoModelDjangoFormMutationOptions(cls)
    _meta.model = model
    _meta.return_field_name = return_field_name

    setattr(cls, return_field_name, graphene.Field(return_node))

    super().__init_subclass_with_meta__(_meta=_meta, **options)

  @classmethod
  def mutate_and_get_payload(cls, root, info, id=None):
    model = cls._meta.model
    instance = None

    if id:
      try:
        instance = model.objects.get(pk=from_global_id(id)[1])
        instance.delete()
      except model.DoesNotExist:
        pass

    return cls(**{
      cls._meta.return_field_name: instance
    })


class UpsertMutation(relay.ClientIDMutation):
  class Meta:
    abstract = True

  @classmethod
  def __init_subclass_with_meta__(cls, model=None, return_node=None, return_field_name=None, _meta=None, **options):
    if not _meta:
      _meta = DjangoModelDjangoFormMutationOptions(cls)

    if not return_node:
      raise Exception(
        "return_node is required for UpsertMutation")

    if not model:
      raise Exception(
        "model is required for UpsertMutation")

    if not return_field_name:
      model_name = model.__name__
      return_field_name = model_name[:1].lower() + model_name[1:]

    _meta = DjangoModelDjangoFormMutationOptions(cls)
    _meta.model = model
    _meta.return_field_name = return_field_name

    setattr(cls, return_field_name, graphene.Field(return_node))

    super().__init_subclass_with_meta__(_meta=_meta, **options)

  @classmethod
  def mutate_and_get_payload(cls, root, info, _id=None, **_input):
    model = cls._meta.model
    instance = None

    if _input:
      _input = convert_global_ids(_input, model)
      if _id:
        instance = model.objects.get(pk=from_global_id(_id)[1])
        _input, many = resolve_many(_input)
        instance = model.objects.filter(pk=from_global_id(_id)[1])
        instance.update(**_input)
        instance = instance.first()
        save_many(instance, many)
        save_files(instance, _input)
      else:
        _input, many = resolve_many(_input)
        instance = model(**_input)
        instance.save()
        save_many(instance, many)
        save_files(instance, _input)

    return cls(**{
      cls._meta.return_field_name: instance
    })


def resolve_many(_input):
  many = {}
  for key, value in list(_input.items()):
    if isinstance(value, list):
      many[key] = _input.pop(key)
  return _input, many


def save_many(instance, many):
  for key, value in list(many.items()):
    if isinstance(value, list):
      field = getattr(instance, key)
      field.remove()
      field.set(value)
  return many


def save_files(instance, _input):
  for model_field in instance._meta.fields:
    if isinstance(model_field, models.FileField):
      _file = _input.get(model_field.name, None)
      if _file:
        field = getattr(instance, model_field.name)
        field.save(_file._name, _file)


def convert_global_ids(_input, model):
  for key, value in _input.items():
    if isinstance(value, str):
      _input[key] = convert_global_id(key, value, model)
    elif isinstance(value, list):
      instances = []
      for list_value in value:
        instances.append(convert_global_id(key, list_value, model))
      _input[key] = instances
  return _input


def convert_global_id(key, value, model):
  try:
    _, pk = from_global_id(value)
    # Field being relative we need to return instance,
    # only id field needs pk itself.
    try:
      _model = getattr(model, key).field.related_model
      return _model.objects.get(pk=pk)
    except:
      return pk
  except:
    return value


# vim: tabstop=2 expandtab shiftwidth=2 softtabstop=2
