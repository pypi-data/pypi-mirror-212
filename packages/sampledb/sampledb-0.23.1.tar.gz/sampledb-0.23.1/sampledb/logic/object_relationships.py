# coding: utf-8
"""

"""
from __future__ import annotations

import copy
import dataclasses
import datetime
import itertools
import typing

import flask

from .actions import get_action, Action
from .files import get_files_for_object, File
from .objects import get_object, find_object_references
from .object_permissions import get_user_permissions_for_multiple_objects, get_objects_with_permissions
from ..models import ObjectLogEntryType, ObjectLogEntry, Permissions, Object
from .. import db


def get_related_object_ids(
        object_id: int,
        include_referenced_objects: bool,
        include_referencing_objects: bool,
        user_id: typing.Optional[int] = None,
        filter_referencing_objects_by_permissions: bool = True
) -> typing.Tuple[
    typing.List[typing.Tuple[int, typing.Optional[str]]], typing.List[typing.Tuple[int, typing.Optional[str]]]
]:
    """
    Get IDs of objects related to a given object.

    An object is considered to be related, if it is:
    - a previous object of the given object (include_referenced_objects)
    - a measurement created using the given object (include_referencing_objects)
    - a sample created using the given object (include_referencing_objects)
    - any object referencing the given object in its metadata (include_referencing_objects)

    :param object_id: the ID of an existing object
    :param include_referenced_objects: whether to include referenced objects
    :param include_referencing_objects: whether to include referencing objects
    :param user_id: the ID of an existing user (optional)
    :param filter_referencing_objects_by_permissions: whether the referencing
        object ID list should only contain objects for which the given user has
        READ permissions
    :return: lists of previous object IDs, measurement IDs and sample IDs
    """
    referenced_object_ids: typing.Set[typing.Tuple[int, typing.Optional[str]]] = set()
    referencing_object_ids: typing.Set[typing.Tuple[int, typing.Optional[str]]] = set()
    if include_referenced_objects:
        object = get_object(object_id)
        for referenced_object_id, _previously_referenced_object_id, _schema_type in find_object_references(object, include_fed_references=True):
            if referenced_object_id is not None:
                referenced_object_ids.add(referenced_object_id)
    if include_referencing_objects:
        object_log_entries = ObjectLogEntry.query.filter(
            db.and_(
                ObjectLogEntry.object_id == object_id,
                ObjectLogEntry.type.in_((
                    ObjectLogEntryType.USE_OBJECT_IN_MEASUREMENT,
                    ObjectLogEntryType.USE_OBJECT_IN_SAMPLE_CREATION,
                    ObjectLogEntryType.REFERENCE_OBJECT_IN_METADATA
                ))
            )
        ).all()
        object_id_key_map = {
            ObjectLogEntryType.USE_OBJECT_IN_MEASUREMENT: 'measurement_id',
            ObjectLogEntryType.USE_OBJECT_IN_SAMPLE_CREATION: 'sample_id',
            ObjectLogEntryType.REFERENCE_OBJECT_IN_METADATA: 'object_id',
        }
        for object_log_entry in object_log_entries:
            object_id_key = object_id_key_map.get(object_log_entry.type, 'object_id')
            referencing_object_id = object_log_entry.data.get(object_id_key)
            if referencing_object_id is not None:
                referencing_object_ids.add((referencing_object_id, None))
        if filter_referencing_objects_by_permissions:
            object_permissions = get_user_permissions_for_multiple_objects(user_id, [referencing_object_id[0] for referencing_object_id in referencing_object_ids])
            referencing_object_ids = {
                referencing_object_id
                for referencing_object_id in referencing_object_ids
                if Permissions.READ in object_permissions[referencing_object_id[0]]
            }
    return list(referencing_object_ids), list(referenced_object_ids)


@dataclasses.dataclass(kw_only=True)
class RelatedObjectsTree:
    object_id: int
    component_uuid: typing.Optional[str]
    path: typing.List[typing.Union[typing.Tuple[int, typing.Optional[str]], int]]
    object: typing.Optional[Object]
    referenced_objects: typing.Optional[typing.List[RelatedObjectsTree]]
    referencing_objects: typing.Optional[typing.List[RelatedObjectsTree]]


def build_related_objects_tree(
        object_id: int,
        user_id: typing.Optional[int],
) -> RelatedObjectsTree:
    """
    Get the tree of related objects for a given object.

    Each node in the tree contains:
    - the ID of an object
    - one possible path from the given object to this object

    All nodes for an object contain the same path to it, and the node at this
    path also contains lists of nodes for previous objects, measurements and
    samples.

    :param object_id: the ID of an existing object
    :param user_id: the ID of an existing user
    :return: the related objects tree
    """
    subtrees: typing.Dict[typing.Tuple[int, typing.Optional[str]], typing.Tuple[RelatedObjectsTree, typing.List[typing.Tuple[int, typing.Optional[str]]], typing.List[typing.Tuple[int, typing.Optional[str]]]]] = {}
    _gather_subtrees(
        object_id=object_id,
        component_uuid=None,
        user_id=user_id,
        subtrees=subtrees
    )

    object_ids = tuple(
        object_id
        for object_id, component_uuid in subtrees
        if component_uuid is None or component_uuid == flask.current_app.config['FEDERATION_UUID']
    )
    objects = get_objects_with_permissions(user_id=user_id, permissions=Permissions.READ, object_ids=object_ids, name_only=True)
    objects_by_id = {
        object.object_id: object
        for object in objects
    }
    return _assemble_tree(subtrees[(object_id, None)][0], objects_by_id, subtrees)


def _get_referencing_object_ids(
        object_ids: typing.Set[int]
) -> typing.Dict[int, typing.Set[typing.Tuple[int, typing.Optional[str]]]]:
    if not object_ids:
        return {}
    referencing_object_ids_by_id: typing.Dict[int, typing.Set[typing.Tuple[int, typing.Optional[str]]]] = {
        object_id: set()
        for object_id in object_ids
    }
    for object_id, referencing_object_id, referencing_component_uuid in db.session.execute(db.text("""
        SELECT DISTINCT object_id, coalesce(data -> 'object_id', data -> 'sample_id', data -> 'measurement_id', NULL)::text::integer AS referencing_object_id, NULL AS referencing_component_uuid
        FROM object_log_entries
        WHERE object_id IN :object_ids AND type IN ('USE_OBJECT_IN_MEASUREMENT', 'USE_OBJECT_IN_SAMPLE_CREATION', 'REFERENCE_OBJECT_IN_METADATA')
    """), {'object_ids': tuple(object_ids)}).fetchall():
        referencing_object_ids_by_id[object_id].add((referencing_object_id, referencing_component_uuid))
    return referencing_object_ids_by_id


def _get_referenced_object_ids(
        object_ids: typing.Set[int]
) -> typing.Dict[int, typing.Set[typing.Tuple[int, typing.Optional[str]]]]:
    if not object_ids:
        return {}
    referenced_object_ids_by_id: typing.Dict[int, typing.Set[typing.Tuple[int, typing.Optional[str]]]] = {
        object_id: set()
        for object_id in object_ids
    }
    for object_id, referenced_object_id, referenced_component_uuid in db.session.execute(db.text("""
        WITH RECURSIVE properties(object_id, value) AS (
            SELECT objects_current.object_id, data.value
            FROM objects_current, jsonb_each(objects_current.data) AS data
            WHERE objects_current.object_id IN :object_ids AND jsonb_typeof(objects_current.data) = 'object'
        UNION ALL
            SELECT properties.object_id, coalesce(object_data.value, array_data.value)
            FROM properties
            LEFT OUTER JOIN jsonb_each(CASE
                WHEN jsonb_typeof(properties.value) = 'object' THEN properties.value
                ELSE '{}'::jsonb
            END) AS object_data ON jsonb_typeof(properties.value) = 'object'
            LEFT OUTER JOIN jsonb_array_elements(CASE
                WHEN jsonb_typeof(properties.value) = 'array' THEN properties.value
                ELSE '[]'::jsonb
            END) AS array_data ON jsonb_typeof(properties.value) = 'array'
            WHERE jsonb_typeof(properties.value) = 'object' OR jsonb_typeof(properties.value) = 'array'
        )
        SELECT object_id, (properties.value -> 'object_id')::integer, properties.value ->> 'component_uuid'
        FROM properties
        WHERE jsonb_typeof(properties.value) = 'object' AND properties.value ? '_type' AND properties.value ? 'object_id' AND properties.value ->> '_type' IN ('object_reference', 'sample', 'measurement')
    """), {'object_ids': tuple(object_ids)}).fetchall():
        referenced_object_ids_by_id[object_id].add((referenced_object_id, referenced_component_uuid))
    return referenced_object_ids_by_id


def _gather_subtrees(
        object_id: int,
        component_uuid: typing.Optional[str],
        user_id: typing.Optional[int],
        subtrees: typing.Dict[typing.Tuple[int, typing.Optional[str]], typing.Tuple[RelatedObjectsTree, typing.List[typing.Tuple[int, typing.Optional[str]]], typing.List[typing.Tuple[int, typing.Optional[str]]]]],
        parent_object_id: typing.Optional[int] = None,
        parent_component_id: typing.Optional[str] = None,
        referencing_object_ids: typing.Optional[typing.Set[typing.Tuple[int, typing.Optional[str]]]] = None,
        referenced_object_ids: typing.Optional[typing.Set[typing.Tuple[int, typing.Optional[str]]]] = None
) -> None:
    if (object_id, component_uuid) in subtrees:
        return
    tree = RelatedObjectsTree(
        object_id=object_id,
        component_uuid=component_uuid,
        path=[],
        object=None,
        referenced_objects=None,
        referencing_objects=None,
    )
    subtrees[object_id, component_uuid] = (tree, [], [])
    if component_uuid is None or component_uuid == flask.current_app.config['FEDERATION_UUID']:
        if referencing_object_ids is None:
            referencing_object_ids = _get_referencing_object_ids({object_id})[object_id]
        if referenced_object_ids is None:
            referenced_object_ids = _get_referenced_object_ids({object_id})[object_id]
        for child_object_list, filtered_child_object_list in [
            (referenced_object_ids, subtrees[object_id, component_uuid][1]),
            (referencing_object_ids, subtrees[object_id, component_uuid][2])
        ]:
            for child_object_id, child_component_uuid in child_object_list:
                if (child_object_id, child_component_uuid) != (parent_object_id, parent_component_id):
                    filtered_child_object_list.append((child_object_id, child_component_uuid))
        local_child_object_ids = {
            child_object_id
            for child_object_id, child_component_uuid in itertools.chain(subtrees[object_id, component_uuid][1], subtrees[object_id, component_uuid][2])
            if (child_object_id, child_component_uuid) not in subtrees and (child_component_uuid is None or child_component_uuid == flask.current_app.config['FEDERATION_UUID'])
        }
        referencing_object_ids_by_id = _get_referencing_object_ids(local_child_object_ids)
        referenced_object_ids_by_id = _get_referenced_object_ids(local_child_object_ids)
        for child_object_id, child_component_uuid in itertools.chain(subtrees[object_id, component_uuid][1], subtrees[object_id, component_uuid][2]):
            if (child_object_id, child_component_uuid) not in subtrees:
                if child_component_uuid is None or child_component_uuid == flask.current_app.config['FEDERATION_UUID']:
                    referencing_object_ids = referencing_object_ids_by_id.get(child_object_id)
                    referenced_object_ids = referenced_object_ids_by_id.get(child_object_id)
                else:
                    referencing_object_ids = None
                    referenced_object_ids = None
                _gather_subtrees(
                    object_id=child_object_id,
                    component_uuid=child_component_uuid,
                    user_id=user_id,
                    subtrees=subtrees,
                    parent_object_id=object_id,
                    parent_component_id=component_uuid,
                    referencing_object_ids=referencing_object_ids,
                    referenced_object_ids=referenced_object_ids
                )


def _assemble_tree(
        tree: RelatedObjectsTree,
        objects_by_id: typing.Dict[int, Object],
        subtrees: typing.Dict[typing.Tuple[int, typing.Optional[str]], typing.Tuple[RelatedObjectsTree, typing.List[typing.Tuple[int, typing.Optional[str]]], typing.List[typing.Tuple[int, typing.Optional[str]]]]],
        path_prefix: typing.Optional[typing.List[typing.Union[int, typing.Tuple[int, typing.Optional[str]]]]] = None
) -> RelatedObjectsTree:
    if path_prefix is None:
        path_prefix = []

    tree, referenced_object_ids, referencing_object_ids = subtrees[(tree.object_id, tree.component_uuid)]
    if not tree.path:
        tree.path = path_prefix + [(tree.object_id, tree.component_uuid)]
        if tree.component_uuid is None or tree.component_uuid == flask.current_app.config['FEDERATION_UUID']:
            if tree.object_id in objects_by_id:
                tree.object = objects_by_id[tree.object_id]
                # create a copy that will contain subtrees
                tree = copy.deepcopy(tree)
                tree.referenced_objects = [
                    _assemble_tree(subtrees[referenced_object_id][0], objects_by_id, subtrees, tree.path + [-1])
                    for referenced_object_id in referenced_object_ids
                ]
                tree.referencing_objects = [
                    _assemble_tree(subtrees[referencing_object_id][0], objects_by_id, subtrees, tree.path + [-2])
                    for referencing_object_id in referencing_object_ids
                    if referencing_object_id[0] in objects_by_id and (referencing_object_id[1] is None or referencing_object_id[1] == flask.current_app.config['FEDERATION_UUID'])
                ]
    return tree


@dataclasses.dataclass(frozen=True)
class WorkflowElement:
    object_id: int
    object: typing.Optional[Object]
    action: typing.Optional[Action]
    is_referencing: bool
    is_referenced: bool
    files: typing.List[File]


def get_workflow_references(object: Object, user_id: int, actions_by_id: typing.Optional[typing.Dict[int, Action]] = None) -> typing.List[WorkflowElement]:
    """
    Creates a list describing all direct object relations for a workflow view as configured in an object's schema.


    :param object: The object for which the workflow view is to be created
    :param user_id: User ID of the user viewing the workflow view taking into account the access permissions
    :param actions_by_id: A dict containing cached actions by ID
    :return: List of WorkflowElements containing, object ID, object data, action data and if the object is referenced
            and/or referencing the object the view is created for
    """
    if object.schema is None or 'workflow_view' not in object.schema.keys():
        return []

    if actions_by_id is None:
        actions_by_id = {}

    referencing_objects = {obj[0] for obj in _get_referencing_object_ids({object.object_id})[object.object_id] if obj[1] is None}
    referenced_objects = {obj[0] for obj in _get_referenced_object_ids({object.object_id})[object.object_id] if obj[1] is None}

    referencing_workflow_action_ids = None if 'referencing_action_id' not in object.schema['workflow_view'] else [object.schema['workflow_view']['referencing_action_id']] if isinstance(object.schema['workflow_view']['referencing_action_id'], int) else object.schema['workflow_view']['referencing_action_id']
    referencing_workflow_action_type_ids = None if 'referencing_action_type_id' not in object.schema['workflow_view'] else [object.schema['workflow_view']['referencing_action_type_id']] if isinstance(object.schema['workflow_view']['referencing_action_type_id'], int) else object.schema['workflow_view']['referencing_action_type_id']

    referenced_workflow_action_ids = None if 'referenced_action_id' not in object.schema['workflow_view'] else [object.schema['workflow_view']['referenced_action_id']] if isinstance(object.schema['workflow_view']['referenced_action_id'], int) else object.schema['workflow_view']['referenced_action_id']
    referenced_workflow_action_type_ids = None if 'referenced_action_type_id' not in object.schema['workflow_view'] else [object.schema['workflow_view']['referenced_action_type_id']] if isinstance(object.schema['workflow_view']['referenced_action_type_id'], int) else object.schema['workflow_view']['referenced_action_type_id']

    object_ids = list(referencing_objects.union(referenced_objects))
    objects = get_objects_with_permissions(user_id, Permissions.READ, object_ids=object_ids)
    objects_by_id = {
        object.object_id: object
        for object in objects
    }
    initital_object_version_by_id = {}
    for object_id in object_ids:
        current_object_version = objects_by_id.get(object_id)
        if current_object_version is not None and current_object_version.version_id == 0:
            initital_object_version_by_id[object_id] = current_object_version
        else:
            initital_object_version_by_id[object_id] = get_object(object_id, version_id=0)

    def creation_time_key(object_id: int) -> datetime.datetime:
        initital_object_version = initital_object_version_by_id.get(object_id)
        if initital_object_version is None or initital_object_version.utc_datetime is None:
            return datetime.datetime.max
        return initital_object_version.utc_datetime

    object_ids.sort(key=creation_time_key)

    workflow = []
    for object_id in object_ids:
        action_id = initital_object_version_by_id[object_id].action_id
        if action_id:
            if action_id in actions_by_id:
                action = actions_by_id[action_id]
            else:
                action = get_action(action_id)
                actions_by_id[action_id] = action
        else:
            action = None

        if (
            (referencing_workflow_action_ids is None and referenced_workflow_action_ids is None and referencing_workflow_action_type_ids is None and referenced_workflow_action_type_ids is None) or
            (
                object_id in referencing_objects and
                (
                    (referencing_workflow_action_ids is None or action_id in referencing_workflow_action_ids) and
                    (
                        referencing_workflow_action_type_ids is None or
                        (
                            action and action.type and (
                                action.type.id in referencing_workflow_action_type_ids or
                                (action.type.fed_id and action.type.fed_id < 0 and action.type.fed_id in referencing_workflow_action_type_ids)
                            )
                        )
                    )
                )
            ) or (
                object_id in referenced_objects and
                (
                    (referenced_workflow_action_ids is None or action_id in referenced_workflow_action_ids) and
                    (
                        referenced_workflow_action_type_ids is None or
                        (
                            action and action.type and
                            (
                                action.type.id in referenced_workflow_action_type_ids or
                                (action.type.fed_id and action.type.fed_id < 0 and action.type.fed_id in referenced_workflow_action_type_ids)
                            )
                        )
                    )
                )
            )
        ):
            if object_id in objects_by_id:
                files = get_files_for_object(object_id)
            else:
                files = []
            workflow.append(WorkflowElement(
                object_id=object_id,
                object=objects_by_id.get(object_id),
                action=action,
                is_referenced=object_id in referenced_objects,
                is_referencing=object_id in referencing_objects,
                files=files
            ))
    return workflow
