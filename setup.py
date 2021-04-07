from setuptools import setup


setup(
    name='cldfbench_hdi',
    py_modules=['cldfbench_hdi'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'hdi=cldfbench_hdi:Dataset',
        ]
    },
    install_requires=[
        'cldfbench',
        'pydictionaria>=2.0',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
