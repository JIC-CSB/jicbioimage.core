"""Tests for the :class:`jicimagelib.image.ImageCollection` class."""

import unittest
from mock import MagicMock, patch

class ImageCollectionTests(unittest.TestCase):
    
    def test_len(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertEqual(len(image_collection), 0)
        
    def test_has_proxy_image(self):
        from jicimagelib.image import ImageCollection
        image_collection = ImageCollection()
        self.assertTrue(callable(image_collection.proxy_image))

    def test_proxy_image(self):
        from jicimagelib.image import ImageCollection, ProxyImage
        image_collection = ImageCollection()
        image_collection.append(ProxyImage('test0.tif'))
        image_collection.append(ProxyImage('test1.tif'))

        proxy_image = image_collection.proxy_image()
        self.assertEqual(proxy_image.fpath, 'test0.tif')

        proxy_image = image_collection.proxy_image(index=1)
        self.assertEqual(proxy_image.fpath, 'test1.tif')

    def test_repr_html(self):
        from jicimagelib.image import ImageCollection, ProxyImage, Image
        image_collection = ImageCollection()
        image = Image((50,50))
        image.png = MagicMock(return_value='image')
        with patch('jicimagelib.image.Image.from_file', return_value=image) as patched_image:
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
        
if __name__ == '__main__':
    unittest.main()

