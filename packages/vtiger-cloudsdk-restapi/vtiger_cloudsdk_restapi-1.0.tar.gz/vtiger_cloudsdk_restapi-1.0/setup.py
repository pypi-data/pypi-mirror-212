from setuptools import setup

setup(
	name='vtiger_cloudsdk_restapi',
	description='Vtiger Cloud RestApi',
        version='1.0',
	author='Vtiger',
	author_email='info@vtiger.com',
	license='VPL',
	packages=['vtiger_cloudsdk_restapi'],
        keywords=['Vtiger', 'Vtiger CRM', 'Cloud', 'SDK'],
	install_requires=[
		'requests'
	],
	zip_safe=False
)
