from unittest import TestCase

from thoth_doc.main import DocGenerator
from thoth_doc.parsers import add_image_host_to_image_links


class DocGeneratorTestCase(TestCase):
    def test_generate(self):
        class MockGenerator(DocGenerator):
            parsers = [add_image_host_to_image_links]
        generator = MockGenerator('src/thoth_doc/docs', 'src/thoth_doc/docs_compiled')
        generator.image_host = 'https://example.com'
        generator.generate()
