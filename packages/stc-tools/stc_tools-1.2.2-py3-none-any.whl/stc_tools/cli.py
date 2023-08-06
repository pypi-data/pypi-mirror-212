#!/usr/bin/env python3
import json
import os.path
import sys

import fire
from stc_tools.client import StcTools
from termcolor import colored


class ItemNotFound(Exception):
    def __init__(self, query):
        self.query = query

    def __str__(self):
        return f'ItemNotFound(query="{self.query}")'


class CidNotFound(Exception):
    def __init__(self, query):
        self.query = query

    def __str__(self):
        return f'CidNotFound(query="{self.query}")'


class StcCliTools(StcTools):
    default_default_fields = {
        'nexus_science': ['title', 'abstract', ],
        'nexus_books': ['title', ],
    }

    def __init__(
            self,
            ipfs_http_endpoint: str = 'http://127.0.0.1:8080',
            index_name: str = 'nexus_science',
            timeout: int = 600,
    ):
        super().__init__(ipfs_http_endpoint=ipfs_http_endpoint,
                         paths=(f'/ipns/standard-template-construct.org/data/{index_name}/',))
        self.index_name = index_name
        self.timeout = timeout

    async def search(self, query: str, limit: int = 1):
        """
        Searches in STC using default Summa match queries.
        Examples: `doi:10.1234/abc, isbns:9781234567890, "fetal hemoglobin"`

        :param query: query in Summa match format
        :param limit: how many results to return, higher values incurs LARGE performance penalty.

        :return: metadata records
        """
        print(f"{colored('INFO', 'green')}: Setting up indices: {', '.join(self.paths)}...")
        await self.start()
        print(f"{colored('INFO', 'green')}: Searching {query}...")
        response = await super().search([{
            "index_alias": self.index_name,
            "query": {
                "match": {"value": query, "default_fields": self.default_default_fields[self.index_name],
                          'field_boosts': {}}},
            "collectors": [{"top_docs": {"limit": limit}}],
            "is_fieldnorms_scoring_enabled": False,
        }])
        return list(
            map(lambda x: json.loads(x.document), response.collector_outputs[0].documents.scored_documents))

    async def download(self, query: str, output_path: str):
        """
        Download file from STC using default Summa match queries.
        Examples: `doi:10.1234/abc, isbns:9781234567890`

        :param query: query in Summa match format
        :param output_path: filepath for writing file

        :return: file if record has corresponding CID
        """
        results = await self.search(query)
        output_path, output_path_ext = os.path.splitext(output_path)
        output_path_ext = output_path_ext.lstrip('.')
        if results:
            print(f"{colored('INFO', 'green')}: Found {query}")
            if 'cid' in results[0]:
                print(f"{colored('INFO', 'green')}: Receiving file {query}...")
                if (real_extension := results[0].get('extension', 'pdf')) != output_path_ext:
                    print(
                        f"{colored('WARN', 'yellow')}: Receiving file extension `{real_extension}` is not matching with your output path extension `{output_path_ext}`. Changed to correct one.")
                    output_path_ext = real_extension
                data = await super().download(results[0]["cid"], self.timeout)
                final_file_name = output_path + '.' + output_path_ext
                with open(final_file_name, 'wb') as f:
                    f.write(data)
                    f.close()
                    print(f"{colored('INFO', 'green')}: File {final_file_name} is written")
            else:
                print(f"{colored('ERROR', 'red')}: Not found CID for {query}", file=sys.stderr)
        else:
            print(f"{colored('ERROR', 'red')}: Not found {query}", file=sys.stderr)


async def stc_tools_cli(
        ipfs_http_endpoint: str = 'http://127.0.0.1:8080',
        index_name: str = 'nexus_science',
        timeout: int = 600
):
    """

    :param ipfs_http_endpoint: IPFS HTTP API Endpoint
    :param index_name: `nexus_books` (similar to LibGen) or `nexus_science` (similar to Crossref)
    :param timeout: timeout for requests to IPFS
    :return:
    """
    stc_tools_client = StcCliTools(ipfs_http_endpoint, index_name, timeout)
    return {
        'search': stc_tools_client.search,
        'download': stc_tools_client.download,
    }


def main():
    fire.Fire(stc_tools_cli, name='stc-tools')


if __name__ == '__main__':
    main()
