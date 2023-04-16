from setuptools import setup

setup(
    name="bing-gpt-server",
    version="0.1.25",
    license="GNU General Public License v2.0",
    author="Jörg Thalheim (Mic92)",
    author_email="joerg@thalheim.io",
    description="Webfrontend for EdgeGPT",
    url="https://github.com/Mic92/bing-gpt-server",
    project_urls={"Bug Report": "https://github.com/Mic92/bing-gpt-server/issues/new"},
    entry_points={
        "console_scripts": ["bing-gpt-server=bing_gpt_server:main"],
    },
    install_requires=[
        "quart",
        "EdgeGPT",
    ],
    packages=["bing_gpt_server"],
    package_data={
        'bing_gpt_server': [
            'templates/*.html',
            'static/*.css',
            'static/*.js',
        ]
     },
    classifiers=[],
)
