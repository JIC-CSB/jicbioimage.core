"""Tests for the :class:`jicbioimage.core.image.MicroscopyCollection` class."""

import unittest
from mock import MagicMock, patch

class MicroscopyCollectionTests(unittest.TestCase):
    
    def test_len(self):
        from jicbioimage.core.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertEqual(len(microscopy_collection), 0)
        
    def test_has_proxy_image(self):
        from jicbioimage.core.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(callable(microscopy_collection.proxy_image))

    def test_proxy_image(self):
        from jicbioimage.core.image import MicroscopyCollection, MicroscopyImage
        microscopy_collection = MicroscopyCollection()
        microscopy_collection.append(MicroscopyImage('test0.tif',
            dict(series=0, channel=0, zslice=0, timepoint=0)))
        microscopy_collection.append(MicroscopyImage('test1.tif',
            dict(series=1, channel=1, zslice=1, timepoint=1)))

        proxy_image = microscopy_collection.proxy_image()
        self.assertEqual(proxy_image.fpath, 'test0.tif')

        proxy_image = microscopy_collection.proxy_image(s=1, c=1, z=1, t=1)
        self.assertEqual(proxy_image.fpath, 'test1.tif')

    def test_zstack_proxy_iterator(self):
        from jicbioimage.core.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(callable(microscopy_collection.zstack_proxy_iterator))
        
    def test_zstack_proxy_iterator_is_iterable(self):
        import collections
        from jicbioimage.core.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(isinstance(microscopy_collection.zstack_proxy_iterator(),
                                   collections.Iterable))
        self.assertTrue(isinstance(microscopy_collection.zstack_proxy_iterator(),
                                   collections.Iterable))
        
    def test_zstack_array(self):
        from jicbioimage.core.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(callable(microscopy_collection.zstack_array))
        
    def test_zstack_array(self):
        from jicbioimage.core.image import MicroscopyCollection
        microscopy_collection = MicroscopyCollection()
        self.assertTrue(callable(microscopy_collection.image))

    def test_repr_html(self):
        from jicbioimage.core.image import MicroscopyCollection, MicroscopyImage, Image
        microscopy_collection = MicroscopyCollection()
        image = Image((50,50))
        image.png = MagicMock(return_value='image')
        with patch('jicbioimage.core.image.Image.from_file', return_value=image) as patched_image:
            microscopy_collection.append(MicroscopyImage('test0.tif',
                dict(series=1, channel=2, zslice=3, timepoint=4)))
            html = microscopy_collection._repr_html_()
            self.assertEqual(html.strip().replace(' ', '').replace('\n', ''),
'''
<div style="float: left; padding: 2px;" >
    <p>
        <table>
            <tr>
                <th>Index</th>
                <th>Series</th>
                <th>Channel</th>
                <th>Z-slice</th>
                <th>Time point</th>
            </tr>
            <tr>
                <td>0</td>
                <td>1</td>
                <td>2</td>
                <td>3</td>
                <td>4</td>
            </tr>
        </table>
    </p>
    <img style="margin-left: auto; margin-right: auto;" src="data:image/png;base64,aW1hZ2U=" />
</div>
'''.strip().replace(' ', '').replace('\n', ''))
        
if __name__ == '__main__':
    unittest.main()
