import setuptools

setuptools.setup(
    name="eol_contact_form",
    version="0.2.2",
    author="Oficina EOL UChile",
    author_email="eol-ing@uchile.cl",
    description="Eol Contact Form",
    long_description="Eol Contact Form",
    url="https://github.com/open-uchile/eol_contact_form",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "lms.djangoapp": [
            "eol_contact_form = eol_contact_form.apps:EolContactFormConfig",
        ],
         "cms.djangoapp": [
            "eol_contact_form = eol_contact_form.apps:EolContactFormConfig",
        ]
    },
)
