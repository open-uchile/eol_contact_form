import setuptools

setuptools.setup(
    name="eol_contact_form",
    version="0.0.1",
    author="matiassalinas",
    author_email="matsalinas@uchile.cl",
    description="Eol Contact Form",
    long_description="Eol Contact Form",
    url="https://eol.uchile.cl",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "lms.djangoapp": [
            "eol_contact_form = eol_contact_form.apps:EolContactFormConfig",
        ]
    },
)
