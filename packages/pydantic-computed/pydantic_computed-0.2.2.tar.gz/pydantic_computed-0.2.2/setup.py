# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_computed']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-computed',
    'version': '0.2.2',
    'description': 'A new decorator for pydantic allowing you to define dynamic fields that are computed from other properties',
    'long_description': '# pydantic-computed\nA new decorator for pydantic allowing you to define dynamic fields that are computed from other properties.\n\n## Installation\n\nInstall the package by running\n```bash\npip install pydantic_computed\n```\n\n## Examples and use cases\n\n\n### A computed integer property\n```python\nfrom pydantic import BaseModel\nfrom pydantic_computed import Computed, computed\n\nclass ComputedModelInt(BaseModel):\n    a: int\n    b: int\n    c: Computed[int]\n    @computed(\'c\')\n    def calculate_c(a: int, b: int, **kwargs):\n        return a + b\n\nmodel = ComputedModelInt(a=1, b=2)\nprint(model.c) # Outputs 3\n```\n\n### Multiple computed properties\n\n```python\nfrom pydantic import BaseModel\nfrom pydantic_computed import Computed, computed\n\nclass MultipleComputed(BaseModel):\n    a: int\n    b: int\n    c: Computed[int]\n    d: Computed[int]\n    e: Computed[int]\n    @computed(\'c\')\n    def calc_c(a: int, b: int, **kwargs):\n        return a + b\n\n    @computed(\'d\')\n    def calc_d(c: int, **kwargs): # Note that property d uses the value of the computed property c (The order of declaration matters!)\n        return c * 2\n\nmodel = MultipleComputed(a=1, b=2)\nprint(model.c) # Outputs 3\nprint(model.d) # Outputs 6\n```\n\nSince all properties are passed as **kwargs to calculate_c, we can use the property names for the parameters\n\n\n### Complex types\n\nSuppose you set up a FastAPI application where you have users and orders stored in a database.\nAll Models in the database have an automatically generated id.\nNow you want to be able to dynamically generate links to those objects.\nE.g. the user with id=3 is accessible on the endpoint http://my-api/users/3\nInstead of storing those links in the database you can simply generate them with the computed decorator.\nexample: \n\n```python\nfrom pydantic import BaseModel, Field\nfrom pydantic_computed import Computed, computed\n\nclass Link(BaseModel):\n    href: str\n    method: str\n\nclass SchemaLinked(BaseModel):\n    id: int\n    base_url: str\n    link: Computed[Link]\n    @computed(\'link\')\n    def compute_link( id: int, base_url: str, **kwargs):        \n        return Link(href=f\'{base_url}/{id}\', method=\'GET\')\n\nclass User(SchemaLinked):\n    base_url: str = Field(\'/users\', exclude=True)\n    username: str\n\nclass Order(SchemaLinked):\n    base_url: str = Field(\'/orders\', exclude=True)\n    user: User\n\nuser = User(id=3, username=\'exampleuser\') \nuser.json()\n"""\n{\n    id: 3,\n    username: "exampleuser",\n    link: {\n        href: "/users/3",\n        method: "GET"\n    }\n}\n"""\norder = Order(id=2, user=user)\norder.json()\n"""\n{\n    id: 2,\n    link: {\n        href: "/orders/2",\n        method: "GET"\n    },\n    user: {\n        id: 3,\n        username: "exampleuser",\n        link: {\n            href: "/users/3",\n            method: "GET"\n        }\n    }\n}\n"""\n``` \n\n\n### Vector example:\n\n```python\nfrom pydantic import BaseModel\nfrom pydantic_computed import computed, Computed\nimport math\n\nclass Point(BaseModel):\n    x: int\n    y: int\n\nclass Vector(BaseModel):\n    p1: Point\n    p2: Point\n    x: Computed[float]\n    y: Computed[float]\n    weight: Computed[float]\n\n    @computed(\'x\')\n    def compute_x(p1: Point, p2: Point, **kwargs):\n        return p2.x - p1.x\n    @computed(\'y\')\n    def compute_y(p1: Point, p2: Point, **kwargs):\n        return p2.y - p1.y\n    @computed(\'weight\')\n    def compute_weight(x: float, y: float, **kwargs):\n        return math.sqrt(x ** 2 + y ** 2)\n\nv1 = Vector(p1=Point(x=0,y=0), p2=Point(x=1,y=0))\nprint(v1.weight) # Outputs 1.0\nv1.p2 = Point(x=2,y=0)\nprint(v1.weight) # Outputs now 2.0 since p2 changed\n# NOTE: if we would have written v1.p2.x = 2 instead of v1.p2 = Point(x=2, y=0), it would not have worked, because of the way pydantic triggers validations\n# The computed field only gets updated if one of the fields in the same model changes (in this case it is property p1 of Vector)\n```\n',
    'author': 'Jakob Leibetseder',
    'author_email': 'leibetsederjakob@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Maydmor/pydantic-computed',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
