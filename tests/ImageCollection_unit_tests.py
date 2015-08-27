"""Tests for the :class:`jicbioimage.core.image.ImageCollection` class."""

import unittest

try:
    from mock import MagicMock, patch
except ImportError:
    from unittest.mock import MagicMock, patch

class ImageCollectionTests(unittest.TestCase):
    
    def test_len(self):
        from jicbioimage.core.image import ImageCollection
        image_collection = ImageCollection()
        self.assertEqual(len(image_collection), 0)
        
    def test_has_proxy_image(self):
        from jicbioimage.core.image import ImageCollection
        image_collection = ImageCollection()
        self.assertTrue(callable(image_collection.proxy_image))

    def test_proxy_image(self):
        from jicbioimage.core.image import ImageCollection, ProxyImage
        image_collection = ImageCollection()
        image_collection.append(ProxyImage('test0.tif'))
        image_collection.append(ProxyImage('test1.tif'))

        proxy_image = image_collection.proxy_image()
        self.assertEqual(proxy_image.fpath, 'test0.tif')

        proxy_image = image_collection.proxy_image(index=1)
        self.assertEqual(proxy_image.fpath, 'test1.tif')

    def test_repr_html(self):
        from jicbioimage.core.image import ImageCollection, ProxyImage, Image
        image_collection = ImageCollection()
        image = Image((50,50))
        image.png = MagicMock(return_value=bytearray('image', encoding='utf-8'))
        with patch('jicbioimage.core.image.Image.from_file', return_value=image) as patched_image:
            image_collection.append(ProxyImage('test0.tif'))
            html = image_collection._repr_html_()
            self.assertEqual(html.strip().replace(' ', '').replace('\n', ''),
'''
<div style="float: left; padding: 2px;" >
    <p>
        <table><tr><th>Index</th><td>0</td></tr></table>
    </p>
    <img style="margin-left: auto; margin-right: auto;" src="data:image/png;base64,aW1hZ2U=" />
</div>
'''.strip().replace(' ', '').replace('\n', ''))

        image.png.assert_called_once_with(width=300)
        
if __name__ == '__main__':
    unittest.main()

