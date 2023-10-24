from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from loguru import logger
from tqdm import tqdm


def config_text_splitter(
    chunk_size=512,
    chunk_overlap=20,
    length_function="len",
    add_start_index=True,
):
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=length_function,
        add_start_index=add_start_index,
    )
    return text_splitter


def preprocess_pdf(
    pdf_path="/mnt/c/Users/Angus/Downloads/eStatementFile_20231011021455.pdf",
    text_splitter: RecursiveCharacterTextSplitter = None,
):
    """
    Load and split a single PDF file
    """
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split(text_splitter)
    return pages


def preprocess_pdf_from_directory(
    path="/mnt/c/Users/Angus/Downloads",
    glob="**/*.pdf",
    use_multithreading=False,
    max_concurrency=4,
    show_progress=True,
    text_splitter: RecursiveCharacterTextSplitter = None,
):
    """
    Load and split PDF files from a directory
    """
    loader = DirectoryLoader(
        path,
        glob=glob,
        use_multithreading=use_multithreading,
        max_concurrency=max_concurrency,
        show_progress=show_progress,
    )
    logger.info("Loading PDFs")
    pages = loader.load_and_split(text_splitter)
    return pages


def get_pdf_embeddings(pages,embedding_model_name="ada"):
    # TODO add multi thread to speed up
    
    embeddings = OpenAIEmbeddings(model_name=embedding_model_name)
    # Turn the first text chunk into a vector with the embedding[
    logger.info("Getting embeddings")
    embeds = [embeddings.embed_query(page.page_content) for page in tqdm(pages)]
    return embeds
