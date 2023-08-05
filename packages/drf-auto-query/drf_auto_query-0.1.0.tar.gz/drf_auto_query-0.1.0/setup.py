# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_auto_query']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2', 'djangorestframework']

setup_kwargs = {
    'name': 'drf-auto-query',
    'version': '0.1.0',
    'description': 'Auto generate Django ORM query sets from serializers.',
    'long_description': '# drf-auto-query\n\nAuto generate Django ORM query sets from serializers.\n\n## Installation\n\n```bash\n$ pip install drf-auto-query\n```\n\n## Description\n\nThe "drf-auto-query" package addresses the common problem of N+1 queries in Django ORM when building REST framework \nendpoints. It provides convenient helper functions and mixins to assist in generating efficient QuerySet objects \ntailored to your specific serializer requirements.\n\nIt is important to note that while "drf-auto-query" aims to alleviate the N+1 problem, it is not a comprehensive \nsolution. Instead, it serves as a valuable tool to be used in conjunction with your own efforts to write efficient \nqueries. By automating the process of prefetching related data, the package helps reduce the number of database \nqueries required, resulting in improved performance and responsiveness for your Django-based APIs, while it also speeds\nup development because you will not have to worry about your serializer setup firing unwanted database queries.\n\n\n## Usage\n\n### Prefetch function\n\nThe `prefetch_queryset_for_serializer` function streamlines the process of setting up the necessary `prefetch_related` \nand `select_related` calls on a `QuerySet` based on a given serializer class.\n\n```python\nfrom rest_framework import serializers\nfrom drf_auto_query import prefetch_queryset_for_serializer\n\nfrom my_app.models import UserGroup\n\n\nclass UserSerializer(serializers.Serializer):\n    id = serializers.IntegerField()\n    username = serializers.CharField()\n    email = serializers.EmailField()\n\n    \nclass UserGroupSerializer(serializers.Serializer):\n    id = serializers.IntegerField()\n    name = serializers.CharField()\n    users = UserSerializer(many=True)\n    \n    \nqueryset = UserGroup.objects.all()\nqueryset = prefetch_queryset_for_serializer(queryset, UserGroupSerializer)\n```\n\n### QuerySet mixin\n\nThe `AutoQuerySetMixin` offers a convenient way to automatically prefetch the required relations on a `QuerySet`.\n\n```python\nfrom django.db import models\n\nfrom drf_auto_query.mixins import AutoQuerySetMixin\n\n\nclass MyModelQuerySet(AutoQuerySetMixin, models.Model):\n    ...\n    \n    \nclass MyModel(models.Model):\n    ...\n    \n    objects = models.Manager.from_queryset(MyModelQuerySet)()\n```\n\nThis can then be used in a class based view.\n\n```python\nfrom rest_framework import generics\n\nfrom my_app.models import MyModel\nfrom my_app.serializers import MyModelSerializer\n\n\nclass MyModelList(generics.ListAPIView):\n    serializer_class = MyModelSerializer\n    queryset = MyModel.objects.prefetch_for(serializer_class)\n```\n\nUsing the both the mixin and the prefetch function ensures that any annotations, joins, or other modifications to the \nQuerySet are preserved while automatically prefetching the necessary data for efficient serialization.\n\n> :warning: Any multi-nested prefetches that have altered querysets might be \n> overwritten. This is a known issue and will be addressed in a future release.\n> \n> Example of a multi-nested prefetch:\n> ```python\n> MyModel.objects.prefetch_related(\n>     Prefetch(\n>         \'my_related_model\',\n>         queryset=MyRelatedModel.objects.prefetch_related(\n>             Prefetch(\n>                 \'my_other_related_model\',\n>                 # This queryset might not be preserved.\n>                 queryset=MyOtherRelatedModel.objects.annotate(count_something=Count(\'something\'))\n>             )\n>         )\n>     )\n> )\n> \n> MyModel.objects.prefetch_related(\n>     Prefetch(\n>         \'my_related_model__my_other_related_model\',\n>         # This will be preserved.\n>         queryset=MyOtherRelatedModel.objects.annotate(count_something=Count(\'something\'))\n>     )\n> )\n> ```\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a \nCode of Conduct. By contributing to this project, you agree to abide by its terms.\n\n\n## License\n\n`drf-auto-query` was created by Jakob Verlic. It is licensed under the terms of the MIT license.\n',
    'author': 'drf-auto-query',
    'author_email': 'jakobverlic66@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jazzyoda5/drf-auto-query',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
