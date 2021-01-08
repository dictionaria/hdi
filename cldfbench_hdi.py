from collections import ChainMap
import pathlib

from pydictionaria.formats import sfm
from pydictionaria.formats.sfm_lib import Database as SFM
from pydictionaria import sfm2cldf

from cldfbench import CLDFSpec, Dataset as BaseDataset


def with_defaults(properties):
    new_props = {
        'entry_sep': properties.get('entry_sep') or sfm2cldf.DEFAULT_ENTRY_SEP,
        'marker_map': ChainMap(
            properties.get('entry_map') or {}, sfm.DEFAULT_MARKER_MAP),
        'entry_map': ChainMap(
            properties.get('entry_map') or {}, sfm2cldf.DEFAULT_ENTRY_MAP),
        'sense_map': ChainMap(
            properties.get('sense_map') or {}, sfm2cldf.DEFAULT_SENSE_MAP),
        'example_map': ChainMap(
            properties.get('example_map') or {}, sfm2cldf.DEFAULT_EXAMPLE_MAP),
    }
    new_props.update(
        (k, v) for k, v in properties.items() if k not in new_props)
    return new_props


def amend_cldf_schema(cldf, properties):
    cldf.add_component(
        'ExampleTable',
        {
            'datatype': 'string',
            'separator': ' ; ',
            'name': 'Sense_IDs',
        })

    cldf.add_foreign_key(
        'ExampleTable', 'Sense_IDs', 'SenseTable', 'ID')


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "hdi"

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return CLDFSpec(
            dir=self.cldf_dir,
            module='Dictionary',
            metadata_fname='cldf-metadata.json')

    def cmd_download(self, args):
        """
        Download files to the raw/ directory. You can use helpers methods of `self.raw_dir`, e.g.

        >>> self.raw_dir.download(url, fname)
        """
        pass

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.

        >>> args.writer.objects['LanguageTable'].append(...)
        """

        # read data

        properties = with_defaults(self.etc_dir.read_json('properties.json'))

        sfm = SFM(
            self.raw_dir / 'db.sfm',
            marker_map=properties['marker_map'],
            entry_sep=properties['entry_sep'])

        # cldf schema

        amend_cldf_schema(args.writer.cldf, properties)

        # processing

        # output
