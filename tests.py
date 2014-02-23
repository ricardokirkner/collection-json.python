from __future__ import absolute_import, unicode_literals
import json
from unittest import TestCase

from collection_json import (
    Array,
    Collection,
    Data,
    Error,
    Item,
    Link,
    Query,
    Template,
)


class CollectionTestCase(TestCase):

    def test_from_json_invalid_data(self):
        with self.assertRaises(ValueError):
            Collection.from_json('')

    def test_from_json_invalid_document(self):
        with self.assertRaises(ValueError):
            Collection.from_json('{}')

    def test_from_json_invaid_uri(self):
        with self.assertRaises(ValueError):
            Collection.from_json('{"collection": {}}')

    def test_from_json_minimal(self):
        collection = Collection.from_json(
            '{"collection": {"href": "http://example.org"}}')
        self.assertEqual(collection.version, '1.0')
        self.assertEqual(collection.href, 'http://example.org')
        self.assertEqual(collection.links, Array(Link, 'links', []))
        self.assertEqual(collection.items, Array(Item, 'items', []))
        self.assertEqual(collection.queries, Array(Query, 'queries', []))
        self.assertEqual(collection.template, None)
        self.assertEqual(collection.error, None)

    def test_from_json_with_error_data(self):
        data = json.dumps({
            'collection': {
                'version': '1.0',
                'href': 'http://example.org',
                'error': {
                    'code': 'code',
                    'message': 'message',
                    'title': 'title',
                }
            }
        })
        collection = Collection.from_json(data)
        self.assertEqual(collection.error,
                         Error('code', 'message', 'title'))

    def test_from_json_with_template_data(self):
        data = json.dumps({
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'template': {
                    'data': [
                        {'name': 'name', 'value': 'value', 'prompt': 'prompt'}
                    ]
                }
            }
        })
        collection = Collection.from_json(data)
        self.assertEqual(collection.template,
                         Template([Data('name', 'value', 'prompt')]))

    def test_from_json_with_items_data(self):
        data = json.dumps({
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'items': [
                    {
                        'href': 'href',
                        'data': [
                            {'name': 'name'}
                        ],
                        'links': [
                            {'href': 'href', 'rel': 'rel'}
                        ]
                    }
                ],
            }
        })
        collection = Collection.from_json(data)
        data = Data('name')
        link = Link('href', 'rel')
        item = Item('href', [data], [link])
        self.assertEqual(collection.items, Array(Item, 'items', [item]))

    def test_from_json_with_links_data(self):
        data = json.dumps({
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'links': [
                    {
                        'rel': 'rel',
                        'href': 'href',
                    }
                ],
            }
        })
        collection = Collection.from_json(data)
        link = Link('href', 'rel')
        self.assertEqual(collection.links, Array(Link, 'links', [link]))

    def test_from_json_with_queries_data(self):
        data = json.dumps({
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'queries': [
                    {
                        'rel': 'rel',
                        'href': 'href',
                    }
                ],
            }
        })
        collection = Collection.from_json(data)
        query = Query('href', 'rel')
        self.assertEqual(collection.queries, Array(Query, 'queries', [query]))

    def test_collection_required_parameters(self):
        with self.assertRaises(TypeError):
            Collection()

    def test_collection_defaults(self):
        collection = Collection('href')
        self.assertEqual(collection.version, '1.0')
        self.assertEqual(collection.href, 'href')
        self.assertEqual(collection.error, None)
        self.assertEqual(collection.template, None)
        self.assertEqual(collection.items, Array(Item, 'items', []))
        self.assertEqual(collection.links, Array(Link, 'links', []))
        self.assertEqual(collection.queries, Array(Query, 'queries', []))

    def test_to_dict_minimal(self):
        collection = Collection(
            href='http://example.com')
        self.assertEqual(collection.to_dict(), {
            'collection': {
                'version': '1.0',
                'href': 'http://example.com'
            }
        })

    def test_to_dict_with_links(self):
        link = Link('href', 'rel')
        collection = Collection(
            href='http://example.com',
            links=[link])
        self.assertEqual(collection.to_dict(), {
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'links': [
                    {'href': 'href', 'rel': 'rel'}
                ]
            }
        })

    def test_to_dict_with_items(self):
        item = Item('href')
        collection = Collection(
            href='http://example.com',
            items=[item])
        self.assertEqual(collection.to_dict(), {
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'items': [
                    {'href': 'href'}
                ]
            }
        })

    def test_to_dict_with_queries(self):
        query = Query('href', 'rel')
        collection = Collection(
            href='http://example.com',
            queries=[query])
        self.assertEqual(collection.to_dict(), {
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'queries': [
                    {'href': 'href', 'rel': 'rel'}
                ]
            }
        })

    def test_to_dict_with_template(self):
        data = Data('name')
        template = Template([data])
        collection = Collection(
            href='http://example.com',
            template=template)
        self.assertEqual(collection.to_dict(), {
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'template': {
                    'data': [
                        {'name': 'name'}
                    ]
                }
            }
        })

    def test_to_dict_with_error(self):
        error = Error('code', 'message', 'title')
        collection = Collection(
            href='http://example.com',
            error=error)
        self.assertEqual(collection.to_dict(), {
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'error': {
                    'code': 'code',
                    'message': 'message',
                    'title': 'title',
                }
            }
        })

    def test_to_dict_full(self):
        link = Link('href', 'rel', 'name', 'render', 'prompt')
        data = Data('name', 'value', 'prompt')
        item = Item('href', [data], [link])
        query = Query('href', 'rel', 'name', 'prompt', [data])
        template = Template([data])
        error = Error('code', 'message', 'title')
        collection = Collection(
            href='http://example.com',
            links=[link],
            items=[item],
            queries=[query],
            template=template,
            error=error)
        expected = {
            'collection': {
                'version': '1.0',
                'href': 'http://example.com',
                'links': [
                    {
                        'rel': 'rel',
                        'href': 'href',
                        'name': 'name',
                        'render': 'render',
                        'prompt': 'prompt',
                    }
                ],
                'items': [
                    {
                        'href': 'href',
                        'data': [
                            {
                                'name': 'name',
                                'value': 'value',
                                'prompt': 'prompt',
                            }
                        ],
                        'links': [
                            {
                                'rel': 'rel',
                                'href': 'href',
                                'name': 'name',
                                'render': 'render',
                                'prompt': 'prompt',
                            }
                        ]
                    }
                ],
                'queries': [
                    {
                        'rel': 'rel',
                        'href': 'href',
                        'name': 'name',
                        'prompt': 'prompt',
                        'data': [
                            {
                                'name': 'name',
                                'value': 'value',
                                'prompt': 'prompt',
                            }
                        ]
                    }
                ],
                'template': {
                    'data': [
                        {
                            'name': 'name',
                            'value': 'value',
                            'prompt': 'prompt',
                        }
                    ]
                },
                'error': {
                    'code': 'code',
                    'message': 'message',
                    'title': 'title',
                }
            }
        }
        self.assertEqual(collection.to_dict(), expected)

    def test_repr(self):
        collection = Collection('href')
        self.assertEqual(
            repr(collection),
            "<Collection: version='1.0' href='href'>")


class ErrorTestCase(TestCase):

    def test_error_minimal(self):
        error = Error()
        self.assertEqual(error.code, None)
        self.assertEqual(error.message, None)
        self.assertEqual(error.title, None)

    def test_error_with_data(self):
        error = Error('code', 'message', 'title')
        self.assertEqual(error.code, 'code')
        self.assertEqual(error.message, 'message')
        self.assertEqual(error.title, 'title')

    def test_error_minimal_to_dict(self):
        error = Error()
        expected = {
            'error': {}
        }
        self.assertEqual(error.to_dict(), expected)

    def test_error_to_dict(self):
        error = Error('code', 'message', 'title')
        expected = {
            'error': {
                'code': 'code',
                'message': 'message',
                'title': 'title',
            }
        }
        self.assertEqual(error.to_dict(), expected)

    def test_error_equal(self):
        error = Error()
        other = Error('code', 'message', 'title')
        self.assertTrue(error.__eq__(error))
        self.assertTrue(other.__eq__(other))
        self.assertFalse(error.__eq__(other))
        self.assertFalse(other.__eq__(error))

    def test_error_not_equal(self):
        error = Error()
        other = Error('code', 'message', 'title')
        self.assertFalse(error.__ne__(error))
        self.assertFalse(other.__ne__(other))
        self.assertTrue(error.__ne__(other))
        self.assertTrue(other.__ne__(error))

    def test_repr_minimal(self):
        error = Error()
        self.assertEqual(repr(error), '<Error>')

    def test_repr_with_code(self):
        error = Error(code='code')
        self.assertEqual(repr(error), "<Error code='code'>")

    def test_repr_with_message(self):
        error = Error(message='message')
        self.assertEqual(repr(error), "<Error message='message'>")

    def test_repr_with_title(self):
        error = Error(title='title')
        self.assertEqual(repr(error), "<Error title='title'>")

    def test_repr_full(self):
        error = Error('code', 'message', 'title')
        self.assertEqual(
            repr(error),
            "<Error code='code' message='message' title='title'>")


class TemplateTestCase(TestCase):

    def test_template_minimal(self):
        template = Template()
        self.assertEqual(template.data, Array(Data, 'data', []))

    def test_template_with_data(self):
        data = [Data('name')]
        template = Template(data)
        self.assertEqual(template.data, Array(Data, 'data', data))

    def test_template_minimal_to_dict(self):
        template = Template()
        expected = {
            'template': {
                'data': [],
            }
        }
        self.assertEqual(template.to_dict(), expected)

    def test_template_to_dict(self):
        data = [Data('name')]
        template = Template(data)
        expected = {
            'template': {
                'data': [
                    {'name': 'name'}
                ]
            }
        }
        self.assertEqual(template.to_dict(), expected)

    def test_repr_minimal(self):
        template = Template()
        self.assertEqual(repr(template), "<Template: data=[]>")

    def test_repr_with_data(self):
        data = [Data('name')]
        template = Template(data)
        self.assertEqual(repr(template), "<Template: data=['name']>")

    def test_properties_minimal(self):
        template = Template()
        self.assertEqual(template.properties, [])

    def test_properties(self):
        data = [Data('name'), Data('other')]
        template = Template(data)
        self.assertEqual(template.properties, ['name', 'other'])


class ItemTestCase(TestCase):
    def test_item_minimal(self):
        item = Item()
        self.assertEqual(item.href, None)
        self.assertEqual(item.data, Array(Data, 'data', []))
        self.assertEqual(item.links, Array(Link, 'links', []))

    def test_item_with_data(self):
        data = [Data('name')]
        links = [Link('href', 'rel')]
        item = Item('href', data, links)
        self.assertEqual(item.href, 'href')
        self.assertEqual(item.data, Array(Data, 'data', data))
        self.assertEqual(item.links, Array(Link, 'links', links))

    def test_repr(self):
        data = [Data('name')]
        links = [Link('href', 'rel')]
        item = Item('href', data, links)
        expected = "<Item: href='href'>"
        self.assertEqual(repr(item), expected)

    def test_to_dict_minimal(self):
        item = Item()
        expected = {}
        self.assertEqual(item.to_dict(), expected)

    def test_to_dict_with_data(self):
        data = [Data('name')]
        links = [Link('href', 'rel')]
        item = Item('href', data, links)
        expected = {
            'href': 'href',
            'data': [
                {'name': 'name'}
            ],
            'links': [
                {'href': 'href', 'rel': 'rel'}
            ]
        }
        self.assertEqual(item.to_dict(), expected)

    def test_properties_minimal(self):
        item = Item()
        self.assertEqual(item.properties, [])

    def test_properties(self):
        data = [Data('name'), Data('other')]
        item = Item(data=data)
        self.assertEqual(item.properties, ['name', 'other'])


class DataTestCase(TestCase):
    def test_data_minimal(self):
        data = Data('name')
        self.assertEqual(data.name, 'name')
        self.assertEqual(data.value, None)
        self.assertEqual(data.prompt, None)

    def test_data_with_data(self):
        data = Data('name', 'value', 'prompt')
        self.assertEqual(data.name, 'name')
        self.assertEqual(data.value, 'value')
        self.assertEqual(data.prompt, 'prompt')

    def test_repr(self):
        data = Data('name', 'value', 'prompt')
        expected = "<Data: name='name' prompt='prompt'>"
        self.assertEqual(repr(data), expected)

    def test_to_dict_minimal(self):
        data = Data('name')
        expected = {
            'name': 'name'
        }
        self.assertEqual(data.to_dict(), expected)

    def test_to_dict_with_data(self):
        data = Data('name', 'value', 'prompt')
        expected = {
            'name': 'name',
            'value': 'value',
            'prompt': 'prompt',
        }
        self.assertEqual(data.to_dict(), expected)

    def test_repr_minimal(self):
        data = Data('name')
        self.assertEqual(repr(data), "<Data: name='name'>")

    def test_repr_with_prompt(self):
        data = Data('name', prompt='prompt')
        self.assertEqual(repr(data), "<Data: name='name' prompt='prompt'>")


class QueryTestCase(TestCase):
    def test_query_minimal(self):
        query = Query('href', 'rel')
        self.assertEqual(query.href, 'href')
        self.assertEqual(query.rel, 'rel')
        self.assertEqual(query.name, None)
        self.assertEqual(query.prompt, None)
        self.assertEqual(query.data, Array(Data, 'data', []))

    def test_query_with_data(self):
        data = [Data('name')]
        query = Query('href', 'rel', 'name', 'prompt', data)
        self.assertEqual(query.href, 'href')
        self.assertEqual(query.rel, 'rel')
        self.assertEqual(query.name, 'name')
        self.assertEqual(query.prompt, 'prompt')
        self.assertEqual(query.data, Array(Data, 'data', data))

    def test_repr_minimal(self):
        query = Query('href', 'rel')
        expected = "<Query: rel='rel'>"
        self.assertEqual(repr(query), expected)

    def test_repr_with_name(self):
        data = [Data('name')]
        query = Query('href', 'rel', 'name', data=data)
        expected = "<Query: rel='rel' name='name'>"
        self.assertEqual(repr(query), expected)

    def test_repr_with_prompt(self):
        data = [Data('name')]
        query = Query('href', 'rel', 'name', 'prompt', data)
        expected = "<Query: rel='rel' name='name' prompt='prompt'>"
        self.assertEqual(repr(query), expected)

    def test_to_dict_minimal(self):
        query = Query('href', 'rel')
        expected = {
            'href': 'href',
            'rel': 'rel',
        }
        self.assertEqual(query.to_dict(), expected)

    def test_to_dict_with_data(self):
        data = [Data('name')]
        query = Query('href', 'rel', 'name', 'prompt', data)
        expected = {
            'href': 'href',
            'rel': 'rel',
            'name': 'name',
            'prompt': 'prompt',
            'data': [
                {'name': 'name'}
            ]
        }
        self.assertEqual(query.to_dict(), expected)


class LinkTestCase(TestCase):
    def test_link_minimal(self):
        link = Link('href', 'rel')
        self.assertEqual(link.href, 'href')
        self.assertEqual(link.rel, 'rel')
        self.assertEqual(link.name, None)
        self.assertEqual(link.render, None)
        self.assertEqual(link.prompt, None)

    def test_link_with_data(self):
        link = Link('href', 'rel', 'name', 'render', 'prompt')
        self.assertEqual(link.href, 'href')
        self.assertEqual(link.rel, 'rel')
        self.assertEqual(link.name, 'name')
        self.assertEqual(link.render, 'render')
        self.assertEqual(link.prompt, 'prompt')

    def test_repr_minimal(self):
        link = Link('href', 'rel')
        expected = "<Link: rel='rel'>"
        self.assertEqual(repr(link), expected)

    def test_repr_with_name(self):
        link = Link('href', 'rel', 'name')
        expected = "<Link: rel='rel' name='name'>"
        self.assertEqual(repr(link), expected)

    def test_repr_with_render(self):
        link = Link('href', 'rel', render='render')
        expected = "<Link: rel='rel' render='render'>"
        self.assertEqual(repr(link), expected)

    def test_repr_full(self):
        link = Link('href', 'rel', 'name', 'render', 'prompt')
        expected = ("<Link: rel='rel' name='name' "
                    "render='render' prompt='prompt'>")
        self.assertEqual(repr(link), expected)

    def test_to_dict_minimal(self):
        link = Link('href', 'rel')
        expected = {
            'href': 'href',
            'rel': 'rel',
        }
        self.assertEqual(link.to_dict(), expected)

    def test_to_dict_with_data(self):
        link = Link('href', 'rel', 'name', 'render', 'prompt')
        expected = {
            'href': 'href',
            'rel': 'rel',
            'name': 'name',
            'render': 'render',
            'prompt': 'prompt',
        }
        self.assertEqual(link.to_dict(), expected)


class ArrayTestCase(TestCase):
    def test_init(self):
        item_class = dict
        array = Array(item_class, 'collection', [])
        self.assertEqual(array.item_class, dict)
        self.assertEqual(array.collection_name, 'collection')
        self.assertEqual(list(array), [])

    def test_invalid_items(self):
        with self.assertRaises(ValueError):
            Array(Data, 'data', [1, 2, 3])

    def test_equal(self):
        array1 = Array(dict, 'items', [{1: 1}])
        array2 = Array(dict, 'items', [{1: 1}])
        self.assertEqual(array1, array1)
        self.assertEqual(array1, array2)

    def test_not_equal(self):
        array1 = Array(dict, 'items', [{1: 1}])
        list1 = [{1: 1}]
        self.assertNotEqual(array1, list1)

    def test_find_by_rel(self):
        link = Link('href', rel='foo')
        links = Array(Link, 'links', [link])
        self.assertEqual(links.find(rel='foo'), [link])

    def test_find_by_rel_not_found(self):
        link = Link('href', rel='foo')
        links = Array(Link, 'links', [link])
        self.assertEqual(links.find(rel='bar'), [])

    def test_find_by_rel_multiple_values(self):
        link1 = Link('href1', rel='foo')
        link2 = Link('href2', rel='foo')
        links = Array(Link, 'links', [link1, link2])
        self.assertEqual(links.find(rel='foo'), [link1, link2])

    def test_find_by_name(self):
        link = Link('href', rel='foo', name='bar')
        links = Array(Link, 'links', [link])
        self.assertEqual(links.find(rel='foo'), [link])
        self.assertEqual(links.find(name='bar'), [link])

    def test_find_by_name_not_found(self):
        link = Link('href', rel='foo', name='bar')
        links = Array(Link, 'links', [link])
        self.assertEqual(links.find(name='foo'), [])

    def test_find_by_name_multiple_values(self):
        link1 = Link('href1', rel='foo', name='bar')
        link2 = Link('href2', rel='foo', name='bar')
        links = Array(Link, 'links', [link1, link2])
        self.assertEqual(links.find(name='bar'), [link1, link2])

    def test_find_by_rel_and_name(self):
        foo = Link('href', rel='foo', name='bar')
        bar = Link('href', rel='bar')
        links = Array(Link, 'links', [foo, bar])
        self.assertEqual(links.find(rel='foo', name='bar'), [foo])
        self.assertEqual(links.find(rel='bar', name='foo'), [])

    def test_attribute_lookup_by_name(self):
        foo = Link('href', rel='foo', name='bar')
        links = Array(Link, 'links', [foo])
        self.assertEqual(links.bar, foo)

    def test_attribute_lookup_by_name_not_found(self):
        links = Array(Link, 'links', [])
        with self.assertRaises(AttributeError):
            links.foo

    def test_attribute_lookup_by_name_multiple_values(self):
        foo = Link('href1', rel='bar', name='foo')
        bar = Link('href2', rel='baz', name='foo')
        links = Array(Link, 'links', [foo, bar])
        self.assertEqual(links.foo, [foo, bar])
