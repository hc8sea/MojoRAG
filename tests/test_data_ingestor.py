# import os
# import pytest
# from models import Message
# from data_ingestor import *

# @pytest.fixture
# def sample_markdown(tmpdir):
#     """Creates a sample markdown file for testing."""
#     sample_md = """
#     # Sample Title
    
#     This is a sample markdown content.
    
#     ## Subtitle
    
#     More content here.
#     """
#     file_path = os.path.join(tmpdir, "sample.md")
#     with open(file_path, "w") as f:
#         f.write(sample_md)
#     return file_path

# def test_parse_arguments():
#     """Test parse_arguments function."""
#     args = parse_arguments(["--data-path", "../data/mojo/docs/*.md"])
#     assert args.data_path == "../data/mojo/docs/*.md"

# def test_split_text():
#     """Test split_text function."""
#     content = "# Header 1\n\nText for header 1.\n\n## Header 2\n\nText for header 2."
#     markdown_splitter = setup_markdown_splitter()
#     token_splitter = setup_token_splitter()
#     split_texts = split_text(content, markdown_splitter, token_splitter)
#     assert len(split_texts) == 2

# def test_setup_markdown_splitter():
#     """Test setup_markdown_splitter function."""
#     markdown_splitter = setup_markdown_splitter()
#     assert markdown_splitter is not None

# def test_setup_token_splitter():
#     """Test setup_token_splitter function."""
#     token_splitter = setup_token_splitter()
#     assert token_splitter is not None

# def test_setup_chromadb():
#     """Test setup_chromadb function."""
#     chroma_collection = setup_chromadb()
#     assert chroma_collection is not None

# def test_read_file_content(sample_markdown):
#     """Test read_file_content function."""
#     title, content = read_file_content(sample_markdown)
#     assert title == "Sample Title"
#     assert "This is a sample markdown content." in content

# def test_prepare_metadata():
#     """Test prepare_metadata function."""
#     token_split_texts = ["chunk1", "chunk2", "chunk3"]
#     base_filename = "sample.md"
#     title = "Sample Title"
#     metadata = prepare_metadata(token_split_texts, base_filename, title)
#     assert len(metadata) == len(token_split_texts)
#     assert metadata[0]["filename"] == base_filename
#     assert metadata[0]["title"] == title

# def test_ingest_chunks():
#     """Test ingest_chunks function."""
#     collection = setup_chromadb()
#     ids = ["id1", "id2", "id3"]
#     documents = ["doc1", "doc2", "doc3"]
#     metadatas = [{"meta1": "data1"}, {"meta2": "data2"}, {"meta3": "data3"}]
#     ingest_chunks(ids, documents, metadatas, collection)
#     # It's difficult to assert something here without querying the collection

# def test_process_file(tmpdir):
#     """Test process_file function."""
#     markdown_splitter = setup_markdown_splitter()
#     token_splitter = setup_token_splitter()
#     chroma_collection = setup_chromadb()

#     sample_md_path = os.path.join(tmpdir, "sample.md")
#     sample_md = """
#     # Sample Title
    
#     This is a sample markdown content.
    
#     ## Subtitle
    
#     More content here.
#     """
#     with open(sample_md_path, "w") as f:
#         f.write(sample_md)

#     total_chunks_added = process_file(sample_md_path, markdown_splitter, token_splitter, chroma_collection, 0)
#     assert total_chunks_added > 0

# def test_main(tmpdir):
#     """Test main function."""
#     data_path = os.path.join(tmpdir, "*.md")
#     args = argparse.Namespace(data_path=data_path)
#     main()
